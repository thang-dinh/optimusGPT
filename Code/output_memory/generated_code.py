# nurse_schedule_fixed.py
from gurobipy import Model, GRB, quicksum

# ---------- Parameters ----------
nurses = [
    'Alice', 'Ben', 'Cara', 'Dana', 'Ethan', 'Fiona',
    'Grace', 'Hannah', 'Ian', 'Jordan', 'Kelly', 'Liam', 'Mia', 'Noah', 'Olivia'
]
days = range(14)            # 14 days
shifts = ['Morning', 'Evening', 'Night']
shift_hours = 8

# Role groupings (based on your data)
RNs = ['Alice', 'Ben', 'Cara', 'Dana', 'Ethan', 'Fiona', 'Noah', 'Olivia']
ICU_RNs = ['Alice', 'Cara', 'Fiona', 'Olivia']
LPNs = ['Grace', 'Hannah', 'Ian']
experienced_LPNs = ['Grace', 'Hannah']  # >3 years
NAs = ['Jordan', 'Kelly', 'Liam', 'Mia']

# Charge Nurse eligible
charge_eligible = ['Alice', 'Cara', 'Ethan', 'Fiona', 'Olivia']

# Availability / restrictions (explicit)
# - Cara: no weekends
# - Dana: M–F only (no weekends)
# - Ben: no Fridays
# - Ian: no Fri–Sun
# - Kelly: not available weekends
# - Mia: minor -> no Evening/Night
# - Fiona prefers nights
# - Olivia prefers mornings
no_weekend = {'Cara', 'Dana', 'Kelly'}
# Map day index -> weekday name for clarity (0 = Monday)
weekday_names = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

# Helper to get weekday index from absolute day
def weekday(d): return d % 7

# ---------- Model ----------
model = Model("Nurse_Scheduling")
model.setParam('OutputFlag', 1)  # set to 0 to silence solver output

# Decision vars: x[n,d,s] = 1 if nurse n works day d shift s
x = model.addVars(nurses, days, shifts, vtype=GRB.BINARY, name="x")

# Soft-preference helpers (we'll penalize missing preferences)
# p_fiona_d = 1 - x[fiona,d,'Night'] -> penalizes Fiona not working nights
# p_olivia_d = 1 - x[olivia,d,'Morning'] -> penalizes Olivia not working mornings
p_fiona = model.addVars(days, vtype=GRB.CONTINUOUS, lb=0, ub=1, name="p_fiona")
p_olivia = model.addVars(days, vtype=GRB.CONTINUOUS, lb=0, ub=1, name="p_olivia")

# ---------- Objective ----------
# Primary: minimize total number of assigned shifts (a simple fairness proxy).
# Secondary: lightly penalize preference violations so Fiona/Olivia are scheduled as preferred when feasible.
total_shifts = quicksum(x[n, d, s] for n in nurses for d in days for s in shifts)
pref_penalty = 0.2 * (quicksum(p_fiona[d] for d in days) + quicksum(p_olivia[d] for d in days))
model.setObjective(total_shifts + pref_penalty, GRB.MINIMIZE)

# ---------- Constraints ----------

# 1) Per-shift coverage requirements (per day d and shift s)
for d in days:
    for s in shifts:
        # exactly 1 charge nurse
        model.addConstr(quicksum(x[n, d, s] for n in charge_eligible) == 1,
                        name=f"ChargeNurse_eq1_d{d}_s{s}")

        # total RNs >= 3 (including the charge nurse)
        model.addConstr(quicksum(x[n, d, s] for n in RNs) >= 3, name=f"RN_coverage_d{d}_s{s}")

        # LPNs >= 2
        model.addConstr(quicksum(x[n, d, s] for n in LPNs) >= 2, name=f"LPN_coverage_d{d}_s{s}")

        # NAs >= 2
        model.addConstr(quicksum(x[n, d, s] for n in NAs) >= 2, name=f"NA_coverage_d{d}_s{s}")

        # ICU RN >= 1
        model.addConstr(quicksum(x[n, d, s] for n in ICU_RNs) >= 1, name=f"ICU_req_d{d}_s{s}")

        # at least one experienced LPN per shift
        model.addConstr(quicksum(x[n, d, s] for n in experienced_LPNs) >= 1,
                        name=f"ExpLPN_req_d{d}_s{s}")

# 2) Max one shift per nurse per day
for n in nurses:
    for d in days:
        model.addConstr(quicksum(x[n, d, s] for s in shifts) <= 1, name=f"max1shift_{n}_d{d}")

# 3) Max 40 hours per week (for each of the two weeks)
for n in nurses:
    for wk in range(2):
        days_in_week = range(wk * 7, wk * 7 + 7)
        model.addConstr(quicksum(x[n, d, s] * shift_hours for d in days_in_week for s in shifts) <= 40,
                        name=f"max40h_{n}_wk{wk}")

# 4) No Night -> Morning the next day, and no Evening -> Morning (ensures min rest)
for n in nurses:
    for d in range(13):  # pairs (d, d+1) up to day 12 -> 13 pairs
        model.addConstr(x[n, d, 'Night'] + x[n, d + 1, 'Morning'] <= 1,
                        name=f"no_Night2Morning_{n}_d{d}")
        model.addConstr(x[n, d, 'Evening'] + x[n, d + 1, 'Morning'] <= 1,
                        name=f"no_Evening2Morning_{n}_d{d}")

# 5) No more than 6 consecutive working days
for n in nurses:
    for start in range(0, 8):  # start indices 0..7 for a 7-day window within 14 days
        model.addConstr(quicksum(x[n, d, s] for d in range(start, start + 7) for s in shifts) <= 6,
                        name=f"max6consec_{n}_start{start}")

# 6) Availability / restrictions (hard)
for d in days:
    wd = weekday(d)
    # Cara & Dana: cannot work weekends (Sat=5, Sun=6)
    for n in ('Cara', 'Dana', 'Kelly'):
        if wd in {5, 6}:
            for s in shifts:
                model.addConstr(x[n, d, s] == 0, name=f"{n}_no_weekend_d{d}_s{s}")

    # Ben: cannot work Fridays (Friday index is 4 when Monday=0)
    if wd == 4:
        for s in shifts:
            model.addConstr(x['Ben', d, s] == 0, name=f"Ben_no_Fri_d{d}_s{s}")

    # Ian: cannot work Fri-Sun (4,5,6)
    if wd in {4, 5, 6}:
        for s in shifts:
            model.addConstr(x['Ian', d, s] == 0, name=f"Ian_no_FriSatSun_d{d}_s{s}")

    # Kelly: not available weekends
    if wd in {5, 6}:
        for s in shifts:
            model.addConstr(x['Kelly', d, s] == 0, name=f"Kelly_no_weekend_d{d}_s{s}")

    # Mia: minor -> cannot work Evening or Night
    for s in ('Evening', 'Night'):
        model.addConstr(x['Mia', d, s] == 0, name=f"Mia_no_late_d{d}_s{s}")

# 7) Soft preference linking for Fiona and Olivia
# p_fiona[d] = 1 - x[Fiona, d, 'Night']  -> minimize p_fiona
# p_olivia[d] = 1 - x[Olivia, d, 'Morning']
for d in days:
    model.addConstr(p_fiona[d] >= 1 - x['Fiona', d, 'Night'], name=f"p_fiona_lb_d{d}")
    model.addConstr(p_fiona[d] >= 0, name=f"p_fiona_nonneg_d{d}")  # redundant due to var lb=0
    model.addConstr(p_olivia[d] >= 1 - x['Olivia', d, 'Morning'], name=f"p_olivia_lb_d{d}")
    model.addConstr(p_olivia[d] >= 0, name=f"p_olivia_nonneg_d{d}")

# 8) Weekend shift rule: ensure at least one non-restricted staff scheduled per shift on weekends (soft fairness baseline)
# "Non-restricted" pool = all nurses except those explicitly no_weekend and Ben/Ian restrictions
non_restricted = [n for n in nurses if n not in {'Cara', 'Dana', 'Ben', 'Ian', 'Kelly'}]
for week in range(2):
    weekend_days = [week * 7 + 5, week * 7 + 6]  # Sat, Sun indices
    for d in weekend_days:
        for s in shifts:
            model.addConstr(quicksum(x[n, d, s] for n in non_restricted) >= 1,
                            name=f"weekend_nonrestricted_atleast1_week{week}_d{d}_s{s}")

# ---------- Optimize ----------
model.optimize()

# ---------- Print solution ----------
if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
    print("\nSchedule (nurse -> day, shift):\n")
    for d in days:
        print(f"Day {d} ({weekday_names[weekday(d)]})")
        for s in shifts:
            assigned = [n for n in nurses if x[n, d, s].X > 0.5]
            print(f"  {s:8}: {', '.join(assigned)}")
        print("-" * 60)
else:
    print("No feasible solution found. Model status:", model.status)
