from pdf2image import convert_from_path

images = convert_from_path("Glosario_recortado.pdf")

for i, image in enumerate(images):
    fname = str(i+1) + ".jpg"
    image.save(fname, "JPEG")
