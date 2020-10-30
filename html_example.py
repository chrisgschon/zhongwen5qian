from IPython.core.display import display, HTML, Javascript
from string import Template
import json

FILE = {'centrality':'data_degree_centrality.json', 'louvain':'data_louvain.json'}

# Select the file you want to visualise
with open(f"../data/{FILE['centrality']}") as json_file:
    data = json.load(json_file)

# Transform the graph into a JSON graph
jsonGraph = json.dumps(data, indent=4)

# Send to Javascript
Javascript("""window.jsonGraph={};""".format(jsonGraph))

# <script src='https://visjs.github.io/vis-network/standalone/umd/vis-network.min.js'></script>
# <div id="mynetwork"></div>
# <script>
#     // create a network
#     var container = document.getElementById('mynetwork');
#     var options = {
#         width: '1600px',
#         height: '1200px',
#       interaction: {
#         dragView : true
#       },
#       nodes: {
#         shape: "circle",
#         scaling: {
#           min: 1,
#           max: 15,
#             label: {
#                 enabled :true,
#                 min: 4,
#                 max:15
#             }
#         },
#         font: {
#             size:10
#         }
#       },
#       edges: {
#         color: {
#           opacity: 0.7  
#         },
#         arrows: {
#           to: {
#               enabled:true,
#               scaleFactor :0.5
#           }  
#         },
#         scaling:{
#           min: 1,
#           max: 15,
#           label: {
#             enabled: false,
#       },
#         font: {
#             size:0
#         }
#       }
#     }}
#         ;
    
#     // We load the JSON graph we generated from iPython input
#     var graph = window.jsonGraph;
    
#     // Display Graph
#     var network = new vis.Network(container, graph, options);
# </script>
