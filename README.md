## Ejecución

### Problema 1: Ecualización Local de Histograma

Este script aplica ecualización local de histograma a la imagen `Imagen_con_detalles_escondidos.tif` para revelar detalles ocultos.

```bash
python prob1.py
```

El script:
- Carga la imagen con detalles escondidos
- Aplica ecualización local con diferentes tamaños de ventana
- Muestra las imágenes procesadas con matplotlib

### Problema 2: Validación de Formularios

Este script procesa y valida 5 formularios escaneados, detectando errores en los campos completados.

```bash
python prob2.py
```

El script:
- Procesa los formularios `formulario_01.png` a `formulario_05.png`
- Valida cada campo según reglas específicas (nombre, edad, mail, legajo, etc.)
- Clasifica los formularios por tipo (A, B o C)
- Genera un archivo `data_formularios.csv` con los resultados de validación
- Muestra una visualización con los campos de nombre (invertidos si hay errores)

**Salida**: El archivo `data_formularios.csv` contendrá las validaciones con formato:
```
ID,Nombre y Apellido,Edad,Mail,Legajo,Pregunta 1,Pregunta 2,Pregunta 3,Comentarios
1,OK,OK,MAL,OK,OK,OK,OK,OK
...
```

## Archivos del Proyecto

- `Procesamiento de Imágenes I - Informe TP1.pdf`- Informe
- `prob1.py` - Problema 1: Ecualización local
- `prob2.py` - Problema 2: Validación de formularios
- `formulario_*.png` - Imágenes de formularios a validar
- `Imagen_con_detalles_escondidos.tif` - Imagen para ecualización
- `data_formularios.csv` - Resultado de la validación (generado)
