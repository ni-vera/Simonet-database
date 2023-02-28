import re
import numpy as np 
import sqlite3
import pandas as pd

glosario_file = open("Simonet.txt", encoding = "utf8")
glosario = glosario_file.read()
glosario_file.close()

#print(glosario[35000:55000])

y = re.compile("^\s{2}\s*[A-ZÀ-ÿ]{3}[A-ZÀ-ÿ]*\s+|^\s{2}\s*[A-ZÀ-ÿ]{3}[A-ZÀ-ÿ]*\.|^\s{2}\s*[A-ZÀ-ÿ]{3}[A-ZÀ-ÿ]*,",flags= re.MULTILINE)

z = re.findall(y,glosario)
z = z[207:]
#print(z[1:30])
#print(len(z))

co = re.compile("\s|\.|\,")
#""""
z_cleansed = z.copy()

for i in range(len(z_cleansed)):
    z_cleansed[i] = re.sub(co,"",z_cleansed[i])

repeticion_inmediata = []
for i in range(len(z_cleansed)-1):
    if z_cleansed[i] == z_cleansed[i + 1]:
        repeticion_inmediata.append(i +1)

for index in repeticion_inmediata:
    z[index] = 0

z = list(filter((0).__ne__,z))

import collections
print([item for item, count in collections.Counter(z_cleansed).items() if count > 1])


z.pop(322)
z.pop(672)
z.pop(743)
z.pop(764)
z.pop(774)
z.pop(810)
z.pop(824)
z.pop(832)
z.pop(983)
z.pop(996)
z.pop(1036)
z.pop(1096)
z.pop(1108)
#z.pop(1024)
#"""
z = z[0:1143]
diccionario = {}


print(len(z))
"""
term = re.sub("\s","",z[1])
nexterm = re.sub("\s","\\\s*",z[2])
cadena = f"(?<={term})(.*)(?={nexterm})"
print(cadena)
a = re.compile(cadena,flags = re.DOTALL)
print(re.findall(a,glosario))
"""
#for i in range(len(z)):
#    if i < len(z) - 1:
#        z[i] = re.sub(co,"",z[i])


for i in range(len(z)):
    if i < len(z) - 1:
        #print(i)
        term = z[i]
        nexterm = z[i + 1]
        cadena = f"{term}.*\n{nexterm}"
        a = re.compile(cadena,flags = re.DOTALL)
        b = re.search(a,glosario)
        c = re.sub(f"{term}","",b[0])
        c = re.sub(f"{nexterm}","",c)
        diccionario[z[i]] = c
        

#for clave in diccionario:
#    clave = re.sub(co,"",clave)

diccionario2 = {}


for clave in diccionario:
    diccionario2[re.sub(co,"",clave)] = diccionario[clave]

pag_counter = 1 


idiomas = ["Gall","Port","Fr","Val","Cat","Prov","Cast","Mall","Vasc","Lat","Rum","Alb","It",]
idiomas_alt = "|".join(idiomas)

palabras_partidas = []

tabla = {
"Entrada": list(diccionario2.keys()),
"paginas": []
}

for idioma in idiomas:
    tabla[idioma] = []

for clave in diccionario:
    tabla["paginas"].append(pag_counter)
    if bool(re.search("\x0c",clave,flags=re.MULTILINE)):
        pag_counter += 1
        palabras_partidas.append(clave)
    elif bool(re.search("\x0c",diccionario[clave],flags=re.MULTILINE)):
        n_matches = len(re.findall("\x0c",diccionario[clave],flags=re.MULTILINE))
        pag_counter += n_matches
        palabras_partidas.append(clave)
    longitud_entrada = len(diccionario[clave])
    if 400 > len(diccionario[clave]):
        until_char = len(diccionario[clave]) - 1
    else:
        until_char = 399
    if bool(re.search(fr"(({idiomas_alt})\.\sy\s({idiomas_alt})\.\s(\w+))|({idiomas_alt})\.\s(\w+)",diccionario[clave][0:until_char],flags=re.MULTILINE)):
        print("Ok")
        matches = re.findall(fr"(({idiomas_alt})\.\sy\s({idiomas_alt})\.\s(\w+))|({idiomas_alt})\.\s(\w+)",diccionario[clave][0:until_char],flags=re.MULTILINE)
        lenguas_en_matches = []
        for match in matches:
            if match[0] != "":
                lenguas = re.findall(fr"{idiomas_alt}",match[0],flags=re.MULTILINE)
                palabra = match[3]
                for lengua in lenguas:
                    if lengua not in lenguas_en_matches:
                        tabla[lengua].append(palabra)   
                        lenguas_en_matches.append(lengua)
            else:
                lengua = match[4]
                palabra = match[5]
                if lengua not in lenguas_en_matches:
                    tabla[lengua].append(palabra)
                    lenguas_en_matches.append(lengua)
        print(lenguas_en_matches)
        for lengua in idiomas:
            if lengua not in lenguas_en_matches:
                tabla[lengua].append('None')
    else:
        for columna in tabla:
            if (columna != "paginas") & (columna !="Entrada"):
                tabla[columna].append('None')
    for columna in tabla:
        if columna != "paginas":
            print(columna + str(len(tabla[columna])))
    print(tabla["Gall"])    
                
"""
entradas_frame = {
    "Entrada": list(diccionario2.keys()),
    "Página": paginas,
    "Castellano": castellano,
    "Portugués": portugues,
    "Francés": frances
}
"""

entradas_frame = tabla

entradas_frame = pd.DataFrame(entradas_frame)

entradas_frame.to_csv("entradas.csv", sep=",",header=True,index=False)

con = sqlite3.connect("simonet_prueba.db")
cur = con.cursor()

entradas_frame.to_sql("entradas",con,if_exists="replace")



    

""""
castellano = []

patron_cas = re.compile("Cast.\s([A-ZÀ-ÿ]+)\s")

for i in diccionario:
    castellano.append(re.sub(patron_cas,"\1",diccionario[i]))

print(castellano)

    """