import networkx as nx
import operator

file = open("\\Retrieving Couples (Blind method)\\_resultingCouples.txt","r",encoding="utf-8")
progress = 0
graph = nx.DiGraph()
total = 38104

for line in file:
    progress = progress + 1
    singer = line.split(" - influenced by -> ")[0]
    influencer = line.split(" - influenced by -> ")[1].replace("\n","")

    graph.add_edge(singer, influencer)
    print(str(progress * 100 / total))

print("Appling page rank...")
pr = nx.pagerank(graph, alpha =0.85)
sorted_pr = sorted(pr.items(), key=operator.itemgetter(1))
sorted_pr.reverse()

print("Writing file...")
#writing result of pagerank#
with open("pagerank(Blind_Method).txt","w",encoding="utf-8") as result:
	for i in sorted_pr:
		result.write(str(i) + "\n")
