import re
import numpy as np 

glosario_file = open("Simonet.txt", encoding = "utf8")
glosario = glosario_file.read()
glosario_file.close()

#print(glosario[35000:55000])

y = re.compile("^\s+[A-ZÀ-ÿ]{3}[A-ZÀ-ÿ]*\s+",flags= re.MULTILINE)

z = re.findall(y,glosario)

z = z[199:]

print(z[1:20])
print(len(z))

