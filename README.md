# agri-vision-qc

Sistema de inspección visual de calidad para productos agroalimentarios: del dataset a una demo desplegada.

> Estado: en desarrollo.

## Requisitos

- Python 3.12 y [uv](https://docs.astral.sh/uv/)
- GPU opcional: NVIDIA (CUDA) o Apple Silicon (MPS)

## Instalación

```bash
git clone git@github.com:NicoZRAM/agri-vision-qc.git
cd agri-vision-qc
uv sync
```

## Comprobar el dispositivo de cómputo

```bash
uv run python -m agri_vision_qc.device
```

## Datos

El proyecto usa el [Lemons quality control dataset](https://github.com/softwaremill/lemon-dataset) de SoftwareMill (licencia MIT): 2.690 imágenes de limones con regiones de defecto anotadas en formato COCO.

Los datos no se guardan en el repositorio. Para descargarlos y verificarlos:

```bash
uv run python -m agri_vision_qc.data.download
```

El script descarga el ZIP en `data/raw/`, comprueba su huella SHA-256 y verifica que todas las imágenes de las anotaciones están en disco.

> Adamiak, M. (2020). *Lemons quality control dataset*. SoftwareMill. https://doi.org/10.5281/zenodo.3965568
