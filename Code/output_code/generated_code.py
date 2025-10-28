# Import the Gurobi library
from gurobipy import Model, GRB

# Create a new model
model = Model("Cautious Asset Investment")

# Define the total investment amount
total_investment = 150000

# Create decision variables for the amount invested in money market fund and foreign bonds
money_market = model.addVar(name="MoneyMarket", lb=0)  # Investment in money market fund
foreign_bonds = model.addVar(name="ForeignBonds", lb=0)  # Investment in foreign bonds

# Set the objective function to maximize the total return
# Money market return is 2% and foreign bonds return is 10%
model.setObjective(0.02 * money_market + 0.10 * foreign_bonds, GRB.MAXIMIZE)

# Add constraints
# 1. Total investment must equal $150,000
model.addConstr(money_market + foreign_bonds == total_investment, "TotalInvestment")

# 2. Minimum investment in money market fund is 40% of total investment
model.addConstr(money_market >= 0.40 * total_investment, "MinMoneyMarket")

# 3. Maximum investment in foreign bonds is 40% of total investment
model.addConstr(foreign_bonds <= 0.40 * total_investment, "MaxForeignBonds")

# Optimize the model
model.optimize()

# Print the results
if model.status == GRB.OPTIMAL:
    print(f"Optimal investment in Money Market Fund: ${money_market.X:.2f}")
    print(f"Optimal investment in Foreign Bonds: ${foreign_bonds.X:.2f}")
else:
    print("No optimal solution found.")