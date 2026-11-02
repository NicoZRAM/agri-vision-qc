"""Selección y comprobación del dispositivo de cómputo (CUDA, MPS o CPU)."""

import platform

import torch


def get_device() -> torch.device:
    """Devuelve el mejor dispositivo disponible: CUDA, después MPS y, si no, CPU."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def main() -> None:
    device = get_device()
    print(f"Sistema: {platform.system()} {platform.machine()}")
    print(f"PyTorch: {torch.__version__}")
    print(f"Dispositivo: {device}")
    if device.type == "cuda":
        props = torch.cuda.get_device_properties(0)
        print(f"GPU: {props.name}")
        print(f"CUDA (PyTorch): {torch.version.cuda}")
        print(f"Memoria GPU: {props.total_memory / 1024**3:.1f} GB")
    # Prueba real: multiplicación de matrices en el dispositivo elegido
    x = torch.randn(1000, 1000, device=device)
    resultado = (x @ x).sum().item()
    print(f"Prueba de cálculo correcta en {device} (suma = {resultado:.2f})")


if __name__ == "__main__":
    main()