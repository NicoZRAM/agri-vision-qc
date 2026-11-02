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