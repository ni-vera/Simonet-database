from pdf2image import convert_from_path

images = convert_from_path("Glosario_recortado.pdf")

contador = 1
for i in range(len(images)):
    images[i].save(f"{str(i + 1)}.jpg","JPEG")
    contador += 1   
