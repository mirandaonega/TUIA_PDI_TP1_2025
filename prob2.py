# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv

# %%
def imshow(img, new_fig=True, title=None, color_img=False, blocking=False, colorbar=True, ticks=False):
    if new_fig:
        plt.figure()
    if color_img:
        plt.imshow(img)
    else:
        plt.imshow(img, cmap='gray')
    plt.title(title)
    if not ticks:
        plt.xticks([]), plt.yticks([])
    if colorbar:
        plt.colorbar()
    if new_fig:        
        plt.show(block=blocking)

# %%
def detectar_palabras(imagen):
    """Detecta palabras en una imagen.
    
    Args:
        imagen: Array numpy con la imagen (puede ser BGR o grayscale)
    
    Returns:
        int: Cantidad de palabras detectadas
    """
    # Verificar si la imagen se cargó correctamente
    if imagen is None:
        print("Error: No se pudo cargar la imagen.")
        return 0
    
    # --- Preprocesamiento: Convertir a escala de grises si es necesario ---
    if len(imagen.shape) == 3:
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    else:
        gris = imagen
    imagen_con_bordes = imagen.copy()
    
    # desenfoque para reducir el ruido
    gris_blur = cv2.medianBlur(gris, 3)

    # Detectamos los bordes con Canny
    bordes_canny = cv2.Canny(gris_blur, 15, 55)

    # Definimos un kernel para la dilatación (ancho para conectar letras, altura pequeña)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 3))
    
    # Dilatamos los bordes horizontalmente para conectar los contornos de las letras
    bordes_dilatados = cv2.dilate(bordes_canny, kernel, iterations=1)

    contornos, _ = cv2.findContours(bordes_dilatados, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_ancho = 30
    min_alto = 3
    
    cant_palabras = 0

    for contorno in contornos:
        x, y, w, h = cv2.boundingRect(contorno)
        
        # Filtrar contornos que parecen texto
        if w > min_ancho and h > min_alto and h <= 30:
            # Dibuja el rectángulo
            cv2.rectangle(imagen_con_bordes, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cant_palabras += 1

    # rgb_imagen = cv2.cvtColor(imagen_con_bordes, cv2.COLOR_BGR2RGB)

    # plt.figure(figsize=(10, 8))
    # plt.imshow(rgb_imagen)
    # plt.title("Detección de Letras Individuales")
    # plt.axis('off')
    # plt.show()

    return cant_palabras

# %%
def detectar_caracteres(imagen, form=False):
    """Detecta caracteres en una imagen.
    
    Args:
        imagen: Array numpy con la imagen (grayscale)
        form: 
            Si True, retorna las dimensiones del último caracter detectado (w, h)
            Si False, retorna la cantidad total de caracteres
    
    Returns:
        int o tuple: Cantidad de caracteres o (ancho, alto) del último caracter
    """
    if imagen is None:
        print("Error: No se pudo cargar la imagen.")
        return 0
    
    # Preprocesamiento: asegurar que sea grayscale
    if len(imagen.shape) == 3:
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    else:
        gris = imagen
    
    # Desenfoque para reducir ruido
    gris_blur = cv2.medianBlur(gris, 3)
    imagen_con_bordes = imagen.copy()

    _, binaria_invertida = cv2.threshold(gris_blur, 160, 255, cv2.THRESH_BINARY_INV)
    
    # Encontrar contornos en la imagen binaria
    contornos, _ = cv2.findContours(binaria_invertida, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrado para letras individuales
    min_ancho = 1 
    min_alto = 1
    max_ancho = 30
    max_alto = 40  
    
    cant_caracteres = 0
    lados_rectangulos = []

    for contorno in contornos:
        x, y, w, h = cv2.boundingRect(contorno)
        
        # Filtrar por tamaño de letra
        if w > min_ancho and h > min_alto and w < max_ancho and h < max_alto: 
            if form:  # Si es la celda de formulario
                lados_rectangulos.append((w, h))

            cv2.rectangle(imagen_con_bordes, (x, y), (x + w, y + h), (0, 255, 0), 1) 
            cant_caracteres += 1

    if form and len(lados_rectangulos) > 0:
        # Retornar las dimensiones del último caracter
        return lados_rectangulos[-1]
    
    # rgb_imagen = cv2.cvtColor(imagen_con_bordes, cv2.COLOR_BGR2RGB)

    # plt.figure(figsize=(10, 8))
    # plt.imshow(rgb_imagen)
    # plt.title("Detección de Letras Individuales (Binarización)")
    # plt.axis('off')
    # plt.show()

    return cant_caracteres


# %%
def extraer_campos(imagen):
    """Permite separar campos en una imagen de interes y guardar sus coordenadas
    en un dicionario."""
    
    campos = ['FORMULARIO', 'NOMBRE_Y_APELLIDO', 'EDAD', 'MAIL', 'LEGAJO', 
            'PREGUNTA_1', 'PREGUNTA_2', 'PREGUNTA_3', 'COMENTARIOS']

    umbral = 80
    imagen_binaria = np.where(imagen >= umbral, 1, 0)

    # Suma valores de píxeles a lo largo de las columnas y filas
    suma_columnas = np.sum(imagen_binaria, axis=0)
    suma_filas = np.sum(imagen_binaria, axis=1)

    # Define umbrales para detectar líneas en columnas y filas
    umbral_columnas = 0.7 * np.max(suma_columnas)
    umbral_filas = 0.5 * np.max(suma_filas)

    # Detectar líneas en columnas y filas
    lineas_columnas = np.where(suma_columnas < umbral_columnas)[0]
    lineas_filas = np.where(suma_filas < umbral_filas)[0]

    renglon = {}
    
    c = 0
    ancho_filas = lineas_filas[1] - lineas_filas[0] 
    
    for i in range(0, len(lineas_filas)):
        if i == 5:
            continue  # saltea la fila de encabezado si/no
        if i == 9:
            # el ancho de la fila de comentarios es aprox el doble del resto.      
            renglon[campos[c]] = (lineas_filas[i-1]+(ancho_filas*2), 
                                    lineas_filas[i]+(ancho_filas*2), 
                                    lineas_columnas[1], 
                                    lineas_columnas[3])
        else:
            if i == 0:
                renglon[campos[c]] = (lineas_filas[i], 
                                        lineas_filas[i]+ancho_filas, 
                                        lineas_columnas[1], 
                                        lineas_columnas[3]) 
            else:
                renglon[campos[c]] = (lineas_filas[i-1]+ancho_filas, 
                                        lineas_filas[i]+ancho_filas, 
                                        lineas_columnas[1], 
                                        lineas_columnas[3])
        c += 1         

    return renglon

# %%
f1 = cv2.imread('formulario_01.png', cv2.IMREAD_GRAYSCALE)
extraer_campos(f1)

# %%
Campos = ["Nombre y apellido", "Edad", "Mail", "Legajo", 
        "Pregunta 1", "Pregunta 2", "Pregunta 3", "Comentarios"]

def validar_nombre_apellido(num_chars, num_words):
    """Mínimo 2 palabras, máximo 25 caracteres totales."""
    if num_chars > 25: 
        return "MAL"
    if num_words < 2: 
        return "MAL"
    return "OK"

def validar_edad(num_chars, num_words):
    """2 o 3 caracteres consecutivos sin espacios."""
    if num_words != 1: 
        return "MAL"
    if not (2 <= num_chars <= 3): 
        return "MAL"
    return "OK"

def validar_mail(num_chars, num_words):
    """Una palabra, no más de 25 caracteres."""
    if num_words != 1: 
        return "MAL"
    if num_chars > 25: 
        return "MAL"
    return "OK"

def validar_legajo(num_chars, num_words):
    """8 caracteres en total, única palabra."""
    if num_chars != 8: 
        return "MAL"
    if num_words != 1: 
        return "MAL"
    return "OK"

def validar_pregunta(num_chars, _):
    """Única celda marcada con un único caracter."""
    if num_chars == 1:
        return "OK"
    else:
        return "MAL"
    
def validar_comentarios(num_chars, num_words):
    """Al menos 1 palabra, no más de 25 caracteres."""
    if num_words < 1: 
        return "MAL"
    if num_chars > 25: 
        return "MAL"
    return "OK"

# %%
def validacion_de_formulario(formulario):
    """Valida un formulario completo.
    
    Args:
        imagen_path: Ruta al archivo de imagen del formulario
    
    Returns:
        tuple: (diccionario_validacion, coordenadas_nombre)
            - diccionario_validacion: dict con campos y 'OK'/'MAL' o tipo de formulario
            - coordenadas_nombre: tupla con coordenadas del campo NOMBRE_Y_APELLIDO
    """

    validadores = [
        validar_nombre_apellido,
        validar_edad,
        validar_mail,
        validar_legajo,
        validar_pregunta,
        validar_pregunta,
        validar_pregunta,
        validar_comentarios
    ]

    # Área del bounding box para tipos de formulario
    a = 11 * 20
    b = 10 * 20

    coordenadas = extraer_campos(formulario)
    resultado_validacion = {}
    coord_nombre = ()

    c = 0
    for campo_nombre, coords in coordenadas.items():
        y1, y2, x1, x2 = coords
        campo_recortado = formulario[y1:y2, x1:x2]
        
        if campo_nombre == 'NOMBRE_Y_APELLIDO':
            coord_nombre = coords

        if campo_nombre != 'FORMULARIO':
            cant_palabras = detectar_palabras(campo_recortado)
            cant_caracteres = detectar_caracteres(campo_recortado)  
            resultado = validadores[c](cant_caracteres, cant_palabras)
            resultado_validacion[campo_nombre] = resultado
            if c < 7:
                c += 1
        else: 
            # Detectar tipo de formulario
            dimensiones = detectar_caracteres(campo_recortado, form=True)
            if isinstance(dimensiones, tuple):
                w, h = dimensiones
                if w * h == a:
                    tipo = 'A'
                elif w * h == b:
                    tipo = 'B'
                else:
                    tipo = 'C'
            else:
                tipo = 'C'  # Default si no se detectó nada
            resultado_validacion[campo_nombre] = tipo

    print('> NOMBRE_Y_APELLIDO:', resultado_validacion.get('NOMBRE_Y_APELLIDO', 'MAL'))
    print('> EDAD:', resultado_validacion.get('EDAD', 'MAL'))
    print('> MAIL:', resultado_validacion.get('MAIL', 'MAL'))
    print('> LEGAJO:', resultado_validacion.get('LEGAJO', 'MAL'))
    print('> PREGUNTA_1:', resultado_validacion.get('PREGUNTA_1', 'MAL'))
    print('> PREGUNTA_2:', resultado_validacion.get('PREGUNTA_2', 'MAL'))
    print('> PREGUNTA_3:', resultado_validacion.get('PREGUNTA_3', 'MAL'))
    print('> COMENTARIOS:', resultado_validacion.get('COMENTARIOS', 'MAL'))
    
    return resultado_validacion, coord_nombre

# %%
def ejecutar():
    """Procesa todos los formularios y genera el CSV de validación."""
    forms_tipo = {'A': [], 'B': [], 'C': []}
    datos_csv = []  # Lista de listas con los datos para el CSV
    coordenadas = {}
    
    # Crear figura más grande con 3 columnas y 2 filas
    plt.figure(figsize=(18, 8))
    
    for i in range(1, 6):
        form = f'formulario_0{i}.png'
        formulario_img = cv2.imread(form, cv2.IMREAD_GRAYSCALE)
        print('='*36)
        print('Índice del formulario', i)
        validacion, coord = validacion_de_formulario(formulario_img)  # ← Pasar la imagen, no la ruta
        
        # Clasificar por tipo
        tipo_form = validacion.get('FORMULARIO', 'C')
        forms_tipo[tipo_form].append(i)

        # Crear fila CSV con el formato especificado:
        # ID, Nombre y Apellido, Edad, Mail, Legajo, Pregunta 1, Pregunta 2, Pregunta 3, Comentarios
        fila_csv = [
            i,  # ID del formulario
            validacion.get('NOMBRE_Y_APELLIDO', 'MAL'),
            validacion.get('EDAD', 'MAL'),
            validacion.get('MAIL', 'MAL'),
            validacion.get('LEGAJO', 'MAL'),
            validacion.get('PREGUNTA_1', 'MAL'),
            validacion.get('PREGUNTA_2', 'MAL'),
            validacion.get('PREGUNTA_3', 'MAL'),
            validacion.get('COMENTARIOS', 'MAL')
        ]

        datos_csv.append(fila_csv)

        # Extraer el crop del campo Nombre y Apellido
        y1, y2, x1, x2 = coord
        crop = formulario_img[y1:y2, x1:x2]

        # Mostrar en grid de 3 columnas
        plt.subplot(2, 3, i)  # 2 filas, 3 columnas
        
        if 'MAL' not in validacion.values():
            # Sin errores: mostrar normalmente
            plt.imshow(crop, cmap='gray')
            plt.title(f'Formulario {i} - Tipo {tipo_form}\n✓ OK', color='green', fontsize=12, weight='bold')
        else:
            # Con errores: invertir colores
            crop_invertido = cv2.bitwise_not(crop)
            plt.imshow(crop_invertido, cmap='gray')
            plt.title(f'Formulario {i} - Tipo {tipo_form}\n✗ CON ERRORES', color='red', fontsize=12, weight='bold')
        
        plt.axis('off')

    plt.tight_layout()
    plt.show()

    nombre_archivo = 'data_formularios.csv'

    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)

        # Escribir encabezado
        encabezado = ['ID', 'Nombre y Apellido', 'Edad', 'Mail', 'Legajo', 
                        'Pregunta 1', 'Pregunta 2', 'Pregunta 3', 'Comentarios']
        escritor.writerow(encabezado)

        # Escribir todas las filas de datos
        escritor.writerows(datos_csv)

    print('='*36)
    print(f"Archivo CSV generado: {nombre_archivo}")
    return datos_csv, coordenadas, forms_tipo
# %%
ejecutar()