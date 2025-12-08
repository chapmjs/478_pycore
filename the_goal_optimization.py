"""
The Goal - Production Scheduling Optimization Exercise
Based on Eliyahu Goldratt's Theory of Constraints

Scenario:
Alex Rogo's plant produces two product families (similar to the book's scenario):
- Product A: Higher profit margin ($90/unit), requires more processing time
- Product B: Lower profit margin ($60/unit), requires less processing time

The plant has three work centers that mirror the book's concepts:
1. Machining Center (like the NCX-10 machines)
2. Heat Treatment (the bottleneck - like Herbie on the hike)
3. Assembly (post-bottleneck operations)

Each product requires different amounts of time at each work center.
Your goal: Maximize throughput (revenue) while respecting capacity constraints.
"""

from pulp import *
import pandas as pd

def create_goal_optimization_model(
    heat_treatment_capacity=160,  # Hours per week - THE BOTTLENECK
    machining_capacity=200,       # Hours per week
    assembly_capacity=180,        # Hours per week
    demand_a=50,                  # Maximum demand for Product A
    demand_b=80,                  # Maximum demand for Product B
    profit_a=90,                  # Profit per unit of Product A
    profit_b=60                   # Profit per unit of Product B
):
    """
    Create and solve the production optimization model.
    
    Key insight from The Goal: The bottleneck (Heat Treatment) determines
    the throughput of the entire system!
    """
    
    # Create the model
    model = LpProblem("The_Goal_Production_Scheduling", LpMaximize)
    
    # Decision variables
    product_a = LpVariable("Product_A", lowBound=0, cat='Continuous')
    product_b = LpVariable("Product_B", lowBound=0, cat='Continuous')
    
    # Objective function: Maximize throughput (profit)
    # Remember Goldratt's definition: Throughput = rate of generating money through sales
    model += profit_a * product_a + profit_b * product_b, "Total_Throughput"
    
    # Processing times (hours per unit)
    machining_time = {"A": 2.5, "B": 1.5}
    heat_treatment_time = {"A": 4.0, "B": 2.0}  # Bottleneck!
    assembly_time = {"A": 2.0, "B": 1.5}
    
    # Constraints
    # 1. Machining capacity constraint
    model += (machining_time["A"] * product_a + 
              machining_time["B"] * product_b <= machining_capacity), "Machining_Capacity"
    
    # 2. Heat Treatment capacity constraint (THE BOTTLENECK)
    # As Jonah would say: "An hour lost at the bottleneck is an hour lost for the entire system"
    model += (heat_treatment_time["A"] * product_a + 
              heat_treatment_time["B"] * product_b <= heat_treatment_capacity), "Heat_Treatment_Capacity_BOTTLENECK"
    
    # 3. Assembly capacity constraint
    model += (assembly_time["A"] * product_a + 
              assembly_time["B"] * product_b <= assembly_capacity), "Assembly_Capacity"
    
    # 4. Demand constraints
    model += product_a <= demand_a, "Demand_Limit_A"
    model += product_b <= demand_b, "Demand_Limit_B"
    
    # Solve the model
    model.solve(PULP_CBC_CMD(msg=0))
    
    # Prepare results
    results = {
        "status": LpStatus[model.status],
        "product_a": value(product_a),
        "product_b": value(product_b),
        "total_throughput": value(model.objective),
        "machining_used": machining_time["A"] * value(product_a) + machining_time["B"] * value(product_b),
        "machining_capacity": machining_capacity,
        "heat_treatment_used": heat_treatment_time["A"] * value(product_a) + heat_treatment_time["B"] * value(product_b),
        "heat_treatment_capacity": heat_treatment_capacity,
        "assembly_used": assembly_time["A"] * value(product_a) + assembly_time["B"] * value(product_b),
        "assembly_capacity": assembly_capacity,
    }
    
    # Calculate utilization percentages
    results["machining_utilization"] = (results["machining_used"] / machining_capacity) * 100
    results["heat_treatment_utilization"] = (results["heat_treatment_used"] / heat_treatment_capacity) * 100
    results["assembly_utilization"] = (results["assembly_used"] / assembly_capacity) * 100
    
    # Identify the binding constraint (actual bottleneck)
    results["bottleneck"] = "Heat Treatment" if results["heat_treatment_utilization"] >= 99.9 else \
                           "Machining" if results["machining_utilization"] >= 99.9 else \
                           "Assembly" if results["assembly_utilization"] >= 99.9 else \
                           "Demand"
    
    # Calculate constraint shadow prices (dual values)
    constraints_data = []
    for name, constraint in model.constraints.items():
        constraints_data.append({
            "Constraint": name,
            "Shadow_Price": constraint.pi,
            "Slack": constraint.slack
        })
    results["constraints_df"] = pd.DataFrame(constraints_data)
    
    return results, model


def format_results(results):
    """Format results for display."""
    output = []
    output.append("="*60)
    output.append("THE GOAL - PRODUCTION OPTIMIZATION RESULTS")
    output.append("="*60)
    output.append(f"\nOptimization Status: {results['status']}")
    output.append(f"\nOptimal Production Plan:")
    output.append(f"  Product A: {results['product_a']:.2f} units")
    output.append(f"  Product B: {results['product_b']:.2f} units")
    output.append(f"\nMaximum Throughput (Profit): ${results['total_throughput']:,.2f}")
    
    output.append(f"\n{'─'*60}")
    output.append("RESOURCE UTILIZATION (Theory of Constraints Analysis)")
    output.append(f"{'─'*60}")
    
    output.append(f"\nMachining Center:")
    output.append(f"  Used: {results['machining_used']:.2f} / {results['machining_capacity']:.2f} hours")
    output.append(f"  Utilization: {results['machining_utilization']:.1f}%")
    
    output.append(f"\nHeat Treatment (Expected Bottleneck):")
    output.append(f"  Used: {results['heat_treatment_used']:.2f} / {results['heat_treatment_capacity']:.2f} hours")
    output.append(f"  Utilization: {results['heat_treatment_utilization']:.1f}%")
    
    output.append(f"\nAssembly Center:")
    output.append(f"  Used: {results['assembly_used']:.2f} / {results['assembly_capacity']:.2f} hours")
    output.append(f"  Utilization: {results['assembly_utilization']:.1f}%")
    
    output.append(f"\n{'─'*60}")
    output.append(f"ACTUAL BOTTLENECK: {results['bottleneck']}")
    output.append(f"{'─'*60}")
    
    output.append("\nKey Insight from The Goal:")
    if results['bottleneck'] == "Heat Treatment":
        output.append("  'An hour lost at the bottleneck is an hour lost for the entire system.'")
        output.append(f"  Every additional hour at Heat Treatment is worth $X to the system.")
    
    output.append("\n" + "="*60)
    
    return "\n".join(output)


if __name__ == "__main__":
    # Solve with default parameters
    results, model = create_goal_optimization_model()
    print(format_results(results))
    print("\nConstraint Analysis:")
    print(results["constraints_df"].to_string(index=False))
