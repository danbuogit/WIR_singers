import wikipediaapi
import os.path

#URL di base wikipedia
url = 'https://en.wikipedia.org/wiki/'

#file txt contente l'elenco dei cantanti
singerfile = '/utilityLists/Singers.txt'

#path salvataggio file
pathSave = '/ListInfluencedPage'

#lista python contenente l'elenco dei cantanti
singerlist = []

#iteratore per scaricare le pagine
i = 0

#variabile temporanea per scrivere i file ed effettuare il parse tostring.
var_temp = []


def get_sections (section, res, levels=0):
    for s in section:
        res.append(s.title)
        res.append(get_sections(s.sections, res, levels+1))
    return res

def fix_list(l):
    res=[]
    for elem in l:
        if (isinstance(elem, str)):
            res.append(elem)
    return res

#flusso di stream dal file txt alla lista python
with open(singerfile, encoding="utf8") as f:
  for line in f:
    currentPlace = line[:-1]
    singerlist.append(currentPlace)


for i in range(len(singerlist)):
    wiki = wikipediaapi.Wikipedia('en')
    mutcd = wiki.page(singerlist[i])
    all_section = fix_list(get_sections(mutcd.sections, [], 0))
    influence_section = ""
    for n in all_section:
        #var_temp=[]
        if "influences" in n or "Influences" in n:
            influence_section = str(n)
            #print(mutcd.section_by_title(influence_section))
            # file su cui salvare la sezione inerente l'influenza del singolo cantante
            file = open(os.path.join(pathSave, singerlist[i]+ '.txt'), 'w', encoding="utf8")
            var_temp = str(mutcd.section_by_title(influence_section))
            file.write(var_temp)
            file.close()

    print("Hai creato il file del cantante numero " + str(i) + " su " + str(len(singerlist)))