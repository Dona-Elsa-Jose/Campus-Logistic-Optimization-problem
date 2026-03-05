import pulp

# 1. Initialize the Model
model = pulp.LpProblem("Campus_Logistics_Optimization", pulp.LpMinimize)

# 2. Data Definition
warehouses = ["NORTH", "SOUTH", "EAST"]
facilities = ["MED_CENTER", "ENG_BLDG", "SCI_HALL", "DORM_A", "DORM_B", "LIBRARY"]

demand = {"MED_CENTER": 80, "ENG_BLDG": 30, "SCI_HALL": 35, "DORM_A": 55, "DORM_B": 51, "LIBRARY": 30}
capacity = {"NORTH": 400, "SOUTH": 350, "EAST": 450}

# Annual Fixed Costs = (Construction / 10) + (Daily Op * 365)
fixed_costs = {
    "NORTH": (300000 / 10) + (800 * 365),
    "SOUTH": (280000 / 10) + (700 * 365),
    "EAST": (320000 / 10) + (900 * 365)
}

# Average Transportation Cost per unit annually (Estimated at $4.00/unit * 365 days)
transport_rate = 4.0 * 365

# 3. Decision Variables
y = pulp.LpVariable.dicts("Open", warehouses, cat=pulp.LpBinary)
x = pulp.LpVariable.dicts("Ship", (warehouses, facilities), lowBound=0, cat=pulp.LpContinuous)

# 4. Objective Function: Minimize Total Annual Cost
model += (
    pulp.lpSum([fixed_costs[i] * y[i] for i in warehouses]) +
    pulp.lpSum([x[i][j] * transport_rate for i in warehouses for j in facilities])
)

# 5. Constraints
model += pulp.lpSum([y[i] for i in warehouses]) == 2  # Must open exactly 2

for j in facilities:
    model += pulp.lpSum([x[i][j] for i in warehouses]) == demand[j]  # Meet all demand

for i in warehouses:
    model += pulp.lpSum([x[i][j] for j in facilities]) <= capacity[i] * y[i]  # Capacity & Link

# 6. Solve
model.solve(pulp.PULP_CBC_CMD(msg=0))

# 7. Output
print(f"Optimization Status: {pulp.LpStatus[model.status]}")
for i in warehouses:
    if y[i].varValue == 1:
        print(f"✅ Open Warehouse: {i}")