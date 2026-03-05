import pulp
import pandas as pd
import folium
import os

# 1. Initialize the Model
# We want to minimize costs, so we use LpMinimize
model = pulp.LpProblem("Campus_Logistics_Optimization", pulp.LpMinimize)

# 2. Data Definition
# Hardcoded coordinates for the map (adjust these to your actual campus if needed)
w_coords = {"NORTH": [40.718, -74.008], "SOUTH": [40.710, -74.005], "EAST": [40.715, -73.995]}
f_coords = {
    "MED_CENTER": [40.712, -74.006], "ENG_BLDG": [40.715, -74.002], 
    "SCI_HALL": [40.718, -74.001], "DORM_A": [40.720, -74.005], 
    "DORM_B": [40.722, -74.009], "LIBRARY": [40.714, -74.009]
}

# The parameters from your project description
warehouses = ["NORTH", "SOUTH", "EAST"]
facilities = ["MED_CENTER", "ENG_BLDG", "SCI_HALL", "DORM_A", "DORM_B", "LIBRARY"]

demand = {"MED_CENTER": 80, "ENG_BLDG": 30, "SCI_HALL": 35, "DORM_A": 55, "DORM_B": 51, "LIBRARY": 30}
capacity = {"NORTH": 400, "SOUTH": 350, "EAST": 450}

# Annual Fixed Costs = (Construction / 10 year depreciation) + (Daily Op * 365)
fixed_costs = {
    "NORTH": (300000 / 10) + (800 * 365),
    "SOUTH": (280000 / 10) + (700 * 365),
    "EAST": (320000 / 10) + (900 * 365)
}

# Transportation cost per unit annually (Estimated at $4.00/unit * 365 days)
transport_rate = 4.0 * 365

# 3. Decision Variables
# y: Binary (1 if open, 0 if closed)
y = pulp.LpVariable.dicts("Open", warehouses, cat=pulp.LpBinary)
# x: Continuous (Amount shipped from i to j)
x = pulp.LpVariable.dicts("Ship", (warehouses, facilities), lowBound=0, cat=pulp.LpContinuous)

# 4. Objective Function: Minimize Total Annual Cost
model += (
    pulp.lpSum([fixed_costs[i] * y[i] for i in warehouses]) +
    pulp.lpSum([x[i][j] * transport_rate for i in warehouses for j in facilities])
)

# 5. Constraints
model += pulp.lpSum([y[i] for i in warehouses]) == 2  # Must open exactly 2 warehouses

for j in facilities:
    model += pulp.lpSum([x[i][j] for i in warehouses]) == demand[j]  # Meet all demand

for i in warehouses:
    # Linking Constraint: If y[i] is 0, then capacity is 0
    model += pulp.lpSum([x[i][j] for j in facilities]) <= capacity[i] * y[i]

# 6. Solve
model.solve(pulp.PULP_CBC_CMD(msg=0))

# 7. Professional Output
print("-" * 40)
print(f"Optimization Status: {pulp.LpStatus[model.status]}")
print(f"Minimal Annual Cost: ${pulp.value(model.objective):,.2f}")
print("-" * 40)

for i in warehouses:
    if y[i].varValue == 1:
        print(f"✅ Open Warehouse: {i}")
print("-" * 40)

# 8. Map Generation (Folium)
m = folium.Map(location=[40.715, -74.005], zoom_start=15)

# Add Warehouses
for i in warehouses:
    is_open = y[i].varValue > 0.5
    status = "OPEN" if is_open else "CLOSED"
    color = "green" if is_open else "red"
    
    folium.Marker(
        location=w_coords[i],
        popup=f"Warehouse {i}: {status}",
        icon=folium.Icon(color=color, icon='university', prefix='fa')
    ).add_to(m)
    
    # Draw Blue lines for shipments from open warehouses
    if is_open:
        for j in facilities:
            if x[i][j].varValue > 0:
                folium.PolyLine(
                    locations=[w_coords[i], f_coords[j]],
                    color="blue", weight=2, opacity=0.5
                ).add_to(m)

# Add Facility Markers
for j in facilities:
    folium.Marker(
        location=f_coords[j],
        popup=f"{j} (Demand: {demand[j]})",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

m.save("campus_map.html")
print("✅ SUCCESS: 'campus_map.html' has been generated.")