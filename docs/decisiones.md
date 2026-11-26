# Registro de decisiones

## 001 · Producto y dataset de la Fase 1

- **Fecha:** 2026-11-02
- **Estado:** aceptada; consecuencias corregidas en la 002

**Contexto.** El sistema necesita un dataset público que localice los defectos (cajas o polígonos), no solo que clasifique la pieza como buena o mala, y un producto fácil de conseguir para crear un conjunto de prueba propio.

**Opciones valoradas.**
- Limón: *Lemons quality control dataset* (SoftwareMill), 2.690 imágenes con regiones de defecto en formato COCO, licencia MIT.
- Naranja, tomate y manzana: datasets públicos sobre todo de clasificación (bueno/malo), o de detección de la fruta entera sin localizar el defecto.

**Decisión.** Limón, con el *Lemons quality control dataset*.

**Consecuencias.**
- Permite clasificación (sano/defectuoso), detección y segmentación de defectos, y detección de anomalías entrenando solo con limones sanos.
- Hay varias fotos de cada limón (`0037_G_I_120_A`: limón 0037, ángulo 120, posición A), así que la división train/val/test se hará por limón para evitar fuga de datos.
- El repositorio original está archivado: se guardará una copia propia del dataset fuera de Git.
- Cita: Adamiak, M. (2020). *Lemons quality control dataset*. SoftwareMill. https://doi.org/10.5281/zenodo.3965568


## 002 · Objetivo del primer modelo

- **Fecha:** 2026-11-26
- **Estado:** aceptada

**Contexto.** El análisis exploratorio (`notebooks/01_eda_limones.ipynb`) mostró que:
- El COCO no conserva las etiquetas de imagen del README (healthy, greening, blurry…).
- Los 117 limones tienen alguna región de defecto, sobre todo `blemish` e `illness`: no hay clase "sano".
- Un limón se identifica por lote + número, no solo por el número.
- El lote G (12 limones, todos con podredumbre) concentra casi todo el moho y se fotografió con menos luz.
- Las regiones de `illness` miden unos 6 px de lado.

**Opciones valoradas.**
- Sano/defectuoso o detección de anomalías con limones sanos: inviables, no hay limones sanos.
- Detección de todos los defectos con YOLO: posible, pero `illness` y `blemish` son demasiado pequeños para un primer modelo.
- Clasificación por imagen de podredumbre (moho o gangrena): 54 de 117 limones y 684 de 2.690 imágenes, con un significado claro (fruta para descarte).

**Decisión.** El primer modelo clasifica cada imagen como "con podredumbre" o "sin podredumbre". La detección de defectos queda para una fase posterior.

**Consecuencias.**
- La división (#7) se hace por limón (`lote_numero`), estratificada por podredumbre y lote.
- La evaluación (#8) incluye métricas por lote y un modelo de control que solo usa el brillo, para detectar si la red aprende la iluminación del lote G en vez del defecto.
- La etiqueta de una imagen no es la de su limón: un limón podrido solo muestra la podredumbre en el 57 % de sus fotos.
- Se descartan `condition` e `image_quality` (8 regiones sueltas). `pedicel` y `artifact` no cuentan como defecto.
- Corrige la 001: no hay limones sanos para clasificar sano/defectuoso ni para detectar anomalías, y el limón se identifica por lote + número.