from stanfordcorenlp import StanfordCoreNLP
import networkx as nx
import json
import os

#returns string            
def fix_name(s):
    pos = s.rfind("(")
    if (pos != -1):
        s = s[:pos-1]
    if ("%3F" in s):
        s = s.replace("%3F", "?")
    if ("%22" in s):
        s = s.replace("%22", '"')
    return s

#path1, path2 are paths to files containing band -> (former) singer
#returns dictionary with entries: "band": set of its singers
def build_band_mapping(path1, path2):
    l1 = open(path1, encoding="utf8").read().splitlines()
    l2 = open(path2, encoding="utf8").read().splitlines()
    l = l1+l2
    
    res = {}
    for elem in l:
        band, singer = elem.split(" -> ")
        band = fix_name(band)
        singer = fix_name(singer)
        if (band in res):
            res[band].add(singer)
        else:
            res[band] = {singer}
    return res

###START###
print("Start Standford CoreNLP Server")

#open Standford CoreNLP server
nlp = StanfordCoreNLP(r'C:\Users\elelo\Desktop\stanford-corenlp-full-2018-10-05', memory='8g')

singers_path = r'C:\Users\elelo\Desktop\WIR\singers_influences'
#list of filenames for all singers with influence section (e.g. Kurt_Cobain.txt)
singers_file = os.listdir(singers_path)

#sorted list containing singers from DBPedia
all_singers = open(r"C:\Users\elelo\Desktop\WIR\listeUtili\Singers.txt", encoding="utf8").read().splitlines()

#sorted list containing bands from DBPedia
all_bands = open(r"C:\Users\elelo\Desktop\WIR\listeUtili\AllBands.txt", encoding="utf8").read().splitlines()

#fix names (e.g. substitue '%3F' with '?')
for i in range(len(all_singers)):
    all_singers[i] = fix_name(all_singers[i])

for i in range(len(all_bands)):
    all_bands[i] = fix_name(all_bands[i])
    
all_singers.sort()
all_bands.sort()

#dictionary with entries: "band": set of its (current and former) singers    
band_members = build_band_mapping(r"C:\Users\elelo\Desktop\WIR\listeUtili\BandAndFormerSinger.txt", r"C:\Users\elelo\Desktop\WIR\listeUtili\BandAndSinger.txt")    

#set of pairs (singer, influencer)
pairs = set()
print("Start processing singers...")

for f in singers_file:
    #remove file extension
    current_singer = fix_name(f[:-4])
    current_path = os.path.join(singers_path, f)
    
    #open file containing influence section of current_singer
    text = open(current_path, encoding='utf8').read()

    print("\ncurrent singer: "+current_singer)

    #run annotation for NER
    print("Running annotation for NER...", end="")
    props = {'annotators': 'ner','pipelineLanguage':'en'}
    json_output = nlp.annotate(text, properties=props)
    print("done")
    ann = json.loads(json_output) #ann is a dictionary
    
    #dictionary containing found entities: "entity_type": word
    entities = {}
    entities["PERSON"] = []
    entities["ORGANIZATION"] = []

    num_sentences = len(ann["sentences"])

    #create dictionary "entities"
    for i in range(num_sentences):
        #entities found in i-th sentence
        current_entities = ann["sentences"][i]["entitymentions"]
        
        #number of entitities found per sentence
        num_current = len(current_entities)
        for j in range(num_current):
            entity_type = current_entities[j]["ner"]
            if (entity_type=="PERSON" or entity_type=="ORGANIZATION"):
                entities[entity_type].append(current_entities[j]["text"].replace(" ", "_"))
    
    #create pairs:     
    #check entities PERSON            
    for p in entities["PERSON"]:
        if (p!=current_singer and p in all_singers):
            #current_singer was influenced by p
            pairs.add((current_singer, p))

    #check entities ORGANIZATION (for bands)
    for b in entities["ORGANIZATION"]:
        if (b in all_bands):
            lead_singers = band_members[b]
            for s in lead_singers:
                #if the singer s of the band b is in all_singers
                #then add (current_singer, s) to pairs
                if (s!=current_singer and s in all_singers):
                    pairs.add((current_singer, s))
                
    print("Finished creating pairs for "+current_singer)
  
print("\nFinished processing singers!")
nlp.close()

#graph of the singers
g = nx.DiGraph()

#add nodes
for s in all_singers:
    g.add_node(s)

#add edges    
g.add_edges_from(pairs)

#apply PageRank and put it in a list of pairs (singer, score)
PR = sorted(nx.pagerank(g).items(), key=lambda kv: kv[1], reverse=True)

#print list of top 100
for i in range(100):
    print(str(i+1)+". "+PR[i][0])

#print("Incoming edges of node Elvis_Presley:")
#print(str(g.in_edges('Elvis_Presley')))

#save output (pairs)
out=open("Coppie.txt", 'w', encoding='utf-8')
for p in pairs:
    out.write(str(p)+"\n")
out.close()

