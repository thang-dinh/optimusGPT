# Import the Gurobi library
from gurobipy import Model, GRB

# Create a new model
model = Model("Cautious Asset Investment")

# Define the total investment amount
total_investment = 150000

# Create decision variables for the investment in money market fund and foreign bonds
money_market_investment = model.addVar(name="MoneyMarket", lb=0)  # Investment in money market fund
foreign_bonds_investment = model.addVar(name="ForeignBonds", lb=0)  # Investment in foreign bonds

# Set the objective function to maximize the total return
# Return from money market fund is 2% and from foreign bonds is 10%
model.setObjective(0.02 * money_market_investment + 0.10 * foreign_bonds_investment, GRB.MAXIMIZE)

# Add constraints
# Total investment must equal $150,000
model.addConstr(money_market_investment + foreign_bonds_investment == total_investment, "TotalInvestment")

# Minimum investment in money market fund must be 40% of total investment
model.addConstr(money_market_investment >= 0.40 * total_investment, "MinMoneyMarket")

# Maximum investment in foreign bonds must be 40% of total investment
model.addConstr(foreign_bonds_investment <= 0.40 * total_investment, "MaxForeignBonds")

# Optimize the model
model.optimize()

# Print the results
if model.status == GRB.OPTIMAL:
    print(f"Optimal investment in Money Market Fund: ${money_market_investment.X:.2f}")
    print(f"Optimal investment in Foreign Bonds: ${foreign_bonds_investment.X:.2f}")
else:
    print("No optimal solution found.")