import re
import numpy as np 
import sqlite3
import pandas as pd

glosario_file = open("Simonet.txt", encoding = "utf8")
glosario = glosario_file.read()
glosario_file.close()

#print(glosario[35000:55000])

y = re.compile("^\s+[A-ZÀ-ÿ]{3}[A-ZÀ-ÿ]*\s+|^\s+[A-ZÀ-ÿ]{3}[A-ZÀ-ÿ]*\.|^\s+[A-ZÀ-ÿ]{3}[A-ZÀ-ÿ]*,",flags= re.MULTILINE)

z = re.findall(y,glosario)

z = z[233:]
#print(z[1:30])
#print(len(z))


z = z[0:70]
print(z)
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


co = re.compile("\s|\.|\,")

#for i in range(len(z)):
#    if i < len(z) - 1:
#        z[i] = re.sub(co,"",z[i])


for i in range(len(z)):
    if i < len(z) - 1:
        print(i)
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

pag_counter = 1 

paginas = []
palabras_partidas = []

for clave in diccionario:
    paginas.append(pag_counter)
    if bool(re.search("\x0c",clave,flags=re.MULTILINE)):
        pag_counter += 1
        palabras_partidas.append(clave)
    elif bool(re.search("\x0c",diccionario[clave],flags=re.MULTILINE)):
        n_matches = len(re.findall("\x0c",diccionario[clave],flags=re.MULTILINE))
        pag_counter += n_matches
        palabras_partidas.append(clave)

diccionario2 = {}

for clave in diccionario:
    diccionario2[re.sub(co,"",clave)] = diccionario[clave]

entradas_frame = {
    "Entrada": list(diccionario2.keys()),
    "Página": paginas
}

entradas_frame = pd.DataFrame(entradas_frame)

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