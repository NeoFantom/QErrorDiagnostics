// Constants
const STAGE_COLORS = {
  'RO_resonator': '#FFD700',
  'qubit': '#90EE90',
  'two-qubit': '#87CEFA'
};

const GRAPH_LAYOUT = {
  name: 'dagre',
  rankDir: 'TB',
  nodeSep: 50,
  edgeSep: 10,
  spacingFactor: 1,
};

// Data loading
async function loadGraphData() {
  try {
    console.log('Attempting to load YAML file...');
    const response = await fetch('./calibration_experiments.yaml');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    console.log('YAML file fetched successfully');
    const yamlText = await response.text();
    console.log('YAML content:', yamlText.substring(0, 100) + '...' + '(omitted)'); // Show first 100 chars
    const yamlData = jsyaml.load(yamlText);
    console.log('YAML parsed successfully:', yamlData);

    const nodes = yamlData.experiments.map(exp => ({
      data: { id: exp.id, label: exp.name, stage: exp.stage }
    }));
    const edges = Object.entries(yamlData.graph)
      .flatMap(([source, targets]) => 
        targets.map(target => ({ data: { source, target } }))
      );

    return { nodes, edges, yamlData };
  } catch (err) {
    console.error('Error loading graph data:', err);
    console.error('Error details:', {
      message: err.message,
      stack: err.stack
    });
    throw err;
  }
}

// Tooltip generation
function generateTooltip(exp) {
  return Object.entries(exp)
    .filter(([key]) => key !== "id")
    .map(([key, value]) => {
      if (key === "procedure") value = "\n" + value;
      if (typeof value === "string" && !value.endsWith("\n\n")) {
        value += "\n\n";
      }
      return `**${key}**: ${value}`;
    })
    .join("\n\n");
}

// Popup handling
window.closePopup = function() {
  document.getElementById('popup').style.display = 'none';
}

function makePopupDraggable() {
  const popup = document.getElementById('popup');
  const header = document.getElementById('popup-header');
  let offsetX = 0, offsetY = 0, isDragging = false;

  header.onmousedown = startDragging;
  popup.addEventListener('mousedown', e => e.stopPropagation());

  function startDragging(e) {
    e.stopPropagation();
    e.preventDefault();
    isDragging = true;
    offsetX = e.clientX - popup.offsetLeft;
    offsetY = e.clientY - popup.offsetTop;
    
    document.onmousemove = onDrag;
    document.onmouseup = stopDragging;
  }

  function onDrag(e) {
    if (isDragging) {
      popup.style.left = `${e.clientX - offsetX}px`;
      popup.style.top = `${e.clientY - offsetY}px`;
    }
  }

  function stopDragging() {
    isDragging = false;
    document.onmousemove = null;
    document.onmouseup = null;
  }
}

// Legend creation
function createLegend() {
  const legend = document.getElementById('legend');
  Object.entries(STAGE_COLORS).forEach(([stage, color]) => {
    const item = document.createElement('div');
    item.className = 'legend-item';
    
    const colorBox = document.createElement('div');
    colorBox.className = 'color-box';
    colorBox.style.backgroundColor = color;
    
    const label = document.createElement('span');
    label.textContent = stage;
    
    item.appendChild(colorBox);
    item.appendChild(label);
    legend.appendChild(item);
  });
}

// Graph initialization
async function initializeGraph() {
  try {
    const { nodes, edges, yamlData } = await loadGraphData();
    const tooltipMap = yamlData.experiments.reduce((map, exp) => {
      map[exp.id] = generateTooltip(exp);
      return map;
    }, {});

    const cy = cytoscape({
      container: document.getElementById('cy'),
      elements: [...nodes, ...edges],
      layout: GRAPH_LAYOUT,
      wheelSensitivity: 0.2,
      style: [
        {
          selector: 'node',
          style: {
            shape: 'rectangle',
            label: 'data(label)',
            color: '#000',
            'font-size': '12px',
            'text-valign': 'center',
            'text-halign': 'center',
            'text-wrap': 'wrap',
            width: 'label',
            padding: '5px',
            'background-color': ele => STAGE_COLORS[ele.data('stage')] || '#ccc'
          }
        },
        {
          selector: 'edge',
          style: {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'line-color': '#ccc',
            'target-arrow-color': '#ccc'
          }
        }
      ]
    });

    cy.on('tap', 'node', evt => {
      const popup = document.getElementById('popup');
      const id = evt.target.id();
      document.getElementById('popup-content').innerHTML = 
        marked.parse(tooltipMap[id] || 'No information.');
      popup.style.display = 'block';
      popup.style.top = `${evt.originalEvent.clientY + 10}px`;
      popup.style.left = `${evt.originalEvent.clientX + 10}px`;
    });

    window.restoreLayout = () => cy.layout(GRAPH_LAYOUT).run();
    makePopupDraggable();
    createLegend();

  } catch (err) {
    console.error('Error initializing graph:', err);
    alert('Failed to load graph data. Please check the console for details.');
  }
}

// Initialize on load
console.log('Document loaded, initializing graph...');
document.addEventListener('DOMContentLoaded', initializeGraph);