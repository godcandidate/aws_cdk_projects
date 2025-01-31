import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import psutil
import logging
from collections import deque
from datetime import datetime
import sys
import platform
import subprocess
from typing import Dict, List
import os
from assets.styles import *

# Set up basic logging to debug
logging.basicConfig(level=logging.INFO)

# Ensure the assets folder exists
assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
if not os.path.exists(assets_path):
    os.makedirs(assets_path)

# Initialize the Dash app with custom stylesheet and assets
app = dash.Dash(
    __name__,
    external_stylesheets=[
        'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    ],
    assets_folder=assets_path
)

# Initialize history deques
history = {
    'ram': deque(maxlen=20),
    'cpu': deque(maxlen=20),
    'disk': deque(maxlen=20),
    'time': deque(maxlen=20),
    'network_sent': deque(maxlen=20),
    'network_recv': deque(maxlen=20),
    'temp': deque(maxlen=20)
}

# Define color scheme
COLORS = {
    'background': '#1a1a1a',
    'text': '#ffffff',
    'ram': '#00ff00',
    'cpu': '#ff6b6b',
    'disk': '#4ecdc4',
    'card_bg': '#2d2d2d',
    'warning': '#ffd700',
    'critical': '#ff4444',
    'network_up': '#4CAF50',
    'network_down': '#2196F3'
}

# Define thresholds for alerts
THRESHOLDS = {
    'ram': {'warning': 70, 'critical': 85},
    'cpu': {'warning': 70, 'critical': 85},
    'disk': {'warning': 80, 'critical': 90},
}

def get_network_speed() -> Dict[str, float]:
    """Get current network speeds in MB/s"""
    net_io = psutil.net_io_counters()
    return {
        'sent': net_io.bytes_sent / 1024 / 1024,
        'recv': net_io.bytes_recv / 1024 / 1024
    }

def get_top_processes(n: int = 5) -> List[Dict]:
    """Get top n processes by CPU usage"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            processes.append({
                'pid': pinfo['pid'],
                'name': pinfo['name'],
                'cpu_percent': pinfo['cpu_percent'],
                'memory_percent': pinfo['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:n]

def get_cpu_temperature() -> float:
    """Get CPU temperature if available"""
    try:
        if platform.system() == 'Linux':
            temp = psutil.sensors_temperatures()
            if 'coretemp' in temp:
                return temp['coretemp'][0].current
        return None
    except:
        return None

def create_alert_card(title: str, value: float, warning: float, critical: float, unit: str = '%', icon: str = None):
    """Create an alert card with dynamic styling based on thresholds"""
    color = COLORS['text']
    icon_class = icon or 'fa-check'
    
    if unit == '%':
        if value >= critical:
            color = COLORS['critical']
            icon_class = 'fa-exclamation-triangle'
        elif value >= warning:
            color = COLORS['warning']
            icon_class = 'fa-exclamation'
    
    return html.Div([
        html.H3(title, style={'color': COLORS['text'], 'marginBottom': '10px'}),
        html.Div([
            html.I(className=f'fas {icon_class}', style={'marginRight': '10px', 'color': color}),
            html.Span(f'{value:.1f}{unit}', style={'color': color, 'fontSize': '24px', 'fontWeight': 'bold'})
        ])
    ], style={
        'backgroundColor': COLORS['card_bg'],
        'padding': '20px',
        'borderRadius': '10px',
        'flex': '1',
        'margin': '10px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'textAlign': 'center'
    })

def create_refresh_rate_slider():
    """Create a styled refresh rate slider"""
    return html.Div([
        html.Label('Refresh Rate (seconds): ', style={'color': COLORS['text'], 'marginRight': '10px'}),
        dcc.Slider(
            id='refresh-slider',
            min=1,
            max=10,
            value=5,
            marks={i: str(i) for i in range(1, 11)},
            step=1,
            className='slider'
        )
    ], style={
        'backgroundColor': COLORS['card_bg'],
        'padding': '20px',
        'borderRadius': '10px',
        'marginBottom': '20px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'display': 'flex',
        'alignItems': 'center',
        'width': '100%'
    })

# Function to get system statistics (RAM, CPU, and Disk)
def get_system_stats():
    try:
        # Get memory stats
        memory = psutil.virtual_memory()
        ram = memory.percent

        # Get CPU usage
        cpu = psutil.cpu_percent(interval=1)

        # Get Disk usage
        disk = psutil.disk_usage('/').percent

        # Return RAM, CPU, and Disk data
        return {
            'RAM Usage (%)': ram,
            'CPU Usage (%)': cpu,
            'Disk Usage (%)': disk
        }
    except Exception as e:
        logging.error(f"Error fetching system stats: {e}")
        return {}

# Determine whether to run in 'one' or 'multiple' mode based on command-line argument
mode = sys.argv[1] if len(sys.argv) > 1 else 'multiple'

if mode == 'one':
    app.layout = html.Div([
        html.Div([
            # Header
            html.H1('System Monitor Dashboard', style={
                'color': COLORS['text'],
                'textAlign': 'center',
                'fontFamily': 'Roboto',
                'marginBottom': '30px',
                'paddingTop': '20px'
            }),

            # Navigation
            html.Div([
                html.Div([
                    html.Div('System Resources', id='nav-resources', style={
                        'color': COLORS['text'],
                        'padding': '10px',
                        'borderRadius': '10px',
                        'cursor': 'pointer',
                        'marginRight': '10px',
                        'backgroundColor': COLORS['card_bg']
                    }),
                    html.Div('Network & Processes', id='nav-network', style={
                        'color': COLORS['text'],
                        'padding': '10px',
                        'borderRadius': '10px',
                        'cursor': 'pointer',
                        'marginRight': '10px',
                        'backgroundColor': COLORS['card_bg']
                    }),
                ], style={
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'marginBottom': '20px'
                })
            ]),

            # Content containers
            html.Div([
                # System Resources Page
                html.Div(id='resources-page', children=[
                    # Refresh rate slider
                    create_refresh_rate_slider(),
                    
                    # Stats cards container
                    html.Div(id='alert-cards', style={
                        'display': 'flex',
                        'flexWrap': 'wrap',
                        'justifyContent': 'space-between',
                        'marginBottom': '20px'
                    }),

                    # Graph container
                    html.Div([
                        dcc.Graph(
                            id='combined-graph',
                            config={'displayModeBar': False}
                        )
                    ], style={
                        'backgroundColor': COLORS['card_bg'],
                        'padding': '20px',
                        'borderRadius': '10px',
                        'marginBottom': '20px',
                        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
                    })
                ], style={'display': 'block'}),

                # Network & Processes Page
                html.Div(id='page-network', style={'display': 'none'}, children=[
                    # Network Stats
                    html.Div([
                        html.Div([
                            html.H3('Network Traffic', style={'color': COLORS['text'], 'marginBottom': '10px'}),
                            html.Div([
                                html.Div([
                                    html.I(className='fas fa-arrow-up', style={'color': COLORS['network_up'], 'marginRight': '5px'}),
                                    html.Span('Upload: ', style={'color': COLORS['text']}),
                                    html.Span(id='network-up', style={'color': COLORS['network_up']})
                                ], style={'marginBottom': '5px'}),
                                html.Div([
                                    html.I(className='fas fa-arrow-down', style={'color': COLORS['network_down'], 'marginRight': '5px'}),
                                    html.Span('Download: ', style={'color': COLORS['text']}),
                                    html.Span(id='network-down', style={'color': COLORS['network_down']})
                                ])
                            ])
                        ], style={
                            'backgroundColor': COLORS['card_bg'],
                            'padding': '20px',
                            'borderRadius': '10px',
                            'flex': '1',
                            'margin': '10px',
                            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                            'textAlign': 'center'
                        }),
                    ]),

                    # Top Processes
                    html.Div([
                        html.H3('Top Processes', style={'color': COLORS['text'], 'marginBottom': '10px'}),
                        html.Div(id='top-processes', style={
                            'backgroundColor': COLORS['card_bg'],
                            'padding': '20px',
                            'borderRadius': '10px',
                            'flex': '1',
                            'margin': '10px',
                            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                            'textAlign': 'center'
                        })
                    ]),
                ])
            ]),

            dcc.Interval(
                id='interval-component',
                interval=5*1000,
                n_intervals=0
            )
        ], style={
            'backgroundColor': COLORS['background'],
            'minHeight': '100vh',
            'padding': '20px'
        })
    ])

    @app.callback(
        [Output('nav-resources', 'style'),
         Output('nav-network', 'style'),
         Output('resources-page', 'style'),
         Output('page-network', 'style')],
        [Input('nav-resources', 'n_clicks'),
         Input('nav-network', 'n_clicks')]
    )
    def toggle_pages(res_clicks, net_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            # Default to resources page
            return {
                'color': COLORS['text'],
                'padding': '10px',
                'borderRadius': '10px',
                'cursor': 'pointer',
                'marginRight': '10px',
                'backgroundColor': COLORS['card_bg'],
                'border': '2px solid ' + COLORS['text']
            }, {
                'color': COLORS['text'],
                'padding': '10px',
                'borderRadius': '10px',
                'cursor': 'pointer',
                'marginRight': '10px',
                'backgroundColor': COLORS['card_bg']
            }, {'display': 'block'}, {'display': 'none'}
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'nav-resources':
            return {
                'color': COLORS['text'],
                'padding': '10px',
                'borderRadius': '10px',
                'cursor': 'pointer',
                'marginRight': '10px',
                'backgroundColor': COLORS['card_bg'],
                'border': '2px solid ' + COLORS['text']
            }, {
                'color': COLORS['text'],
                'padding': '10px',
                'borderRadius': '10px',
                'cursor': 'pointer',
                'marginRight': '10px',
                'backgroundColor': COLORS['card_bg']
            }, {'display': 'block'}, {'display': 'none'}
        else:
            return {
                'color': COLORS['text'],
                'padding': '10px',
                'borderRadius': '10px',
                'cursor': 'pointer',
                'marginRight': '10px',
                'backgroundColor': COLORS['card_bg']
            }, {
                'color': COLORS['text'],
                'padding': '10px',
                'borderRadius': '10px',
                'cursor': 'pointer',
                'marginRight': '10px',
                'backgroundColor': COLORS['card_bg'],
                'border': '2px solid ' + COLORS['text']
            }, {'display': 'none'}, {'display': 'block'}

    @app.callback(
        [Output('interval-component', 'interval')],
        [Input('refresh-slider', 'value')]
    )
    def update_interval(value):
        return [value * 1000]

    @app.callback(
        [Output('combined-graph', 'figure'),
         Output('alert-cards', 'children'),
         Output('network-up', 'children'),
         Output('network-down', 'children'),
         Output('top-processes', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_all(n):
        # Get system stats
        data = get_system_stats()
        if not data:
            return {}, [], '', '', []

        # Get temperature
        temp = get_cpu_temperature()
        
        # Create alert cards
        alert_cards = [
            create_alert_card('RAM Usage', data['RAM Usage (%)'], THRESHOLDS['ram']['warning'], THRESHOLDS['ram']['critical'], '%', 'fa-memory'),
            create_alert_card('CPU Usage', data['CPU Usage (%)'], THRESHOLDS['cpu']['warning'], THRESHOLDS['cpu']['critical'], '%', 'fa-microchip'),
            create_alert_card('Disk Usage', data['Disk Usage (%)'], THRESHOLDS['disk']['warning'], THRESHOLDS['disk']['critical'], '%', 'fa-hdd')
        ]
        
        # Add temperature card if available
        if temp is not None:
            alert_cards.append(
                create_alert_card('CPU Temp', temp, 70, 85, '°C', 'fa-thermometer-half')
            )

        # Get network stats
        net_stats = get_network_speed()
        network_up = f"{net_stats['sent']:.2f} MB/s"
        network_down = f"{net_stats['recv']:.2f} MB/s"

        # Get top processes
        processes = get_top_processes()
        process_list = html.Table([
            html.Thead(
                html.Tr([
                    html.Th('PID', style={
                        'color': COLORS['text'],
                        'textAlign': 'left',
                        'padding': '10px'
                    }),
                    html.Th('Process Name', style={
                        'color': COLORS['text'],
                        'textAlign': 'left',
                        'padding': '10px'
                    }),
                    html.Th('CPU Usage', style={
                        'color': COLORS['text'],
                        'textAlign': 'left',
                        'padding': '10px'
                    }),
                    html.Th('Memory Usage', style={
                        'color': COLORS['text'],
                        'textAlign': 'left',
                        'padding': '10px'
                    })
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(str(p['pid']), style={
                        'color': COLORS['text'],
                        'textAlign': 'left',
                        'padding': '10px'
                    }),
                    html.Td(p['name'][:40], style={
                        'color': COLORS['text'],
                        'textAlign': 'left',
                        'padding': '10px'
                    }),
                    html.Td(f"{p['cpu_percent']:>6.1f}%", style={
                        'color': COLORS['text'],
                        'textAlign': 'left',
                        'padding': '10px'
                    }),
                    html.Td(f"{p['memory_percent']:>6.1f}%", style={
                        'color': COLORS['text'],
                        'textAlign': 'left',
                        'padding': '10px'
                    })
                ], style={'backgroundColor': COLORS['card_bg'], 'transition': 'background-color 0.3s'},
                   className='process-row') for p in processes
            ])
        ], style={
            'backgroundColor': COLORS['card_bg'],
            'padding': '20px',
            'borderRadius': '10px',
            'flex': '1',
            'margin': '10px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'textAlign': 'center'
        })

        # Update history and create graph
        current_time = datetime.now().strftime('%H:%M:%S')
        history['ram'].append(data['RAM Usage (%)'])
        history['cpu'].append(data['CPU Usage (%)'])
        history['disk'].append(data['Disk Usage (%)'])
        history['time'].append(current_time)

        combined_figure = {
            'data': [
                go.Scatter(
                    x=list(history['time']),
                    y=list(history['ram']),
                    name='RAM',
                    line=dict(color=COLORS['ram'], width=3),
                    mode='lines+markers'
                ),
                go.Scatter(
                    x=list(history['time']),
                    y=list(history['cpu']),
                    name='CPU',
                    line=dict(color=COLORS['cpu'], width=3),
                    mode='lines+markers'
                ),
                go.Scatter(
                    x=list(history['time']),
                    y=list(history['disk']),
                    name='Disk',
                    line=dict(color=COLORS['disk'], width=3),
                    mode='lines+markers'
                )
            ],
            'layout': go.Layout(
                plot_bgcolor=COLORS['card_bg'],
                paper_bgcolor=COLORS['card_bg'],
                font={'color': COLORS['text']},
                title={
                    'text': 'System Resource Usage Over Time',
                    'font': {'size': 24, 'color': COLORS['text']},
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis={
                    'title': 'Time',
                    'gridcolor': '#444444',
                    'showgrid': True
                },
                yaxis={
                    'title': 'Usage (%)',
                    'range': [0, 100],
                    'gridcolor': '#444444',
                    'showgrid': True
                },
                margin={'l': 60, 'r': 40, 't': 80, 'b': 60},
                legend={
                    'bgcolor': COLORS['card_bg'],
                    'font': {'color': COLORS['text']},
                    'orientation': 'h',
                    'yanchor': 'bottom',
                    'y': 1.02,
                    'xanchor': 'right',
                    'x': 1
                },
                hovermode='x unified'
            )
        }

        return combined_figure, alert_cards, network_up, network_down, process_list

else:
    # Layout for multiple graphs (RAM, CPU, Disk each on its own graph)
    app.layout = html.Div([
        html.Div([
            html.H1('System Monitoring Dashboard', 
                style={
                    'color': COLORS['text'],
                    'textAlign': 'center',
                    'fontFamily': 'Roboto',
                    'marginBottom': '30px',
                    'paddingTop': '20px'
                }
            ),
            
            # Separate graphs container
            html.Div([
                dcc.Graph(id='ram-graph', style={'backgroundColor': COLORS['card_bg']}),
                dcc.Graph(id='cpu-graph', style={'backgroundColor': COLORS['card_bg']}),
                dcc.Graph(id='disk-graph', style={'backgroundColor': COLORS['card_bg']})
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))',
                'gap': '20px',
                'padding': '20px'
            }),

            dcc.Interval(
                id='interval-component',
                interval=5*1000,
                n_intervals=0
            )
        ], style={
            'backgroundColor': COLORS['background'],
            'minHeight': '100vh',
            'padding': '20px'
        })
    ])

    # Update callback to refresh the RAM, CPU, and Disk usage graphs every interval
    @app.callback(
        [Output('ram-graph', 'figure'),
         Output('cpu-graph', 'figure'),
         Output('disk-graph', 'figure')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_separate_graphs(n):
        # Fetch system stats (RAM, CPU, and Disk)
        data = get_system_stats()

        if not data:
            logging.info("No data fetched")
            return {}, {}, {}

        logging.info(f"Fetched data: {data}")

        # Append the current time, RAM, CPU, and Disk usage to history
        current_time = datetime.now().strftime('%H:%M:%S')  # Get the current time as a string
        history['ram'].append(data['RAM Usage (%)'])
        history['cpu'].append(data['CPU Usage (%)'])
        history['disk'].append(data['Disk Usage (%)'])
        history['time'].append(current_time)

        # Create RAM Usage Line Chart
        ram_figure = {
            'data': [go.Scatter(
                x=list(history['time']),
                y=list(history['ram']),
                name='RAM',
                line=dict(color=COLORS['ram'], width=3),
                mode='lines+markers'
            )],
            'layout': go.Layout(
                plot_bgcolor=COLORS['card_bg'],
                paper_bgcolor=COLORS['card_bg'],
                font={'color': COLORS['text']},
                title={
                    'text': 'RAM Usage Over Time',
                    'font': {'size': 18, 'color': COLORS['text']},
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis={
                    'title': 'Time',
                    'gridcolor': '#444444',
                    'showgrid': True
                },
                yaxis={
                    'title': 'Usage (%)',
                    'range': [0, 100],
                    'gridcolor': '#444444',
                    'showgrid': True
                },
                margin={'l': 60, 'r': 40, 't': 80, 'b': 60},
                legend={
                    'bgcolor': COLORS['card_bg'],
                    'font': {'color': COLORS['text']},
                    'orientation': 'h',
                    'yanchor': 'bottom',
                    'y': 1.02,
                    'xanchor': 'right',
                    'x': 1
                },
                hovermode='x unified'
            )
        }

        # Create CPU Usage Line Chart
        cpu_figure = {
            'data': [go.Scatter(
                x=list(history['time']),
                y=list(history['cpu']),
                name='CPU',
                line=dict(color=COLORS['cpu'], width=3),
                mode='lines+markers'
            )],
            'layout': go.Layout(
                plot_bgcolor=COLORS['card_bg'],
                paper_bgcolor=COLORS['card_bg'],
                font={'color': COLORS['text']},
                title={
                    'text': 'CPU Usage Over Time',
                    'font': {'size': 18, 'color': COLORS['text']},
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis={
                    'title': 'Time',
                    'gridcolor': '#444444',
                    'showgrid': True
                },
                yaxis={
                    'title': 'Usage (%)',
                    'range': [0, 100],
                    'gridcolor': '#444444',
                    'showgrid': True
                },
                margin={'l': 60, 'r': 40, 't': 80, 'b': 60},
                legend={
                    'bgcolor': COLORS['card_bg'],
                    'font': {'color': COLORS['text']},
                    'orientation': 'h',
                    'yanchor': 'bottom',
                    'y': 1.02,
                    'xanchor': 'right',
                    'x': 1
                },
                hovermode='x unified'
            )
        }

        # Create Disk Usage Line Chart
        disk_figure = {
            'data': [go.Scatter(
                x=list(history['time']),
                y=list(history['disk']),
                name='Disk',
                line=dict(color=COLORS['disk'], width=3),
                mode='lines+markers'
            )],
            'layout': go.Layout(
                plot_bgcolor=COLORS['card_bg'],
                paper_bgcolor=COLORS['card_bg'],
                font={'color': COLORS['text']},
                title={
                    'text': 'Disk Usage Over Time',
                    'font': {'size': 18, 'color': COLORS['text']},
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis={
                    'title': 'Time',
                    'gridcolor': '#444444',
                    'showgrid': True
                },
                yaxis={
                    'title': 'Usage (%)',
                    'range': [0, 100],
                    'gridcolor': '#444444',
                    'showgrid': True
                },
                margin={'l': 60, 'r': 40, 't': 80, 'b': 60},
                legend={
                    'bgcolor': COLORS['card_bg'],
                    'font': {'color': COLORS['text']},
                    'orientation': 'h',
                    'yanchor': 'bottom',
                    'y': 1.02,
                    'xanchor': 'right',
                    'x': 1
                },
                hovermode='x unified'
            )
        }

        return ram_figure, cpu_figure, disk_figure

# Run the app
# python app.py one 
# python app.py multiple
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)