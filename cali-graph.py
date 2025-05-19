# Load the YAML data
import yaml
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import time

# Load the Dagre layout plugin
cyto.load_extra_layouts()

# === CONSTANTS ===
# YAML file path
YAML_FILE = "calibration_experiments.yaml"

# Node colors based on stage
STAGE_COLOR_MAP = {
    "RO_resonator": "#FFD700",  # Soft yellow (Gold)
    "qubit": "#90EE90",        # Light green
    "1qb_gate": "#87CEFA"      # Light blue (Sky Blue)
}

# === HELPER FUNCTIONS ===
def load_yaml(file_path):
    """
    Load YAML data from the specified file path.
    """
    with open(file_path, "r", encoding='utf8') as file:
        return yaml.safe_load(file)

def generate_tooltip(exp):
    """
    Generate a tooltip for a given experiment.
    Ensures each value ends with two newlines and prepends a newline for 'procedure'.
    """
    tooltip = []
    for k, v in exp.items():
        if k == "id":
            continue
        if k == "procedure":
            v = f"\n{v}"  # Prepend a newline for 'procedure'
        if isinstance(v, str) and not v.endswith("\n\n"):
            v += "\n\n"  # Ensure it ends with two newlines
        tooltip.append(f"**{k}**: {v}")
    return "\n\n".join(tooltip)

def generate_stylesheet(stage_color_map):
    """
    Generate a Cytoscape stylesheet based on the stage-color mapping.
    """
    stylesheet = []
    
    # Add styles for each stage
    for stage, color in stage_color_map.items():
        stylesheet.append({
            'selector': f'node[stage = "{stage}"]',
            'style': {
                'background-color': color,
            }
        })
    
    # Add default node and edge styles
    stylesheet.extend([
        {
            'selector': 'node',
            'style': {
                'shape': 'rectangle',
                'label': 'data(label)',
                'color': '#000',
                'font-size': '12px',
                'text-valign': 'center',
                'text-halign': 'center',
                'text-wrap': 'wrap',
                'width': 'label',
                'padding': '5px'
            }
        },
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'line-color': '#ccc',
                'target-arrow-color': '#ccc'
            }
        }
    ])
    return stylesheet

def get_dagre_layout():
    """
    Define the default Dagre layout with top-to-bottom rank direction.
    """
    return {
        'name': 'dagre',
        'rankDir': 'TB',        # top-to-bottom
        'nodeSep': 50,          # spacing between nodes
        'edgeSep': 10,          # spacing between edges
        'spacingFactor': 1.2,   # overall spacing
        'animate': True,
        'refresh': time.time()
    }

# === MAIN SCRIPT ===
if __name__ == '__main__':
    # Load YAML data
    data = load_yaml(YAML_FILE)

    # Create Cytoscape elements
    elements = []
    tooltip_map = {}
    for exp in data["experiments"]:
        exp_id = exp["id"]
        elements.append({
            'data': {
                'id': exp_id,
                'label': exp.get('name', 'exp_id'),
                'stage': exp.get('stage', 'unknown')  # Add stage to node data
            }
        })
        tooltip_map[exp_id] = generate_tooltip(exp)

    for parent, children in data["graph"].items():
        for child in children:
            elements.append({'data': {'source': parent, 'target': child}})

    # Generate the stylesheet dynamically
    stylesheet = generate_stylesheet(STAGE_COLOR_MAP)

    # Initialize Dash app
    app = dash.Dash(__name__)

    # App layout with bordered container and popup div using CSS classes instead of inline styles
    graph_container = html.Div([
        html.Div([
            cyto.Cytoscape(
                id='cytoscape-graph',
                layout=get_dagre_layout(),
                className='cytoscape-style',  # using external CSS
                elements=elements,
                stylesheet=stylesheet
            ),
            html.Div(id='popup', className='popup-style')
        ], className='graph-container'),
        html.Div([
            html.Button(
                "Restore Layout",
                id="restore-layout",
                n_clicks=0,
                className='restore-button-style'
            )
        ], style={'textAlign': 'center', 'width': '100%', 'marginTop': '20px'}),
    ])
    app.layout = graph_container

    # Callback to display popup content on node click
    @app.callback(
        Output('popup', 'children'),
        Output('popup', 'style'),
        Input('cytoscape-graph', 'tapNodeData')
    )
    def display_popup(data):
        if not data:
            return '', {}  # let CSS handle the hiding if necessary
        node_id = data['id']
        content = tooltip_map[node_id]
        return dcc.Markdown(content), {}

    # Callback to restore graph layout to Dagre default
    @app.callback(
        Output('cytoscape-graph', 'layout'),
        Input('restore-layout', 'n_clicks')
    )
    def restore_layout(n):
        return get_dagre_layout()

    # Run the app
    app.run(debug=True, port=8051, host='0.0.0.0')