import cv2
import numpy as np
import matplotlib.pyplot as plt


# Carga de formularios
forms = []
forms_grayscale = []
for i in range(1, 6):
    form = f'formulario_0{i}.png'
    forms.append(form)
    form_grayscale = cv2.imread(form, cv2.IMREAD_GRAYSCALE)
    forms_grayscale.append(form_grayscale)

for i in forms_grayscale:
    plt.figure(), plt.imshow(i, cmap='gray'), plt.show(block=False)

form_vacio = cv2.imread('formulario_vacio.png', cv2.IMREAD_GRAYSCALE)

# Campos
Campos = ["Nombre y apellido", "Edad", "Mail", "Legajo", "Pregunta 1", "Pregunta 2", "Pregunta 3", "Comentarios"]