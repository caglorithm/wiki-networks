#!/usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
import urllib2
import re
from Tkinter import *
from lxml import etree
from bs4 import BeautifulSoup
from networkx import graphviz_layout
from datetime import date
import sys
import Queue

def draw_graph(graph):

    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    G=nx.Graph()

    # add nodes
    for node in nodes:
        G.add_node(node)

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos)

    # show graph
    plt.show()

def of_today(inp):
	return (inp.find_all('td' , recursive=False, text = re.compile(todaystring) ) != [])

class MensaAnzeiger(Frame):

    def createWidgets(self,essen1, essen2 , schnellerTeller , wochenwechsel):
		# self.QUIT = Button(self)
		# self.QUIT["text"] = "Close"
		# self.QUIT["command"] = self.quit
		self.canvas1 = Canvas(self, height = "220" , width = "800")
		self.canvas1.create_text(90,40 , text = "Schneller Teller: \n"+schnellerTeller)
		self.canvas1.create_text(390,50 , text =  "Essen 1: \n"+essen1)
		self.canvas1.create_text(670,50 , text = 		 "Essen 2: \n"+essen2)
		self.canvas1.create_text(360,150 , text = "Pommes: \n"+wochenwechsel)

		self.canvas1.pack({"side" : "left"})

		# self.canvas2 = Canvas(self , bg = "#ccbb99")
		# self.canvas2.create_text(40,40,text=" Deine Mudda", fill = "red")
		# self.canvas2.pack({"side" : "left"})
    def setNoFood(self):

		self.canvas1 = Canvas(self, height = "220" , width = "800")
		self.canvas1.create_text(390,100 , text = "Heute kein Essen!")
		self.canvas1.pack({"side" : "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()




########### Parsing
old_links = {}
queue = Queue.Queue(0)
# first page to start with: http://de.wikipedia.org/wiki/User_Agent'


base_url = 'http://en.wikipedia.org/wiki/'
tree_url = str(sys.argv[1])
queue.put(tree_url)

n_loops=0
G=nx.Graph()
G.add_node(tree_url)
num=0
while (num<int(sys.argv[2])):
	n_loops += 1
	tree_url = queue.get()
	#tree_url = urllib2.quote(tree_url)
	req_url = base_url + tree_url
	print req_url
	print(tree_url +  "  q: %d" % queue.qsize() + " nodes: %d" % num + " - %d bytes" % sys.getsizeof(G))
	
	try:
		req = urllib2.Request(req_url,headers={"User-Agent":"Opera/9.63"})
		filehandle = urllib2.urlopen( req ).read().decode('ascii', 'ignore')
	except:
		pass
			
	soup = BeautifulSoup(filehandle)

	todaystring = date.today().strftime("%d.%m.%Y")
	
##### GUI	
#root = Tk()
#app = MensaAnzeiger(master=root  )
	
	for link in soup.body.findAll("a"):
		
		thislink = link.get('href')
		thislink=str(thislink)
		
		if thislink.startswith("/wiki/") and not thislink.startswith("/wiki/Main_Page") and not ":" in thislink:
			#cut the #-tag
			if '#' in thislink:
				thislink=thislink[:thislink.rfind('#')]
			# cut the /wiki/ part
			thislink = str(link.get('href'))[6:]
			num+=1
			if thislink[0] == '%': 
				thislink = thislink[1:]
			if thislink not in old_links:
				queue.put(thislink)
				old_links[thislink]=num
				#thislink = urllib2.unquote(thislink)
				#tree_url = urllib2.quote(tree_url.encode('utf-8'))
				G.add_node(thislink)
				G.add_edge(tree_url, thislink)
			else:
				G.add_edge(tree_url, thislink)
			#print(str(link.get('href'))[6:])
			
	
	#print("qsize: %d" % queue.qsize())	

f = open('graph.txt', 'w')
for writelink in old_links:
	#print "%d %s" % (old_links[writelink],writelink)
	f.write("%d" % old_links[writelink])
	f.write(" " + str(writelink) + "\n")
print "data written ..."

#print G.nodes()

print "clustering: %f" % nx.average_clustering(G)
#print "shortest path LSD->MDMA %f" % nx.shortest_path_length(G, source="LSD", target="Magic_Mushrooms")

#print(old_links)
pos = nx.graphviz_layout(G,root=0)
print "drawing graph..."
plt.figure(figsize=(50,50), facecolor='w', edgecolor='k')
nx.draw(G, pos,node_size=5,alpha=0.5,node_color="blue", edge_alpha=0.1, edge_color="gray",edge_tickness=0.1, font_size=12)
# show graph

plt.savefig("plot.png")
#plt.show()


# Finde Tabelleneintrag für heute und schreibe Einträge in Strings
if soup.body.table.find(of_today)!= None:
	E1 =  soup.body.table.find(of_today).find_all('td')[2].get_text("\n",strip=True)
	E2 =  soup.body.table.find(of_today).find_all('td')[3].get_text("\n",strip=True)
	ST =  soup.body.table.find(of_today).find_all('td')[1].get_text("\n",strip=True)
	WW =  soup.body.table.find(of_today).find_all('td')[4].get_text("\n",strip=True)

	#app.createWidgets(E1,E2 , ST , WW)

#else :
	#app.setNoFood()

#app.mainloop()
#root.destroy()
########### Oberfläche zum ausgeben mit Tkinter

