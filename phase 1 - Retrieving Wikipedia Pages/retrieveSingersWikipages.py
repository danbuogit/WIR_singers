from pywebcopy import WebPage

#URL di base wikipedia
url = 'https://en.wikipedia.org/wiki/'

#cartella di download delle pagine HTML dei cantanti
download_folder = 'C:/Users/Daniele/Desktop/Università/Web Information Retrivial/progetto v2/ricercaCoppie/'

#file txt contente l'elenco dei cantanti
singerfile = 'C:/Users/Daniele/Desktop/Università/Web Information Retrivial/progetto v2/ricercaListe/Singers.txt'

#lista python contenente l'elenco dei cantanti
singerlist = []

#iteratore per scaricare le pagine
i = 0

#flusso di stream dal file txt alla lista python
with open(singerfile, encoding="utf8") as f:
  for line in f:
    currentPlace = line[:-1]
    singerlist.append(currentPlace)
#print(singerlist)

for n in singerlist:
    wp = WebPage(url+singerlist[i], download_folder)
    wp.save_html()
    i=i+1



