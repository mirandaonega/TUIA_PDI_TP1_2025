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

# Validar campos
def validar_nombre_apellido(num_chars, num_words):
    """Mínimo 2 palabras, máximo 25 caracteres totales."""
    if num_chars > 25: 
        return "MAL"
    if num_words < 2: 
        return "MAL"
    return "OK"

def validar_edad(num_chars, num_words):
    """2 o 3 caracteres consecutivos sin espacios."""
    if num_words != 1: return "MAL"
    if not (2 <= num_chars <= 3): return "MAL"
    return "OK"

def validar_mail(num_chars, num_words):
    """Una palabra, no más de 25 caracteres."""
    if num_words != 1: return "MAL"
    if num_chars > 25: return "MAL"
    return "OK"

def validar_legajo(num_chars, num_words):
    """8 caracteres en total, única palabra."""
    if num_chars != 8: return "MAL"
    if num_words != 1: return "MAL"
    return "OK"

def validar_pregunta(num_chars_si, num_chars_no):
    """Única celda marcada con un único caracter."""
    marcada_si = (num_chars_si == 1)
    marcada_no = (num_chars_no == 1)
    
    if marcada_si or marcada_no:
        return "OK"
    else:
        return "MAL"
    
def validar_comentarios(num_chars, num_words):
    """Al menos 1 palabra, no más de 25 caracteres."""
    if num_words < 1: return "MAL"
    if num_chars > 25: return "MAL"
    return "OK"

# Mapeo de validadores
validacion = {
    "Nombre y apellido": validar_nombre_apellido,
    "Edad": validar_edad,
    "Mail": validar_mail,
    "Legajo": validar_legajo,
    "Comentarios": validar_comentarios,
}