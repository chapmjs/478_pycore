"""
Option A: Multi-Scenario Comparison
Python Shiny Core Version
"""

from shiny import App, ui, render, reactive
import plotly.graph_objects as go
from the_goal_optimization import create_goal_optimization_model

# UI Definition
app_ui = ui.page_fluid(
    # Custom CSS
    ui.tags.head(
        ui.tags.style("""
            .header-box {
                background-color: #1e3a8a;
                color: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 8px;
            }
            .scenario-card {
                border: 3px solid #94a3b8;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f8fafc;
            }
            .scenario-card.best {
                border-color: #16a34a;
            }
            .metric-box {
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
            }
            .throughput-box {
                background-color: #dbeafe;
            }
            .product-box {
                background-color: #dcfce7;
                color: #15803d;
            }
            .bottleneck-box {
                background-color: #fee2e2;
                color: #991b1b;
            }
            .insight-box {
                background-color: #dcfce7;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #16a34a;
                margin: 10px 0;
            }
        """)
    ),
    
    # Header
    ui.div(
        {"class": "header-box"},
        ui.h1("🏭 The Goal: Multi-Scenario Comparison"),
        ui.p("What Python Shiny Core Can Do That Excel Solver Cannot", style="font-style: italic;")
    ),
    
    # Info Panel
    ui.panel_well(
        ui.strong("💡 Why This Matters:"),
        " In Excel Solver, you can only solve ONE scenario at a time. "
        "To compare 3 different strategies, you'd need to manually solve each one, write down results, "
        "and create comparison charts yourself. Python Shiny solves all scenarios simultaneously and "
        "generates comparisons automatically!",
        style="background-color: #dbeafe; border-left: 4px solid #3b82f6;"
    ),
    
    # Layout
    ui.layout_sidebar(
        # Sidebar
        ui.panel_sidebar(
            ui.h3("📊 Configure Your Scenarios"),
            
            ui.input_radio_buttons(
                "selected_scenario",
                "Select Scenario to Edit:",
                choices={
                    "s1": "Scenario 1",
                    "s2": "Scenario 2",
                    "s3": "Scenario 3"
                },
                selected="s1"
            ),
            
            ui.hr(),
            
            # Scenario 1 inputs
            ui.panel_conditional(
                "input.selected_scenario === 's1'",
                ui.h4("Edit Scenario 1"),
                ui.input_text("name1", "Scenario Name:", value="Baseline"),
                ui.input_slider("heat1", "Heat Treatment (hrs):", min=80, max=240, value=160, step=10),
                ui.input_slider("mach1", "Machining (hrs):", min=100, max=300, value=200, step=10),
                ui.input_slider("assy1", "Assembly (hrs):", min=100, max=300, value=180, step=10),
                ui.input_slider("dema1", "Demand A:", min=0, max=100, value=50, step=5),
                ui.input_slider("demb1", "Demand B:", min=0, max=150, value=80, step=5),
                ui.input_slider("profa1", "Profit A ($):", min=50, max=150, value=90, step=5),
                ui.input_slider("profb1", "Profit B ($):", min=30, max=100, value=60, step=5)
            ),
            
            # Scenario 2 inputs
            ui.panel_conditional(
                "input.selected_scenario === 's2'",
                ui.h4("Edit Scenario 2"),
                ui.input_text("name2", "Scenario Name:", value="Elevate Bottleneck"),
                ui.input_slider("heat2", "Heat Treatment (hrs):", min=80, max=240, value=200, step=10),
                ui.input_slider("mach2", "Machining (hrs):", min=100, max=300, value=200, step=10),
                ui.input_slider("assy2", "Assembly (hrs):", min=100, max=300, value=180, step=10),
                ui.input_slider("dema2", "Demand A:", min=0, max=100, value=50, step=5),
                ui.input_slider("demb2", "Demand B:", min=0, max=150, value=80, step=5),
                ui.input_slider("profa2", "Profit A ($):", min=50, max=150, value=90, step=5),
                ui.input_slider("profb2", "Profit B ($):", min=30, max=100, value=60, step=5)
            ),
            
            # Scenario 3 inputs
            ui.panel_conditional(
                "input.selected_scenario === 's3'",
                ui.h4("Edit Scenario 3"),
                ui.input_text("name3", "Scenario Name:", value="Premium Product A"),
                ui.input_slider("heat3", "Heat Treatment (hrs):", min=80, max=240, value=160, step=10),
                ui.input_slider("mach3", "Machining (hrs):", min=100, max=300, value=200, step=10),
                ui.input_slider("assy3", "Assembly (hrs):", min=100, max=300, value=180, step=10),
                ui.input_slider("dema3", "Demand A:", min=0, max=100, value=50, step=5),
                ui.input_slider("demb3", "Demand B:", min=0, max=150, value=80, step=5),
                ui.input_slider("profa3", "Profit A ($):", min=50, max=150, value=140, step=5),
                ui.input_slider("profb3", "Profit B ($):", min=30, max=100, value=60, step=5)
            ),
            
            width=350
        ),
        
        # Main Panel
        ui.panel_main(
            ui.h2("📊 Scenario Comparison"),
            
            # Scenario Cards
            ui.row(
                ui.column(4, ui.output_ui("scenario1_card")),
                ui.column(4, ui.output_ui("scenario2_card")),
                ui.column(4, ui.output_ui("scenario3_card"))
            ),
            
            ui.hr(),
            
            ui.h2("📈 Visual Comparisons"),
            
            ui.row(
                ui.column(6, ui.output_ui("throughput_chart")),
                ui.column(6, ui.output_ui("product_mix_chart"))
            ),
            
            ui.hr(),
            
            ui.h2("💡 Automatic Insights & Recommendations"),
            
            ui.output_ui("insights"),
            
            ui.hr(),
            
            # Footer
            ui.panel_well(
                ui.p(
                    ui.strong("Why Python Shiny Core > Excel for This:"),
                    " Excel Solver requires manual solving of each scenario, separate worksheets, "
                    "manual comparison charts, and significant time. Python Shiny Core does it all "
                    "automatically in real-time!"
                ),
                ui.p(ui.em("Based on 'The Goal' by Eliyahu M. Goldratt")),
                style="text-align: center; color: #666;"
            )
        )
    )
)

# Server Logic
def server(input, output, session):
    
    # Reactive: Solve all scenarios
    @reactive.Calc
    def solve_scenarios():
        # Scenario 1
        result1, _ = create_goal_optimization_model(
            heat_treatment_capacity=input.heat1(),
            machining_capacity=input.mach1(),
            assembly_capacity=input.assy1(),
            demand_a=input.dema1(),
            demand_b=input.demb1(),
            profit_a=input.profa1(),
            profit_b=input.profb1()
        )
        result1['name'] = input.name1()
        
        # Scenario 2
        result2, _ = create_goal_optimization_model(
            heat_treatment_capacity=input.heat2(),
            machining_capacity=input.mach2(),
            assembly_capacity=input.assy2(),
            demand_a=input.dema2(),
            demand_b=input.demb2(),
            profit_a=input.profa2(),
            profit_b=input.profb2()
        )
        result2['name'] = input.name2()
        
        # Scenario 3
        result3, _ = create_goal_optimization_model(
            heat_treatment_capacity=input.heat3(),
            machining_capacity=input.mach3(),
            assembly_capacity=input.assy3(),
            demand_a=input.dema3(),
            demand_b=input.demb3(),
            profit_a=input.profa3(),
            profit_b=input.profb3()
        )
        result3['name'] = input.name3()
        
        return {'s1': result1, 's2': result2, 's3': result3}
    
    # Helper function to create scenario card HTML
    def create_scenario_card_html(result, is_best):
        border_color = "#16a34a" if is_best else "#94a3b8"
        badge = " 👑 BEST" if is_best else ""
        
        return f"""
        <div class="scenario-card" style="border-color: {border_color};">
            <h3 style="color: #1e3a8a;">{result['name']}{badge}</h3>
            <div class="metric-box throughput-box">
                <h4 style="color: #1e40af; margin: 0;">Throughput: ${result['total_throughput']:,.2f}</h4>
            </div>
            <div class="metric-box product-box">
                <p style="margin: 5px 0;"><strong>Product A:</strong> {result['product_a']:.1f} units</p>
                <p style="margin: 5px 0;"><strong>Product B:</strong> {result['product_b']:.1f} units</p>
            </div>
            <div class="metric-box bottleneck-box">
                <p style="margin: 5px 0;"><strong>Bottleneck:</strong> {result['bottleneck']}</p>
                <small>HT Utilization: {result['heat_treatment_utilization']:.1f}%</small>
            </div>
        </div>
        """
    
    # Render scenario cards
    @output
    @render.ui
    def scenario1_card():
        results = solve_scenarios()
        best_throughput = max(results['s1']['total_throughput'], 
                            results['s2']['total_throughput'], 
                            results['s3']['total_throughput'])
        is_best = results['s1']['total_throughput'] == best_throughput
        return ui.HTML(create_scenario_card_html(results['s1'], is_best))
    
    @output
    @render.ui
    def scenario2_card():
        results = solve_scenarios()
        best_throughput = max(results['s1']['total_throughput'], 
                            results['s2']['total_throughput'], 
                            results['s3']['total_throughput'])
        is_best = results['s2']['total_throughput'] == best_throughput
        return ui.HTML(create_scenario_card_html(results['s2'], is_best))
    
    @output
    @render.ui
    def scenario3_card():
        results = solve_scenarios()
        best_throughput = max(results['s1']['total_throughput'], 
                            results['s2']['total_throughput'], 
                            results['s3']['total_throughput'])
        is_best = results['s3']['total_throughput'] == best_throughput
        return ui.HTML(create_scenario_card_html(results['s3'], is_best))
    
    # Throughput comparison chart
    @output
    @render.ui
    def throughput_chart():
        results = solve_scenarios()
        
        names = [results['s1']['name'], results['s2']['name'], results['s3']['name']]
        throughputs = [results['s1']['total_throughput'], 
                      results['s2']['total_throughput'], 
                      results['s3']['total_throughput']]
        max_throughput = max(throughputs)
        colors = ['#16a34a' if t == max_throughput else '#3b82f6' for t in throughputs]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=names,
            y=throughputs,
            marker_color=colors,
            text=[f'${t:,.0f}' for t in throughputs],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Total Throughput Comparison",
            yaxis_title='Throughput ($)',
            showlegend=False,
            height=400
        )
        
        return ui.HTML(fig.to_html(include_plotlyjs='cdn', div_id='throughput_plot'))
    
    # Product mix chart
    @output
    @render.ui
    def product_mix_chart():
        results = solve_scenarios()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name=results['s1']['name'],
            x=['Product A', 'Product B'],
            y=[results['s1']['product_a'], results['s1']['product_b']]
        ))
        
        fig.add_trace(go.Bar(
            name=results['s2']['name'],
            x=['Product A', 'Product B'],
            y=[results['s2']['product_a'], results['s2']['product_b']]
        ))
        
        fig.add_trace(go.Bar(
            name=results['s3']['name'],
            x=['Product A', 'Product B'],
            y=[results['s3']['product_a'], results['s3']['product_b']]
        ))
        
        fig.update_layout(
            title="Product Mix Comparison",
            yaxis_title='Units Produced',
            barmode='group',
            height=400
        )
        
        return ui.HTML(fig.to_html(include_plotlyjs='cdn', div_id='product_mix_plot'))
    
    # Insights
    @output
    @render.ui
    def insights():
        results = solve_scenarios()
        
        # Find best scenario
        throughputs = [results['s1']['total_throughput'], 
                      results['s2']['total_throughput'], 
                      results['s3']['total_throughput']]
        best_idx = throughputs.index(max(throughputs))
        scenario_keys = ['s1', 's2', 's3']
        best_result = results[scenario_keys[best_idx]]
        best_name = best_result['name']
        
        # Calculate improvement
        baseline_throughput = results['s1']['total_throughput']
        best_throughput = best_result['total_throughput']
        improvement = best_throughput - baseline_throughput
        improvement_pct = (improvement / baseline_throughput) * 100 if baseline_throughput > 0 else 0
        
        insights_html = f"""
        <div class="insight-box">
            <strong>Best Scenario:</strong> {best_name} achieves the highest throughput at ${best_throughput:,.2f}
        </div>
        """
        
        if best_idx != 0:
            insights_html += f"""
            <div class="insight-box">
                <strong>Improvement:</strong> {best_name} produces ${improvement:,.2f} ({improvement_pct:.1f}%) more than the baseline
            </div>
            """
        
        # Bottleneck insights
        bottlenecks = [results['s1']['bottleneck'], results['s2']['bottleneck'], results['s3']['bottleneck']]
        unique_bottlenecks = list(set(bottlenecks))
        
        if len(unique_bottlenecks) > 1:
            insights_html += f"""
            <div style="background-color: #dbeafe; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; margin: 10px 0;">
                <strong>Bottleneck Shift:</strong> The constraint changes across scenarios: {', '.join(unique_bottlenecks)}
            </div>
            """
        else:
            insights_html += f"""
            <div style="background-color: #dbeafe; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; margin: 10px 0;">
                <strong>Consistent Bottleneck:</strong> {unique_bottlenecks[0]} remains the constraint across all scenarios
            </div>
            """
        
        return ui.HTML(insights_html)

# Create the app
app = App(app_ui, server)
