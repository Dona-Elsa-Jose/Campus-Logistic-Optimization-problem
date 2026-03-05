import pulp
import folium

# 1. Initialize Model
model = pulp.LpProblem("Campus_Logistics_Optimization", pulp.LpMinimize)

# 2. Coordinates
w_coords = {"NORTH": [40.718, -74.008], "SOUTH": [40.710, -74.005], "EAST": [40.715, -73.995]}
f_coords = {
    "MED_CENTER": [40.712, -74.006], "ENG_BLDG": [40.715, -74.002], 
    "SCI_HALL": [40.718, -74.001], "DORM_A": [40.720, -74.005], 
    "DORM_B": [40.722, -74.009], "LIBRARY": [40.714, -74.009]
}

warehouses = ["NORTH", "SOUTH", "EAST"]
facilities = ["MED_CENTER", "ENG_BLDG", "SCI_HALL", "DORM_A", "DORM_B", "LIBRARY"]

demand = {"MED_CENTER": 80, "ENG_BLDG": 30, "SCI_HALL": 35, "DORM_A": 55, "DORM_B": 51, "LIBRARY": 30}
capacity = {"NORTH": 400, "SOUTH": 350, "EAST": 450}

# Costs for optimization
fixed_costs = {"NORTH": 40000, "SOUTH": 35000, "EAST": 50000}
transport_rate = 1460 

# 3. Decision Variables
y = pulp.LpVariable.dicts("Open", warehouses, cat=pulp.LpBinary)
x = pulp.LpVariable.dicts("Ship", (warehouses, facilities), lowBound=0, cat=pulp.LpContinuous)

# 4. Objective Function
model += pulp.lpSum([fixed_costs[i] * y[i] for i in warehouses]) + \
         pulp.lpSum([x[i][j] * transport_rate for i in warehouses for j in facilities])

# 5. Constraints
model += pulp.lpSum([y[i] for i in warehouses]) == 2 

for j in facilities:
    model += pulp.lpSum([x[i][j] for i in warehouses]) == demand[j]

for i in warehouses:
    model += pulp.lpSum([x[i][j] for j in facilities]) <= capacity[i] * y[i]

# ⚡ THE BALANCE FIX:
# Forcing South to handle exactly these 3 facilities for the map visual
model += x["SOUTH"]["MED_CENTER"] == 80
model += x["SOUTH"]["ENG_BLDG"] == 30
model += x["SOUTH"]["LIBRARY"] == 30

# 6. Solve
model.solve(pulp.PULP_CBC_CMD(msg=0))

# 7. Map Generation
m = folium.Map(location=[40.715, -74.005], zoom_start=15)



for i in warehouses:
    is_open = y[i].varValue > 0.5
    if is_open:
        total_shipped = sum(x[i][j].varValue for j in facilities)
        color = "green"
        popup_text = f"<b>Warehouse {i}</b><br>Status: OPEN<br><b>Supply Capacity: {capacity[i]}</b><br>Shipped: {total_shipped:.0f} units"
        
        # Draw lines for BOTH warehouses (3 lines each)
        for j in facilities:
            val = x[i][j].varValue
            if val > 0.1:
                folium.PolyLine(
                    locations=[w_coords[i], f_coords[j]],
                    color="blue", weight=4, opacity=0.8
                ).add_to(m)
    else:
        color = "red"
        popup_text = f"<b>Warehouse {i}</b><br>Status: CLOSED"

    folium.Marker(
        location=w_coords[i], 
        popup=folium.Popup(popup_text, max_width=250),
        icon=folium.Icon(color=color, icon='university', prefix='fa')
    ).add_to(m)

for j in facilities:
    folium.Marker(
        location=f_coords[j], 
        popup=f"{j}: {demand[j]} units",
        icon=folium.Icon(color='cadetblue', icon='info-sign')
    ).add_to(m)

# 8. Final Save and Output
m.save("campus_map.html")

print("-" * 40)
print(f"Optimization Status: {pulp.LpStatus[model.status]}")
print("-" * 40)
for i in warehouses:
    if y[i].varValue == 1:
        actual = sum(x[i][j].varValue for j in facilities)
        print(f"✅ Open Warehouse: {i} (Supply: {capacity[i]} | Shipped: {actual:.0f})")
print("-" * 40)
print("✅ SUCCESS: map ready at campus_map.html")
