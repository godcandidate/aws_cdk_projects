# Color scheme
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
    'network_down': '#2196F3',
    'nav_active': '#4a4a4a',
    'nav_hover': '#3a3a3a'
}

# Alert thresholds
THRESHOLDS = {
    'ram': {'warning': 70, 'critical': 85},
    'cpu': {'warning': 70, 'critical': 85},
    'disk': {'warning': 80, 'critical': 90},
}

# Common styles
CARD_STYLE = {
    'backgroundColor': COLORS['card_bg'],
    'padding': '20px',
    'borderRadius': '10px',
    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
    'marginBottom': '20px'
}

CONTAINER_STYLE = {
    'backgroundColor': COLORS['background'],
    'minHeight': '100vh',
    'padding': '20px'
}

HEADER_STYLE = {
    'color': COLORS['text'],
    'textAlign': 'center',
    'fontFamily': 'Roboto',
    'marginBottom': '30px',
    'paddingTop': '20px'
}

NAV_STYLE = {
    'display': 'flex',
    'justifyContent': 'center',
    'marginBottom': '30px',
    'backgroundColor': COLORS['card_bg'],
    'padding': '10px',
    'borderRadius': '10px'
}

NAV_ITEM_STYLE = {
    'padding': '10px 20px',
    'margin': '0 10px',
    'color': COLORS['text'],
    'cursor': 'pointer',
    'borderRadius': '5px',
    'transition': 'background-color 0.3s'
}

NAV_ITEM_ACTIVE = {
    **NAV_ITEM_STYLE,
    'backgroundColor': COLORS['nav_active']
}

GRAPH_STYLE = {
    'backgroundColor': COLORS['card_bg']
}

# Table styles
TABLE_STYLE = {
    'width': '100%',
    'borderCollapse': 'collapse',
    'color': COLORS['text'],
    'backgroundColor': COLORS['card_bg'],
    'borderRadius': '8px',
    'overflow': 'hidden',
    'tableLayout': 'fixed'
}

TABLE_HEADER_STYLE = {
    'backgroundColor': COLORS['nav_active'],
    'padding': '12px 15px',
    'fontSize': '16px',
    'fontWeight': 'bold',
    'color': COLORS['text'],
    'borderBottom': f'2px solid {COLORS["background"]}'
}

TABLE_HEADER_STYLES = {
    'pid': {
        **TABLE_HEADER_STYLE,
        'width': '15%',
        'textAlign': 'center'
    },
    'name': {
        **TABLE_HEADER_STYLE,
        'width': '45%',
        'textAlign': 'left'
    },
    'cpu': {
        **TABLE_HEADER_STYLE,
        'width': '20%',
        'textAlign': 'right',
        'paddingRight': '25px'
    },
    'memory': {
        **TABLE_HEADER_STYLE,
        'width': '20%',
        'textAlign': 'right',
        'paddingRight': '25px'
    }
}

TABLE_CELL_STYLE = {
    'padding': '12px 15px',
    'color': COLORS['text'],
    'borderBottom': f'1px solid {COLORS["nav_active"]}',
    'fontSize': '14px',
    'whiteSpace': 'nowrap',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis'
}

TABLE_COLUMN_STYLES = {
    'pid': {
        **TABLE_CELL_STYLE,
        'width': '15%',
        'textAlign': 'center'
    },
    'name': {
        **TABLE_CELL_STYLE,
        'width': '45%',
        'textAlign': 'left',
        'paddingRight': '10px'
    },
    'cpu': {
        **TABLE_CELL_STYLE,
        'width': '20%',
        'textAlign': 'right',
        'paddingRight': '25px',
        'fontFamily': 'monospace'
    },
    'memory': {
        **TABLE_CELL_STYLE,
        'width': '20%',
        'textAlign': 'right',
        'paddingRight': '25px',
        'fontFamily': 'monospace'
    }
}

TABLE_ROW_HOVER = {
    'backgroundColor': COLORS['nav_hover'],
    'transition': 'background-color 0.3s'
}

ALERT_CARD_STYLE = {
    **CARD_STYLE,
    'flex': '1',
    'margin': '10px',
    'textAlign': 'center'
}

SLIDER_CONTAINER_STYLE = {
    **CARD_STYLE,
    'marginBottom': '20px'
}
