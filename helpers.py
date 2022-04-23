
import networkx as nx
import pickle
import chart_studio.plotly as py
import random
import plotly
from plotly.graph_objs import *
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, plot, iplot
import json
init_notebook_mode(connected=True)

map_towns = {
	0: {'pos': (34.7541761, -0.1029109), 'connections': [1,2,3]}, 
 	1: {'pos': (35.2833, -0.3666), 'connections': [0,3,4]},
	2: {'pos': (35.2715481, 0.5198329), 'connections': [0,3,9]}, 
	3: {'pos': (36.0712048, -0.2802724), 'connections': [0,1,2,4,5]}, 
	4: {'pos': (35.47742284932569, -1.2779365500000002), 'connections': [1,3,5]}, 
	5: {'pos': (36.826061224105075, -1.3031689499999999),'connections': [3,4,7]}, 
	6: {'pos': (36.9517005, -0.4192962), 'connections': [7,9]}, 
	7: {'pos': (37.077523, -1.036648), 'connections': [5,6,8]}, 
	8: {'pos': (37.4583949, -0.5376699), 'connections': [7,9]}, 
	9: {'pos': (37.583303,0.35), 'connections': [2,6,8]} 

}

class Map:
	def __init__(self, G):
		self._graph = G
		self.intersections = nx.get_node_attributes(G, "pos")
		self.roads = [list(G[node ]) for node in G.nodes()]
		self.actual_distances = nx.get_edge_attributes(G, 'weight')
		self.actual_distances[(1,0)] = 66
		self.actual_distances[(2,0)] = 90
		self.actual_distances[(3,0)] = 148
		self.actual_distances[(3,1)] = 88
		self.actual_distances[(4,1)] = 103
		self.actual_distances[(3,2)] = 126 
		self.actual_distances[(9,2)] = 391
		self.actual_distances[(4,3)] = 391
		self.actual_distances[(5,3)] = 141
		self.actual_distances[(5,4)] = 150 
		self.actual_distances[(7,5)] = 41
		self.actual_distances[(7,6)] = 70  
		self.actual_distances[(9,6)] = 255 
		self.actual_distances[(8,7)] = 60
		self.actual_distances[(9,8)] = 268 


	def save(self, filename):
		with open(filename, 'wb') as f:
			pickle.dump(self._graph, f)

def load_map_graph(map_dict):
	G = nx.Graph()
	for node in map_dict.keys():
		G.add_node(node, pos=map_dict[node]['pos'])
	for node in map_dict.keys():
		for con_node in map_dict[node]['connections']:
			G.add_edge(node, con_node)
	return G

def load_map_towns():
    G = load_map_graph(map_towns)
    towns = {0:{'Town':'Kisumu'},1:{'Town':'Kericho'},2:{'Town':'Eldoret'},3:{'Town':'Nakuru'},4:{'Town':'Narok'},5:{'Town':'Nairobi'},6:{'Town':'Nyeri'},7:{'Town':'Thika'},8:{'Town':'Embu'},9:{'Town':'Isiolo'}}
#     distances = {(0,1):{'Distance':66},(0,2):{'Distance':90},(0,3):{'Distance':148},(1,3):{'Distance':88},(1,4):{'Distance':103},(2,3):{'Distance':126},(2,9):{'Distance':391},(3,4):{'Distance':129},(3,5):{'Distance':141},(4,5):{'Distance':150},(5,7):{'Distance':41},(6,7):{'Distance':70},(6,9):{'Distance':255},(7,8):{'Distance':60},(8,9):{'Distance':268}}
    nx.set_node_attributes(G, towns)
    #x.set_edge_attributes(G, distances)
    
    G[0][1]['weight'] = 66
    G[0][2]['weight'] = 90
    G[0][3]['weight'] = 148
    G[1][3]['weight'] = 88
    G[1][4]['weight'] = 103 
    G[2][3]['weight'] = 126
    G[2][9]['weight'] = 391
    G[3][4]['weight'] = 129
    G[3][5]['weight'] = 141
    G[4][5]['weight'] = 150
    G[5][7]['weight'] = 41
    G[6][7]['weight'] = 70
    G[6][9]['weight'] = 255
    G[7][8]['weight'] = 60
    G[8][9]['weight'] = 268
            
    return Map(G)


def show_map(M, start=None, goal=None, path=None):
    G = M._graph
    pos = nx.get_node_attributes(G, 'pos')
    towns = nx.get_node_attributes(G,'Town')
    actual_distances = nx.get_edge_attributes(G, 'weight')
    actual_distances[(1,0)] = 66 
    actual_distances[(2,0)] = 90
    actual_distances[(3,0)] = 148 
    actual_distances[(4,1)] = 103
    actual_distances[(3,1)] = 88
    actual_distances[(3,2)] = 126 
    actual_distances[(9,2)] = 391 
    actual_distances[(4,3)] = 129 
    actual_distances[(5,3)] = 141 
    actual_distances[(5,4)] = 150 
    actual_distances[(7,5)] = 41 
    actual_distances[(7,6)] = 70 
    actual_distances[(9,6)] = 255 
    actual_distances[(8,7)] = 60 
    actual_distances[(9,8)] = 268 
        
    etext = [w for w in list(nx.get_edge_attributes(G, 'weight').values())]
    ntext = [w for w in list(nx.get_edge_attributes(G, 'towns').values())]

           
    edge_x = []
    edge_y = []
    xtext=[]
    ytext=[]
    
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        xtext.append((x0+x1)/2)
        ytext.append((y0+y1)/2)
        
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.0, color='#888'),
        hoverinfo='none',
        text = etext,
        mode='lines'
    )
    eweights_trace = go.Scatter(x=xtext, y= ytext, 
                            mode='text',
                            marker_size=0.5,
                            textposition='top center',
                            text=etext,
                            hovertemplate='Distance: %{text}<extra></extra>'
                            )
    
    node_x = []
    node_y = []
    
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        town = G.nodes[node]['Town']
        node_x.append(x)
        node_y.append(y)
     
    
    def getTowns():
        ds = towns
        d = []
        for i in ds.keys():
              d.append(ds[i])
        return d
    
    
    master_colours = []
    
    for node in G.nodes():
        color = None
        if node == start:
            master_colours.append("#0000FF")
        elif path and node in path:
            master_colours.append("#ff0000")
        elif node == goal:
            master_colours.append("#FFFF00")
        else:
            master_colours.append("#ffffff")
            
        
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode=('text+markers'),
        hoverinfo='text',
        text = getTowns(),
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
#             colorscale='YlGnBu',
            reversescale=True,
            color = [],
            size=15,
            line_width=2))
    
    node_trace.marker.color = master_colours
    
    fig = go.Figure(data=[edge_trace, node_trace,eweights_trace],
             layout=go.Layout(
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=25,
            font_family="Rockwell"
            )
    )
    fig.update_traces(textposition='top center')
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON
