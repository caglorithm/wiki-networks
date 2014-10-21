#!/usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
#from pylab import *
#import matplotlib.pyplot as plt
import urllib2
import re
#from lxml import etree
from bs4 import BeautifulSoup
from networkx import graphviz_layout
from datetime import date
import sys
import Queue
import xml.etree.cElementTree as ET

import pygephi

# gephi stuff
g = pygephi.GephiClient('http://localhost:8080/workspace0', autoflush=True)
g.clean()

node_attributes = {"size":10, 'r':0.0, 'g':0.0, 'b':1.0, 'label':''}


# OPTIONS
do_stats = 0

# CREATING THE XML
#<gexf xmlns:viz="http:///www.gexf.net/1.1draft/viz" version="1.1" xmlns="http://www.gexf.net/1.1draft">
xmlgexl = ET.Element("gexf")
#<graph defaultedgetype="undirected" idtype="string" type="static">
xmlgraph = ET.SubElement(xmlgexl, "graph")
xmlgraph.set("defaultedgetype","undirected")
xmlgraph.set("idtype","string")
xmlgraph.set("type","static")
#<nodes count="77">
xmlnodes = ET.SubElement(xmlgraph, "nodes")
xmledges = ET.SubElement(xmlgraph, "edges")
field = []
edges = []

########### Parsing
old_links = {}
queue = Queue.Queue(0)
# first page to start with: http://de.wikipedia.org/wiki/User_Agent'

first_link = str(sys.argv[1])
old_links[first_link] = 0
field.append(ET.SubElement(xmlnodes, "node"))
field[0].set("id",str(0))
field[0].set("label", first_link)

base_url = 'http://en.wikipedia.org/wiki/'
tree_url = first_link
queue.put(tree_url)

n_loops=0
G=nx.Graph()
G.add_node(tree_url)
num=0
num_edges=-1
f = open('graph.txt', 'w')
fstat = open('stats.txt', 'w')
fstat.close()
while (num<int(sys.argv[2])):
    n_loops += 1
    tree_url = queue.get()
	#tree_url = urllib2.quote(tree_url)
    req_url = base_url + tree_url
    print req_url
    print("\t" + tree_url +  "  q: %d" % queue.qsize() + " nodes: %d" % num)
	
    try:
        req = urllib2.Request(req_url,headers={"User-Agent":"Opera/9.63"})
        filehandle = urllib2.urlopen( req ).read().decode('ascii', 'ignore')
    except:
        pass
			
    soup = BeautifulSoup(filehandle)
	
	# counter for new links per page
    new_nodes = 0
	
	# loop through links per page
    for link in soup.body.findAll("a"):
		# get all the href's of the html code
        thislink = link.get('href')
        thislink = str(thislink)
		
		# Filter out the wikipedia links to create new nodes
        if thislink.startswith("/wiki/") and not thislink.startswith("/wiki/Main_Page") and not ":" in thislink:
			# cut the /wiki/ part
            thislink = thislink[6:]
			
			#### FILTERS
			# cut the #-tag
            if '#' in thislink:
                thislink=thislink[:thislink.rfind('#')]
			
			# filter out disambiguation pages
            if "disambiguation"	in thislink:
                thislink=thislink[:thislink.rfind('disambiguation')-2]
			
			# filter out lists
            if thislink[:7] == "List_of":
                break

            
            if thislink[0] == '%': 
                thislink = thislink[1:]
			
			# if link is not already in old_links, add new node and add to queue	
            if thislink not in old_links:
                num += 1
                new_nodes += 1
                num_edges += 1
                queue.put(thislink)
                old_links[thislink]=num
				#thislink = urllib2.unquote(thislink)
				#tree_url = urllib2.quote(tree_url.encode('utf-8'))
                field.append(ET.SubElement(xmlnodes, "node"))
                field[num].set("id",str(num))
                field[num].set("label", thislink)
                field[num].set("size", str(1))
                edges.append(ET.SubElement(xmlnodes, "edge"))
                edges[num_edges].set("id",str(num_edges))
                edges[num_edges].set("source",str(old_links[tree_url]))
                edges[num_edges].set("target",str(old_links[thislink]))
                #gephi
                node_attributes['label'] = thislink
                g.add_node(str(num), **node_attributes)
                g.add_edge(str(num_edges), str(old_links[tree_url]), str(old_links[thislink]), directed=False)
                #G.add_node(thislink,node_color="blue")
                #G.add_edge(tree_url, thislink)
                #f.write (str(tree_url) + " -> " + str(thislink) + "\n")
            else:
                num_edges += 1
                edges.append(ET.SubElement(xmlnodes, "edge"))
                edges[num_edges].set("id",str(num_edges))
                edges[num_edges].set("source",str(old_links[tree_url]))
                edges[num_edges].set("target",str(old_links[thislink]))
                #G.add_edge(tree_url, thislink)
                #f.write (str(tree_url) + " -> " + str(thislink) + "\n")

	field[old_links[tree_url]].set("size", str(new_nodes))
    print "\tnew nodes: %d  level %d    num=%d" % (new_nodes,old_links[tree_url],num)	
    if (do_stats):    
        fstat = open('stats.txt', 'a')	
        fstat.write ("%d %d\n"% (n_loops,num))
        fstat.close()
				
f.close()
#print (old_links)
print "# data written ..."

#print "# clustering: %f" % nx.average_clustering(G)
#print(old_links)
print "# laying out the graph..."

# node size base on number of neighbours of a node
nodesize=[len(G.neighbors(v))+2 for v in G]

xmlnodes.set("count",str(num))
xmledges.set("count",str(num_edges))
tree = ET.ElementTree(xmlgexl)
filename = "filename.gexf"
tree.write(filename)

"""
# graphviz layouts = twopi, gvcolor, wc, ccomps, tred, sccmap, fdp, circo, neato, acyclic, nop, gvpr, dot
pos = nx.graphviz_layout(G)
print "# drawing graph..."
plt.figure(figsize=(60,60), dpi=500, facecolor='w', edgecolor='k')
#nx.draw(G, pos,node_size=nodesize, alpha=0.5, edge_alpha=0.1, edge_color="gray",edge_tickness=0.1, font_size=10)
# show graph
#plt.savefig("plot.jpg")
# write gexf file
#nx.write_gexf(G, "test.gexf")

######## TEST ALL LAYOUTS OF GRAPHVIz


bigfig = plt.figure(figsize=(4*60,4*60), dpi=500, facecolor='w', edgecolor='k')
gs = GridSpec(4, 4)
gs.update(left=0.1, right=0.98, top=0.98, bottom=0.10, wspace=0.05,hspace=0)

#layouts = ['twopi', 'gvcolor', 'wc', 'ccomps', 'tred', 'sccmap', 'fdp', 'circo', 'neato', 'acyclic', 'nop', 'gvpr', 'dot']
layouts = ['twopi',   'fdp', 'circo',  'dot']
for plot_i in range(0,len(layouts)-1):
	subplot(gs[plot_i])
	print "# Laying out %s" % layouts[plot_i]
	pos = nx.graphviz_layout(G,prog=layouts[plot_i])
	nx.draw(G, pos,node_size=nodesize, alpha=0.5, edge_alpha=0.1, edge_color="gray",edge_tickness=0.1, font_size=10)

plt.savefig('bigfig.jpg')
"""


