from ipapy import UNICODE_TO_IPA
from ipapy import is_valid_ipa
from ipapy.ipachar import IPAConsonant
from ipapy.ipachar import IPAVowel
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


modifiers_post=["ˈ","̞","̃","̻","̺","̪","ˤ","ˠ","ʲ","ʷ","̰","’","̤","ʰ","̯","̩","̬","̥"] 
vowels="iyɪʏeøɛœæaɶɨʉəɐɑɒɔʌoɤuɯʊ"

##Creació de taula de paraules a partir de llistes de Swadesh
##Create word table from Swadesh lists
def filetotab(file): 
    fi=open(file,"r",encoding="utf8")
    lines=fi.readlines()
    wordn=len(lines)
    langn=len(lines[0].split())
    tab_swa=[]
    for i in range(langn):
        tab_swa.append([])
        for j in range(wordn):
            tab_swa[i].append(lines[j].split()[i])
    fi.close()
    return tab_swa

##Creació de taula de trets fonològics
##Create phonological feature table
def features():
    fi=open("features.txt","r",encoding="utf8")
    lines=fi.readlines()
    tab_feat=[]
    for i in range(len(lines)):
        tab_feat.append(lines[i].split())
        for j in range(len(tab_feat[i])):
            if j!=0:
                tab_feat[i][j]=float(tab_feat[i][j])
    return tab_feat


##Creació de taula d'operadors (diacrítics)
##Create operator table (diacritics)
def operators():
    fi=open("operators.txt","r",encoding="utf8")
    lines=fi.readlines()
    tab_ope=[]
    for i in range(len(lines)):
        tab_ope.append([modifiers_post[i]])
        tab_ope[i].extend(lines[i].split())
        for j in range(1,len(tab_ope[i])):
            if tab_ope[i][j]!="ND":
                tab_ope[i][j]=float(tab_ope[i][j]) 
    return tab_ope

##Divisió de la paraula gràfica en AFI en grups de caràcters que corresponen cada un a un so.
##Division of the IPA transcription into groups of characters referring to one sound each. 
def segment(word): 
    word=word.replace("ɫ","lˠ")
    charlist=list(word)
    for i in range(len(charlist)-1,-1,-1):
        if charlist[i] == "ˈ":
            for j in range(i,len(charlist)):
                if charlist[j] in vowels:
                    charlist[j]=charlist[j]+charlist[i]
                    break
            del charlist[i]
    for i in range(len(charlist)-1,-1,-1):
        if charlist[i] == "͡": 
            charlist[i+1]=charlist[i]+charlist[i+1]+charlist[i+2]
            del charlist[i+2]
            del charlist[i]
        elif charlist[i] in modifiers_post:
            charlist[i-1]=charlist[i-1]+charlist[i]
            del charlist[i]
        elif charlist[i]==".":
            del charlist[i]
    for i in range(len(charlist)):
        if charlist[i]=="ː":
            charlist[i]=charlist[i-1]
    return charlist


##Obtenir vector de trets per al segment introduït
##Obtain feature vector for the character group 
def get_features(letters): 
    letlist=list(letters)
    if letlist[0]!="͡":
        feature=tab_feat[phonlist.index(letlist[0])].copy()
        del feature[0] 
        del letlist[0]
    else:
        del letlist[0]
        feature=tab_feat[phonlist.index(letlist[1])].copy()
        del feature[0]
        feature[4]=0.5
        feature[7]=1.0
        del letlist[0] 
        del letlist[0]
    for i in letlist:
        if i in modifiers_post:
            vec=tab_ope[modifiers_post.index(i)].copy()
            del vec[0]
            for j in range(len(vec)):
                if vec[j]!="ND":
                    feature[j]=vec[j]
        del letlist[0]
    return feature

##Càlcul de distància vectorial entre trets
##Distance between features
def dist_feat(phon1,phon2): 
    dist=0.0
    feat1=get_features(phon1)
    feat2=get_features(phon2)
    for i in range(len(feat1)):
        dist+=(feat1[i]-feat2[i])**2.0
    dist=np.sqrt(dist)
    dist=dist/np.sqrt(len(feat1))
    return dist
    
##Càlcul de distància entre paraules amb fórmula pròpia
##Distance between words using self-created formula.
def dist_word(word1,word2):
    dist=0.0
    distaux=0.0
    word1=segment(word1)
    word2=segment(word2)
    for i in word1:
        for j in word2:
            dist+=dist_feat(i,j)
    dist=dist/(len(word1)*len(word2))
    for i in word1:
        for j in word1:
            distaux+=dist_feat(i,j)
    distaux=distaux/(len(word1)**2.0)
    dist=dist-0.5*distaux
    distaux=0
    for i in word2:
        for j in word2:
            distaux+=dist_feat(i,j)
    distaux=distaux/(len(word2)**2.0)
    dist=dist-0.5*distaux
    return dist

##Càlcul de distància entre llengües a partir de mitjana de distància de paraules
##Distance between languages using average distance between words
def dist_lang(lang_ind_1,lang_ind_2):
    dist=0.0
    null=0
    for i in range(wordn):
        if tab_swa[lang_ind_1][i]=="-" or tab_swa[lang_ind_2][i]=="-":
            null+=1
        else:    
            dist+=dist_word(tab_swa[lang_ind_1][i],tab_swa[lang_ind_2][i])        
    dist=dist/(wordn-null)
    return dist

##Creació de taula amb distàncies entre llengües
##Create a table with the distances between languages
def dist_tab(file):
    global tab_swa
    tab_swa=filetotab(file)
    global langn
    langn=len(tab_swa)
    global wordn
    wordn=len(tab_swa[0])
    tab_dist=[]
    for i in range(langn):
        tab_dist.append([])
        for j in range(langn):
            a=dist_lang(i,j)*100.0
            tab_dist[i].append(round(a,2))
    return(tab_dist)
        
    
##Creació de matrius de trets auxiliars de referència
##Create feate
tab_feat=features()
tab_ope=operators()
phonlist=[]
for i in range(len(tab_feat)):
        phonlist.append(tab_feat[i][0])


##Formació de taules de distàncies
##Distance-table plots
tab_swa=filetotab("swadesh_rom_eus.txt")  ##Introduir fitxer
data= dist_tab("swadesh_rom_eus.txt")     ##Introduir fitxer
data_array = np.array(data)

cmap = plt.get_cmap("RdYlGn_r")
norm = Normalize(vmin=np.min(data_array), vmax=np.max(data_array))
sm = ScalarMappable(cmap=cmap, norm=norm)

fig, ax = plt.subplots(figsize=(6,4))
ax.axis('off')
##Introduir noms de llengües / Insert language names
table = ax.table(cellText=data, cellLoc='center', loc='center', colLabels=["Francès","Català","Castellà","Portuguès","Basc"],rowLabels=["Francès","Català","Castellà","Portuguès","Basc"])
for (i, j), cell in table.get_celld().items():
    cell.set_height(0.1)
    if j==-1:
        cell.set_text_props(ha="center", va="center")

for i in range(len(data)):
    for j in range(len(data[i])):
        color = sm.to_rgba(data[i][j])  
        table[(i+1, j)].set_facecolor(color)

plt.title("Distància entre llengües",fontsize=14,pad=3)
plt.subplots_adjust(top=0.85)
plt.show()












    
    






