# 🚚 Campus City Logistics – Supply Distribution Optimization

## 📌 Project Overview
As an optimization analyst at **Campus City Logistics**, this project aims to design an optimal supply distribution network for essential resources across campus facilities. The goal is to transition from an inefficient ad-hoc system to a mathematically optimized plan that minimizes total annual costs while strictly adhering to budget and capacity constraints.

## 🎯 Problem Statement
The objective is to determine the optimal warehouse locations and shipment flows to minimize expenditures while ensuring service reliability.

### Key Constraints:
1. **Budget:** Total Annual Cost must remain $\le$ **$1,500,000**.
2. **Redundancy:** Exactly **2 warehouses** must be commissioned.
3. **Demand:** All facilities must receive 100% of their daily resource requirements.
4. **Capacity:** Shipments cannot exceed the maximum daily capacity of the active warehouses.
5. **Financial Period:** 1 Year (365 Days). Construction costs are amortized over 10 years for annual budgeting.

## 📊 Dataset Overview

### Facilities Data
| Facility ID | Facility Name | Type | Daily Demand (Units) |
| :--- | :--- | :--- | :--- |
| MED_CENTER | Campus Medical Center | Hospital | 80 |
| ENG_BUILDING | Engineering Building | Academic | 30 |
| SCIENCE_HALL | Science Hall | Academic | 35 |
| DORM_A | North Dormitory | Residential | 55 |
| DORM_B | South Dormitory | Residential | 51 |
| LIBRARY | Main Library | Academic | 30 |

*Total Daily Demand ≈ 281 Units/Day*

### Warehouse Data
| Warehouse ID | Warehouse Name | Daily Capacity | Construction Cost | Daily Op. Cost |
| :--- | :--- | :--- | :--- | :--- |
| WH_NORTH | North Campus Warehouse | 400 | $300,000 | $800 |
| WH_SOUTH | South Campus Warehouse | 350 | $280,000 | $700 |
| WH_EAST | East Gate Warehouse | 450 | $320,000 | $900 |

## ⚙️ Solution Approach

### Optimization Technique
**Mixed Integer Linear Programming (MILP)** using the **PuLP** library in Python.

### Decision Variables
| Variable | Type | Description |
| :--- | :--- | :--- |
| Warehouse Selection | Binary | Open or Close Warehouse (1 or 0) |
| Shipment Quantity | Continuous | Units shipped from Warehouse $i$ to Facility $j$ |



## 📈 Optimization Results

### Financial Summary
| Metric | Value |
| :--- | :--- |
| **Total Annual Cost** | **$959,466.05** |
| Fixed Costs (Amortized) | $60,500.00 |
| Annual Operational Costs | $545,000.00 |
| Transport Costs (Est.) | $353,966.05 |
| **Remaining Budget** | **$540,533.95** |

### Selected Warehouses
| Warehouse | Selected |
| :--- | :--- |
| **WH_NORTH** | **Yes** |
| **WH_SOUTH** | **Yes** |
| **WH_EAST** | No |

## 🛠️ Technologies Used
* **Python**: Core programming and logic.
* **PuLP**: Linear programming optimization engine.
* **Pandas**: Data structuring and manipulation.
* **GitHub**: Version control and documentation.

## 🏁 Conclusion
The MILP optimization model successfully identified the **North** and **South** warehouses as the most cost-effective hubs. This configuration meets all campus demands while utilizing only **64%** of the allocated budget, providing significant financial savings and operational scalability for the university.