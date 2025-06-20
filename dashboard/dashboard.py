import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import numpy as np

# Load environment variables
load_dotenv()

# Database connection parameters
db_params = {
    "dbname": os.getenv('PGDATABASE'),
    "user": os.getenv('PGUSER'),
    "password": os.getenv('PGPASSWORD'),
    "host": os.getenv('PGHOST'),
    "port": "5432"
}

def get_sqlalchemy_engine():
    """Creates SQLAlchemy engine for pandas operations"""
    connection_string = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
    return create_engine(connection_string)

def fetch_data():
    """Fetch all data from PostgreSQL database"""
    engine = get_sqlalchemy_engine()
    
    try:
        # Fetch attendance data
        attendance_query = '''
            SELECT "Date", "Department", "Employee", "Entry", "Exit"
            FROM icta.attendance
            ORDER BY "Date", "Employee"
        '''
        attendance_df = pd.read_sql(attendance_query, engine)
        
        # Fetch monthly aggregated data
        monthly_query = '''
            SELECT "Employee", "Department", "Month", "Delay", "Overtime", "Fine", "Bonus"
            FROM icta.monthly_fines_bonuses
            ORDER BY "Employee", "Month"
        '''
        monthly_df = pd.read_sql(monthly_query, engine)
        
        # Fetch processed data
        data_query = '''
            SELECT "Date", "Department", "Employee", "Adjusted_Work_Hours", "Overtime", "Delay"
            FROM icta.data
            ORDER BY "Date", "Employee"
        '''
        processed_df = pd.read_sql(data_query, engine)
        
        return attendance_df, monthly_df, processed_df
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        # Return empty dataframes as fallback
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    finally:
        engine.dispose()

def calculate_insights(monthly_df, processed_df):
    """Calculate meaningful business insights"""
    insights = {}
    
    if not monthly_df.empty:
        # Overall KPIs
        insights['total_employees'] = monthly_df['Employee'].nunique()
        insights['total_departments'] = monthly_df['Department'].nunique()
        insights['avg_overtime'] = monthly_df['Overtime'].mean()
        insights['avg_delay'] = monthly_df['Delay'].mean()
        insights['total_fines'] = monthly_df['Fine'].sum()
        insights['total_bonuses'] = monthly_df['Bonus'].sum()
        
        # Performance insights
        insights['top_performer'] = monthly_df.loc[monthly_df['Overtime'].idxmax(), 'Employee'] if len(monthly_df) > 0 else 'N/A'
        insights['most_delays'] = monthly_df.loc[monthly_df['Delay'].idxmax(), 'Employee'] if len(monthly_df) > 0 else 'N/A'
        insights['highest_bonus'] = monthly_df.loc[monthly_df['Bonus'].idxmax(), 'Employee'] if len(monthly_df) > 0 else 'N/A'
        insights['highest_fine'] = monthly_df.loc[monthly_df['Fine'].idxmax(), 'Employee'] if len(monthly_df) > 0 else 'N/A'
        
        # Department insights
        dept_stats = monthly_df.groupby('Department').agg({
            'Overtime': 'mean',
            'Delay': 'mean',
            'Fine': 'sum',
            'Bonus': 'sum'
        }).round(2)
        insights['dept_stats'] = dept_stats
        
        # Productivity score (overtime - delay)
        monthly_df['Productivity_Score'] = monthly_df['Overtime'] - monthly_df['Delay']
        insights['top_productive'] = monthly_df.loc[monthly_df['Productivity_Score'].idxmax(), 'Employee'] if len(monthly_df) > 0 else 'N/A'
        
    return insights

# Load data
attendance_df, monthly_df, processed_df = fetch_data()
insights = calculate_insights(monthly_df, processed_df)

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server  # For deployment

# Custom CSS styling
app.layout = html.Div([
    html.Div([
        html.H1("🏢 ICTA Employee Performance Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
        html.P("Real-time analytics powered by PostgreSQL database", 
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '16px'})
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'marginBottom': '20px'}),

    # KPI Cards
    html.Div([
        html.Div([
            html.H3(f"{insights.get('total_employees', 0)}", style={'color': '#3498db', 'margin': 0}),
            html.P("Total Employees", style={'margin': 0})
        ], className='kpi-card', style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1'}),
        
        html.Div([
            html.H3(f"{insights.get('avg_overtime', 0):.1f}h", style={'color': '#e74c3c', 'margin': 0}),
            html.P("Avg Overtime", style={'margin': 0})
        ], className='kpi-card', style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1'}),
        
        html.Div([
            html.H3(f"{insights.get('avg_delay', 0):.1f}h", style={'color': '#f39c12', 'margin': 0}),
            html.P("Avg Delays", style={'margin': 0})
        ], className='kpi-card', style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1'}),
        
        html.Div([
            html.H3(f"${insights.get('total_bonuses', 0):.0f}", style={'color': '#27ae60', 'margin': 0}),
            html.P("Total Bonuses", style={'margin': 0})
        ], className='kpi-card', style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1'})
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '30px'}),

    # Navigation Tabs
    dcc.Tabs(id="tabs", value='overview', children=[
        dcc.Tab(label='📊 Executive Overview', value='overview'),
        dcc.Tab(label='👥 Employee Analysis', value='employee_analysis'),
        dcc.Tab(label='🏢 Department Performance', value='department_performance'),
        dcc.Tab(label='💰 Financial Impact', value='financial_impact'),
        dcc.Tab(label='📈 Trends & Insights', value='trends_insights'),
    ], style={'marginBottom': '20px'}),

    html.Div(id='content')
], style={'fontFamily': 'Arial, sans-serif', 'margin': '0', 'padding': '20px'})

@app.callback(Output('content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    if monthly_df.empty:
        return html.Div([
            html.H3("⚠️ No Data Available", style={'color': '#e74c3c', 'textAlign': 'center'}),
            html.P("Please check database connection and ensure data is loaded.", style={'textAlign': 'center'})
        ])
    
    if tab == 'overview':
        return render_overview()
    elif tab == 'employee_analysis':
        return render_employee_analysis()
    elif tab == 'department_performance':
        return render_department_performance()
    elif tab == 'financial_impact':
        return render_financial_impact()
    elif tab == 'trends_insights':
        return render_trends_insights()

def render_overview():
    # Executive Summary Cards
    summary_cards = html.Div([
        html.H3("🎯 Executive Summary", style={'color': '#2c3e50', 'marginBottom': '20px'}),
        
        html.Div([
            html.Div([
                html.H4("🏆 Top Performer", style={'color': '#27ae60'}),
                html.P(f"{insights.get('top_performer', 'N/A')}", style={'fontSize': '18px', 'fontWeight': 'bold'}),
                html.P("Highest overtime hours", style={'color': '#7f8c8d'})
            ], style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'flex': '1'}),
            
            html.Div([
                html.H4("⚠️ Attention Needed", style={'color': '#e74c3c'}),
                html.P(f"{insights.get('most_delays', 'N/A')}", style={'fontSize': '18px', 'fontWeight': 'bold'}),
                html.P("Highest delay hours", style={'color': '#7f8c8d'})
            ], style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'flex': '1'}),
            
            html.Div([
                html.H4("💎 Most Productive", style={'color': '#3498db'}),
                html.P(f"{insights.get('top_productive', 'N/A')}", style={'fontSize': '18px', 'fontWeight': 'bold'}),
                html.P("Best overtime/delay ratio", style={'color': '#7f8c8d'})
            ], style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'flex': '1'})
        ], style={'display': 'flex', 'marginBottom': '30px'})
    ])
    
    # Performance Overview Charts
    fig1 = px.bar(
        monthly_df.groupby('Employee')['Overtime'].sum().reset_index().sort_values('Overtime', ascending=False),
        x='Employee', y='Overtime', 
        title='📊 Total Overtime by Employee',
        color='Overtime',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(showlegend=False)
    
    # Department comparison
    dept_comparison = monthly_df.groupby('Department').agg({
        'Overtime': 'mean',
        'Delay': 'mean'
    }).reset_index()
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name='Avg Overtime', x=dept_comparison['Department'], y=dept_comparison['Overtime'], marker_color='#3498db'))
    fig2.add_trace(go.Bar(name='Avg Delay', x=dept_comparison['Department'], y=dept_comparison['Delay'], marker_color='#e74c3c'))
    fig2.update_layout(title='🏢 Department Performance Comparison', barmode='group')
    
    return html.Div([
        summary_cards,
        html.Div([
            dcc.Graph(figure=fig1, style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(figure=fig2, style={'width': '50%', 'display': 'inline-block'})
        ])
    ])

def render_employee_analysis():
    # Employee performance metrics
    employee_stats = monthly_df.groupby('Employee').agg({
        'Overtime': ['sum', 'mean'],
        'Delay': ['sum', 'mean'],
        'Fine': 'sum',
        'Bonus': 'sum'
    }).round(2)
    employee_stats.columns = ['Total_Overtime', 'Avg_Overtime', 'Total_Delay', 'Avg_Delay', 'Total_Fine', 'Total_Bonus']
    employee_stats['Productivity_Score'] = employee_stats['Total_Overtime'] - employee_stats['Total_Delay']
    employee_stats = employee_stats.reset_index()
    
    # Performance scatter plot
    fig1 = px.scatter(
        employee_stats, x='Total_Overtime', y='Total_Delay', 
        size='Productivity_Score', color='Productivity_Score',
        hover_name='Employee',
        title='📈 Employee Performance Matrix (Overtime vs Delay)',
        labels={'Total_Overtime': 'Total Overtime (hours)', 'Total_Delay': 'Total Delay (hours)'},
        color_continuous_scale='RdYlGn'
    )
    
    # Top performers
    top_performers = employee_stats.nlargest(5, 'Productivity_Score')
    fig2 = px.bar(
        top_performers, x='Employee', y='Productivity_Score',
        title='🏆 Top 5 Most Productive Employees',
        color='Productivity_Score',
        color_continuous_scale='Greens'
    )
    
    # Employee performance table
    performance_table = dash_table.DataTable(
        data=employee_stats.to_dict('records'),
        columns=[
            {"name": "Employee", "id": "Employee"},
            {"name": "Total Overtime", "id": "Total_Overtime", "type": "numeric", "format": {"specifier": ".1f"}},
            {"name": "Total Delay", "id": "Total_Delay", "type": "numeric", "format": {"specifier": ".1f"}},
            {"name": "Productivity Score", "id": "Productivity_Score", "type": "numeric", "format": {"specifier": ".1f"}},
            {"name": "Total Bonus", "id": "Total_Bonus", "type": "numeric", "format": {"specifier": ".2f"}},
            {"name": "Total Fine", "id": "Total_Fine", "type": "numeric", "format": {"specifier": ".2f"}}
        ],
        style_cell={'textAlign': 'center'},
        style_data_conditional=[
            {
                'if': {'filter_query': '{Productivity_Score} > 10'},
                'backgroundColor': '#d5f4e6',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{Productivity_Score} < 0'},
                'backgroundColor': '#ffeaa7',
                'color': 'black',
            }
        ],
        sort_action="native"
    )
    
    return html.Div([
        html.H3("👥 Employee Performance Analysis"),
        html.Div([
            dcc.Graph(figure=fig1, style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(figure=fig2, style={'width': '50%', 'display': 'inline-block'})
        ]),
        html.H4("📋 Detailed Performance Metrics"),
        performance_table
    ])

def render_department_performance():
    # Department statistics
    dept_stats = insights.get('dept_stats', pd.DataFrame())
    
    if not dept_stats.empty:
        # Department performance radar chart
        fig1 = go.Figure()
        
        departments = dept_stats.index.tolist()
        metrics = ['Overtime', 'Delay', 'Bonus', 'Fine']
        
        for dept in departments:
            values = [
                dept_stats.loc[dept, 'Overtime'],
                dept_stats.loc[dept, 'Delay'],
                dept_stats.loc[dept, 'Bonus'] * 100,  # Scale for visibility
                dept_stats.loc[dept, 'Fine'] * 100   # Scale for visibility
            ]
            
            fig1.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics,
                fill='toself',
                name=dept
            ))
        
        fig1.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max([dept_stats['Overtime'].max(), dept_stats['Delay'].max()])])
            ),
            title="🔄 Department Performance Radar",
            showlegend=True
        )
        
        # Department efficiency
        dept_efficiency = dept_stats.copy()
        dept_efficiency['Efficiency'] = dept_efficiency['Overtime'] / (dept_efficiency['Delay'] + 1)  # +1 to avoid division by zero
        dept_efficiency = dept_efficiency.reset_index()
        
        fig2 = px.bar(
            dept_efficiency, x='Department', y='Efficiency',
            title='⚡ Department Efficiency Score',
            color='Efficiency',
            color_continuous_scale='Viridis'
        )
    else:
        fig1 = go.Figure()
        fig2 = go.Figure()
    
    return html.Div([
        html.H3("🏢 Department Performance Analysis"),
        html.Div([
            dcc.Graph(figure=fig1, style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(figure=fig2, style={'width': '50%', 'display': 'inline-block'})
        ])
    ])

def render_financial_impact():
    # Financial analysis
    financial_summary = monthly_df.groupby('Employee').agg({
        'Fine': 'sum',
        'Bonus': 'sum'
    }).reset_index()
    financial_summary['Net_Impact'] = financial_summary['Bonus'] - financial_summary['Fine']
    
    # Financial impact visualization
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='Bonuses', x=financial_summary['Employee'], y=financial_summary['Bonus'], marker_color='#27ae60'))
    fig1.add_trace(go.Bar(name='Fines', x=financial_summary['Employee'], y=financial_summary['Fine'], marker_color='#e74c3c'))
    fig1.update_layout(title='💰 Financial Impact by Employee', barmode='group')
    
    # Net financial impact
    fig2 = px.bar(
        financial_summary.sort_values('Net_Impact', ascending=True),
        x='Net_Impact', y='Employee',
        title='📊 Net Financial Impact (Bonus - Fine)',
        orientation='h',
        color='Net_Impact',
        color_continuous_scale='RdYlGn'
    )
    
    # Financial metrics
    total_bonuses = financial_summary['Bonus'].sum()
    total_fines = financial_summary['Fine'].sum()
    net_impact = total_bonuses - total_fines
    
    financial_cards = html.Div([
        html.Div([
            html.H4("💚 Total Bonuses", style={'color': '#27ae60'}),
            html.H2(f"${total_bonuses:.2f}", style={'margin': 0})
        ], style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'flex': '1', 'textAlign': 'center'}),
        
        html.Div([
            html.H4("💸 Total Fines", style={'color': '#e74c3c'}),
            html.H2(f"${total_fines:.2f}", style={'margin': 0})
        ], style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'flex': '1', 'textAlign': 'center'}),
        
        html.Div([
            html.H4("📈 Net Impact", style={'color': '#3498db'}),
            html.H2(f"${net_impact:.2f}", style={'margin': 0, 'color': '#27ae60' if net_impact > 0 else '#e74c3c'})
        ], style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'flex': '1', 'textAlign': 'center'})
    ], style={'display': 'flex', 'marginBottom': '30px'})
    
    return html.Div([
        html.H3("💰 Financial Impact Analysis"),
        financial_cards,
        html.Div([
            dcc.Graph(figure=fig1, style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(figure=fig2, style={'width': '50%', 'display': 'inline-block'})
        ])
    ])

def render_trends_insights():
    # Time series analysis if we have date information
    if not processed_df.empty and 'Date' in processed_df.columns:
        processed_df['Date'] = pd.to_datetime(processed_df['Date'])
        daily_trends = processed_df.groupby('Date').agg({
            'Overtime': 'mean',
            'Delay': 'mean'
        }).reset_index()
        
        fig1 = px.line(
            daily_trends, x='Date', y=['Overtime', 'Delay'],
            title='📈 Daily Trends - Overtime vs Delay',
            labels={'value': 'Hours', 'variable': 'Metric'}
        )
    else:
        fig1 = go.Figure()
        fig1.add_annotation(text="No trend data available", xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Insights and recommendations
    recommendations = []
    
    if insights.get('avg_delay', 0) > insights.get('avg_overtime', 0):
        recommendations.append("🔴 High delay rates detected. Consider reviewing attendance policies.")
    
    if insights.get('total_fines', 0) > insights.get('total_bonuses', 0):
        recommendations.append("💡 More fines than bonuses. Focus on employee development programs.")
    
    top_performer = insights.get('top_performer', 'N/A')
    if top_performer != 'N/A':
        recommendations.append(f"⭐ {top_performer} shows excellent performance. Consider for recognition/promotion.")
    
    insights_cards = html.Div([
        html.H4("🧠 AI-Powered Insights & Recommendations"),
        html.Ul([html.Li(rec) for rec in recommendations]) if recommendations else html.P("No specific recommendations at this time.")
    ], style={'backgroundColor': '#fff', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px'})
    
    return html.Div([
        html.H3("📈 Trends & Business Insights"),
        insights_cards,
        dcc.Graph(figure=fig1)
    ])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)