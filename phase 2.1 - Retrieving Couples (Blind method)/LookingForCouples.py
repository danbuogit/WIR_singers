from html.parser import HTMLParser
from lxml import html
from SPARQLWrapper import SPARQLWrapper, JSON

refer = []
index = 0
progress = 0

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, store only value with "wiki" in it.
               if name == "href":
                   if "wiki/" in value:
                   		substring = value.split("wiki/")[1]
                   		#removing special cases#
                   		if substring[:5] != "File:" and substring[:5] != "Help:" and substring[:10] != "Wikipedia:" and substring[:9] != "Category:" and substring[:8] != "Special:" and substring[:7] != "Portal:" and substring[:5] != "Book:":
                   			refer.append(substring)

index = 0

#taking all singer name as string, in order to check their relations#
strings = []
with open(r'utilityLists\\Singers.txt','r',encoding='utf-8') as singers:
    for s in singers:
        strings.append(s)

total = len(strings)
#looking and working on the exact file#
matches = []
for s in strings:
  actualSinger = s.split("\n")[0]
  #adaptation to special character "/"#
  if "/" in actualSinger:
    actualSinger = actualSinger.replace("/","$")

  fileName = "Retrieving Wikipedia Pages\\en.wikipedia.org\\wiki" + actualSinger + ".html"
  parser = MyHTMLParser()

  fileFound = True
  possibleMatches = []
  
  try:
    #getting wiki file#
    with open(fileName,'r', encoding='utf-8') as f:
      #getting links list#
      parser.feed(f.read())
  except Exception as e:
    fileFound = False
  
  if fileFound:
    #removing duplicates#
    possibleMatches = list(set(refer))

    #looking for matches in the singer file#
    with open(r'utilityLists\\Singers.txt','r',encoding='utf-8') as AllSingers:
      for s in AllSingers:
        for m in possibleMatches:
          s = s.replace("\n","")
          m = m.replace("\n","")
          if m == s and m != actualSinger:
            couple = [actualSinger, s]
            matches.append(couple)

    #looking for matches in the BAND file#
    bandMatches = []
    with open(r'utilityLists\\AllBands.txt','r',encoding='utf-8') as AllBands:
      for b in AllBands:
        for m in possibleMatches:
          b = b.replace("\n","")
          m = m.replace("\n","")
          if m==b:
            bandMatches.append(b)

    #look for singer in the bands found previously#
    if len(bandMatches) != 0:
      with open(r'utilityLists\\BandAndSinger.txt','r',encoding='utf-8') as BandAndSinger:
        for m in bandMatches:
          for BandS in BandAndSinger:
            bandName = BandS.split(" -> ")[0]
            singerName = BandS.split(" -> ")[1].replace("\n","")
            if m == bandName and singerName != actualSinger:
              couple = [actualSinger, singerName]
              matches.append(couple)

      with open(r'utilityLists\\BandAndFormerSinger.txt','r',encoding='utf-8') as BandAndFormerSinger:
        for m in bandMatches:
          for BandS in BandAndFormerSinger:
            bandName = BandS.split(" -> ")[0]
            singerName = BandS.split(" -> ")[1].replace("\n","")
            if m == bandName and singerName != actualSinger:
              couple = [actualSinger, singerName]
              matches.append(couple)

      #emptying list#
      bandMatches.clear()
      
  else:
    print(fileName + " not found")

  possibleMatches.clear()
  refer.clear()
  
  #progress tacking#
  progress = progress + 1
  percentProgress = 100 * progress / total
  print(str(percentProgress) + "% done")

  #writing down results every 1000 matches or above#
  if len(matches) > 1000:
    file = open("_resultingCouples" + str(index) + ".txt", "w", encoding="utf-8", newline='')
    index = index + 1
    for x in matches:
      file.write(x[0] + " - influenced by -> " + x[1] + "\n")
    file.close()
    print("New result file written")
    matches.clear()

#removing duplicates#
index = 0
#have to arrive to 413#
fileName = "_resultingCouples"
progress = 0
lines = []

while index < 44:
  realFileName = fileName + str(index) + ".txt"
  with open(realFileName,'r',encoding='utf-8') as file:
    #store file locally#
    for line in file:
      thisLine = line.replace("\n","")
      lines.append(thisLine)
  #removing duplicates#
  lines = list(set(lines))
  lines.sort()
  #writing file#
  with open(realFileName, 'w', encoding = 'utf-8') as newFile:
    for l in lines:
      newFile.write(l + "\n")
  index = index + 1
  lines.clear()

  #tracking progress#
  progress = index/43 * 100
  print(str(progress) + "% done")

#retrieving fictional singer and eliminate them from list#
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
fictionalSingers = []
sparql.setQuery(
"""select ?singer where {?singer a yago:Singer110599806; rdf:type dbo:FictionalCharacter.} """)

sparql.setReturnFormat(JSON)
resultsSingers = sparql.query().convert()
fictionalSingers.append(resultsSingers)

singerNames = []
#per ogni risultato in "bindings"#
for page in fictionalSingers:
    for result in page["results"]["bindings"]:
        try:
            #get stringa in "singer" in "value", dopo il divisore "/resource/"#
            cantante = result["singer"]["value"].split("/resource/")[1]
            #aggiungi stringa in lista#
            singerNames.append(cantante.replace("\n",""))
        except:
            print("",end="")

print("Found " + str(len(singerNames)) + " fictional singers")

#starting to eliminate these singers from list#
fileName = "_resultingCouples"
for fs in singerNames:
  index = 0
  while index < 44:
    lines = []
    realFileName = fileName + str(index) + ".txt"
    index = index + 1
    with open(realFileName,'r',encoding = 'utf-8') as file:
      numberOfLines = 0
      for l in file:
        numberOfLines = numberOfLines + 1
        if fs not in l:
          lines.append(l)

    if len(lines)!=numberOfLines:
      #something has been erased, so we have to write a new file#
      with open(realFileName, 'w', encoding = 'utf-8') as newFile:
        for l in lines:
          newFile.write(l)

#all couples are found, now is required a single file#
fileName = "_resultingCouples"
index = 0
couples = []

while index < 43:
  realFileName = fileName + str(index) + ".txt"
  index = index + 1
  with open(realFileName, 'r', encoding='utf-8') as file:
    for line in file:
      couples.append(line)

with open(fileName + ".txt", 'w', encoding = 'utf-8') as newFile:
  for c in couples:
    newFile.write(c)
