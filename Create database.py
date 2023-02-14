import re
import numpy as np 

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


co = re.compile("\s|\. |\.")

#for i in range(len(z)):
#    if i < len(z) - 1:
#        z[i] = re.sub(co,"",z[i])


for i in range(len(z)):
    if i < len(z) - 1:
        print(i)
        term = re.sub("\s","",z[i])
        nexterm = re.sub("\s","\\\s+",z[i + 1])
        cadena = f"^{term}.*^{nexterm}"
        a = re.compile(cadena,flags = re.DOTALL)
        b = re.search(a,glosario)
        print(b)
        c = re.sub(f"^{term}(.*)^{nexterm}","\1",b[0])
        diccionario[z[i]] = c
        #print(re.findall(a,glosario))

for clave in diccionario:
    clave = re.sub(co,"",clave)

pag_counter = 1 

paginas = []
palabras_partidas = []

for clave in diccionario:
    paginas.append(pag_counter)
    if bool(re.search("\x0c",clave,flags=re.MULTILINE)) or bool(re.search("\x0c",diccionario[clave],flags=re.MULTILINE)):
        pag_counter += 1
        palabras_partidas.append(clave)
        






    

""""
castellano = []

patron_cas = re.compile("Cast.\s([A-ZÀ-ÿ]+)\s")

for i in diccionario:
    castellano.append(re.sub(patron_cas,"\1",diccionario[i]))

print(castellano)

    """