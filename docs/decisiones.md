# Registro de decisiones

## 001 · Producto y dataset de la Fase 1

- **Fecha:** 2026-11-02
- **Estado:** aceptada

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