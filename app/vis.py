from neo import NeoGraph
from db import Db

g = NeoGraph()

import json
import argparse

from IPython.core.display import display, HTML, Javascript

# Select the file you want to visualise
with open(f"shang4.json") as json_file:
    data = json.load(json_file)

# Transform the graph into a JSON graph
jsonGraph = json.dumps(data, indent=4)

# Send to Javascript
Javascript("""window.jsonGraph={};""".format(jsonGraph))

def generate_vis_json_from_char(char):

    out_links = g.run_query(f"""match path = (source:Character)-[link:WORD]->(target:Character)
    where source.strokes = '{char}'
    return source,link,target""")

    in_links = g.run_query(f"""match path = (target:Character)<-[link:WORD]-(source:Character)
    where target.strokes = '{char}'
    return source,link,target""")

    root_node = g.run_query(f"""match (n:Character)
    where n.strokes = '{char}'
    return distinct n""")

    connected_nodes = g.run_query(f"""MATCH (n {{strokes : '{char}'}})-[:WORD]-(connected)
    RETURN distinct connected""")

    nodes = [node['n'] for node in root_node]  + [node['connected'] for node in connected_nodes]

    nodesj = json.loads(json.dumps(nodes))

    nodes_plt = nodesj.copy()

    for x in nodes_plt:
        x['id'] = x.pop('strokes')
        x['label'] = x.get('id')
        x.pop('descr', None)

    nodes_out = nodes_plt.copy()

    linksj = json.loads(json.dumps(out_links)) + json.loads(json.dumps(in_links))

    links_plt = []

    for link in linksj:
        links_plt.append({'from':link['source']['strokes'], 'to':link['target']['strokes'], 'label' : link['link']['descr']})

    out = {'nodes':nodes_out, 'edges':links_plt}

    with open(f'./assets/chars/{char}.json', 'w') as outfile:
        json.dump(out, outfile)


def generate_html_from_json(char):

    with open(f"./assets/chars/{char}.json") as json_file:
        data = json.load(json_file)

    jsonGraph = json.dumps(data, indent=4)

    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>JavaScript Network Graph</title>
        <style>
        html, body, #container {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
        }
        </style>
    </head>
    <body>
        <div id="container"></div>
    <script src='https://visjs.github.io/vis-network/standalone/umd/vis-network.min.js'></script>
    <div id="mynetwork"></div>
    <script>
        var container = document.getElementById('mynetwork');
        var options = { width : '800px', height : '600px',
        "edges": {
            "arrows": {
            "to": {
                "enabled": true,
                "scaleFactor": 0.7
            }
            },
            "color": {
            "opacity": 0.4
            },
            "font": {
            "size": 7,
            "face": "verdana",
            "align": "top"
            },
            "selfReferenceSize": null,
            "selfReference": {
            "angle": 0.7853981633974483
            },
            "smooth": {
            "forceDirection": "none"
            }
        },
        "physics": {
            "minVelocity": 0.75
        }
        }
                ;
        
        var json = $.getJSON("./assets/chars/{char}.json").done(function(data){
    var data = {
      nodes: data.nodes,
      edges: data.edges
    };
        
        var network = new vis.Network(container, data, options);
    </script>
    </body>
    </html>
    """.replace('{char}', char)

    print(html)

    print

    with open(f'./assets/html/{char}.html', 'w') as outfile:
        outfile.write(html)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--char",
        required=False,
        default='上',
        help="Generate character and connected character json artefacts",
    )

    args = parser.parse_args()
    generate_vis_json_from_char(args.char)
    generate_html_from_json(args.char)

if __name__=='__main__':
    main()
