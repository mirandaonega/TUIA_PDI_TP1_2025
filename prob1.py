# %%
import cv2
import matplotlib.pyplot as plt
import numpy as np
from roipoly import RoiPoly     # https://pypi.org/project/roipoly/


# %%

url = '/home/jere/tuia/pdi/TUIA_PDI_TP1_2025/Imagen_con_detalles_escondidos.tif'

img = cv2.imread(url, cv2.IMREAD_GRAYSCALE)

shape = img.shape


# %%
def ecualizacion_local(img: np.array, size: tuple, border_type: str):
    """
    Parameters:
        img: Input grayscale image
        size: Tuple (m, n):
                m --> filas (filas/alto de w)
                n --> columnas (columnas/ancho de w)
    
    Returns:
        img_nueva: Imagen con la ecualización local hecha
    """
    m = size[0]
    n = size[1]
    
    # Ensure m and n are odd (so we have a clear center pixel)
    m = m + 1 if m % 2 == 0 else m
    n = n + 1 if n % 2 == 0 else n
    
    # Calculate half-sizes for border and center indexing
    alto = m // 2
    ancho = n // 2

    shape = img.shape
    alto_img = shape[0]
    ancho_img = shape[1]

    border_map = {
        "BORDER_CONSTANT": cv2.BORDER_CONSTANT,
        "BORDER_REFLECT": cv2.BORDER_REFLECT,
        "BORDER_REFLECT_101": cv2.BORDER_REFLECT_101,
        "BORDER_REPLICATE": cv2.BORDER_REPLICATE,
        "BORDER_WRAP": cv2.BORDER_WRAP,
    }

    if border_type not in border_map:
        raise ValueError(f"Tipo de borde '{border_type}' no válido. Opciones: {list(border_map.keys())}")

    # Add border to handle edge pixels
    img_resized = cv2.copyMakeBorder(img, alto, alto, ancho, ancho, borderType=border_map[border_type])
    img_nueva = np.zeros(shape, dtype=np.uint8)

    # Display original image
    plt.figure()
    plt.subplot(121)
    plt.imshow(img, cmap='gray')
    plt.title('Imagen Original')
    plt.xticks([]), plt.yticks([])

    # Apply local histogram equalization
    for i in range(alto_img):
        for j in range(ancho_img):
            # Extract local window
            crop = img_resized[i:i+m, j:j+n]
            # Apply histogram equalization to the window
            crop_eq = cv2.equalizeHist(crop)
            # Take the center pixel value from the equalized window
            img_nueva[i, j] = crop_eq[alto, ancho]

    # Display result
    plt.subplot(122)
    plt.imshow(img_nueva, cmap='gray')
    plt.title('Ecualización Local')
    plt.xticks([]), plt.yticks([])
    plt.show(block=False)

    return img_nueva

# %%
# Probamos con varios bordes y máscaras, me qué con una que va bien.
# Estaría bueno probar con más de una no cuadrada

# border_map = {
#     "BORDER_CONSTANT": cv2.BORDER_CONSTANT,
#     "BORDER_REFLECT": cv2.BORDER_REFLECT,
#     "BORDER_REFLECT_101": cv2.BORDER_REFLECT_101,
#     "BORDER_REPLICATE": cv2.BORDER_REPLICATE,
#     "BORDER_WRAP": cv2.BORDER_WRAP,
# }

# for border in border_map:
#     print('='*12)
#     print("Tipo de borde:", border)
#     print('='*12)

#     for i in range(50):
#         print("Tamaño de la ventana:", i)
#         ecualizacion_local(img, (i,i), border)

ecualizacion_local(img, (25,25), 'BORDER_REPLICATE')
ecualizacion_local(img, (20,35), 'BORDER_REPLICATE')



