from SPARQLWrapper import SPARQLWrapper, JSON
#lista per visualizzare file JSON#
singers = []
#costruzione query: select all singers with type Singer#
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(
"""select ?singer where 
{?singer a yago:Singer110599806; 
rdf:type dbo:Person; 
rdf:type dbo:MusicalArtist; 
rdf:type yago:LivingThing100004258; 
rdf:type umbel-rc:MusicalPerformer} """)
#aggiunti risultati in forma JSON alla lista#
sparql.setReturnFormat(JSON)
resultsSingers = sparql.query().convert()
singers.append(resultsSingers)
#creating list of singers (only name)#
singerNames = []
#per ogni risultato in "bindings"#
for page in singers:
    for result in page["results"]["bindings"]:
        try:
            #get stringa in "singer" in "value", dopo il divisore "/resource/"#
            cantante = result["singer"]["value"].split("/resource/")[1]
            #aggiungi stringa in lista#
            singerNames.append(cantante)
        except:
            print("",end="")

#writing file with all singers#
file = open("Singers.txt","w",encoding='utf-8')
for s in singerNames:
    file.write(s + "\n")
file.close()

#lista di tutte la bands con i membri attuali#
bandAndMembers = []
#costruzione query#
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(
"""select ?band ?member 
where{?band a dbo:Band. 
?band dbo:bandMember ?member. 
?member rdf:type ?type. 
filter(?type IN (yago:Singer110599806)&&(umbel-rc:MusicalPerformer)&&(yago:LivingThing100004258)&&(dbo:MusicalArtist)&&(dbo:Person))}""")
#risultati aggiunti alla lista#
sparql.setReturnFormat(JSON)
resultsBandNoFormers = sparql.query().convert()
bandAndMembers.append(resultsBandNoFormers)

#risultati aggiunti alla lista#
sparql.setReturnFormat(JSON)
resultsBandNoFormers = sparql.query().convert()
bandAndMembers.append(resultsBandNoFormers)
#creating list of tuples of band and members (only name)#
bandAndMember = []
#per ogni risultato in "bindings"#
for b in bandAndMembers:
    for result in b["results"]["bindings"]:
        try:
            #get band and member name#
            band = result["band"]["value"].split("/resource/")[1]
            member = result["member"]["value"].split("/resource/")[1]
            #create tuple and attach it to the list#
            couple = (band, member)
            bandAndMember.append(couple)
        except:
            print("",end="")

file = open("BandAndSinger.txt","w",encoding='utf-8')
for c in bandAndMember:
    bandName = c[0]
    memberName = c[1]
    file.write(bandName + " -> " + memberName + "\n")
file.close()

#lista di tutte la bands con i membri "former"#
bandAndMembers = []
#costruzione query#
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(
"""select ?band ?member 
where{?band a dbo:Band. 
?band dbo:formerBandMember ?member. 
?member rdf:type ?type. 
filter(?type IN (yago:Singer110599806)&&(umbel-rc:MusicalPerformer)&&(yago:LivingThing100004258)&&(dbo:MusicalArtist)&&(dbo:Person))} """)
#risultati aggiunti alla lista#
sparql.setReturnFormat(JSON)
resultsBandNoFormers = sparql.query().convert()
bandAndMembers.append(resultsBandNoFormers)

#creating list of tuples of band and members (only name)#
bandAndMember = []
#per ogni risultato in "bindings"#
for b in bandAndMembers:
    for result in b["results"]["bindings"]:
        try:
            #get band and member name#
            band = result["band"]["value"].split("/resource/")[1]
            member = result["member"]["value"].split("/resource/")[1]
            #create tuple and attach it to the list#
            couple = (band, member)
            bandAndMember.append(couple)
        except:
            print("",end="")

file = open("BandAndFormerSinger.txt","w",encoding='utf-8')
for c in bandAndMember:
    bandName = c[0]
    memberName = c[1]
    file.write(bandName + " -> " + memberName + "\n")
file.close()

#removing not singer members#
singers = []
bandsAndSingerToWriteDown = []

with open(r'Singers.txt','r',encoding='utf-8') as singerFile:
	for line in singerFile:
		singers.append(line.replace("\n",""))

with open(r'BandAndSinger.txt','r',encoding='utf-8') as bandFile:
	for b in bandFile:
		if b.split(" -> ")[1].replace("\n","") in singers:
			bandsAndSingerToWriteDown.append(b)
                                                         
newFile = open("BandAndSinger.txt",'w',encoding='utf-8')
for l in bandsAndSingerToWriteDown:
	newFile.write(l)
newFile.close()

bandsAndSingerToWriteDown.clear()

with open(r'BandAndFormerSinger.txt','r',encoding='utf-8') as bandFile:
	for b in bandFile:
		if b.split(" -> ")[1].replace("\n","") in singers:
			bandsAndSingerToWriteDown.append(b)

newFile = open("BandAndFormerSinger.txt",'w',encoding='utf-8')
for l in bandsAndSingerToWriteDown:
	newFile.write(l)
newFile.close()

#removing duplicates#
alreadyRead = []

with open(r'BandAndSinger.txt','r',encoding='utf-8') as file:
	for line in file:
		l = line.replace("\n","")
		if l not in alreadyRead:
			alreadyRead.append(l)

newFile = open("BandAndSinger.txt","w",encoding='utf-8')
for x in alreadyRead:
	newFile.write(x + "\n")
newFile.close()

alreadyRead = []

with open(r'BandAndFormerSinger.txt','r',encoding='utf-8') as file:
	for line in file:
		l = line.replace("\n","")
		if l not in alreadyRead:
			alreadyRead.append(l)

newFile = open("BandAndFormerSinger.txt","w",encoding='utf-8')
for x in alreadyRead:
	newFile.write(x + "\n")
newFile.close()

#per una ricerca più veloce, vorrei creare una unica lista di band e vedere se i due file contengono band diverse o meno#
bandsWithDuplicate = []
with open(r'BandAndSinger.txt','r',encoding='utf-8') as file:
	for line in file:
		bandName = line.split(" -> ")[0]
		bandsWithDuplicate.append(bandName)

#removing duplicate#
bands = list(set(bandsWithDuplicate))
print("List 1 has size of ")
print(len(bands))

bandsWithDuplicateFormer = []
with open(r'BandAndFormerSinger.txt','r',encoding='utf-8') as file:
	for line in file:
		bandName = line.split(" -> ")[0]
		bandsWithDuplicateFormer.append(bandName)

#removing duplicate#
formerBands = list(set(bandsWithDuplicateFormer))
print("List 1 has size of ")
print(len(formerBands))

#looking for different band#
uniqueList = bands

for b1 in formerBands:
	found = False
	for b2 in bands:
		if b2 == b1:
			found = True
	if found==False:
		#add band to list#
		uniqueList.append(b1)

print("Final file has size of ")
print(len(uniqueList))

#writing file#
file = open("AllBands.txt", "w", encoding="utf-8")
for b in uniqueList:
	file.write(b + "\n")
file.close()

#sorting lists#
files = ["Singers.txt","BandAndSinger.txt","BandAndFormerSinger.txt","AllBands.txt"]
index = 0
lines = []

while index < 4:
	with open(files[index],'r',encoding='utf-8') as file:
		for l in file:
			lines.append(l)

	lines.sort()
	
	newFile = open(files[index],'w',encoding='utf-8')
	for x in lines:
		newFile.write(x)

	newFile.close()
	lines.clear()
	index = index + 1

