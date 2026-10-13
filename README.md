# Simulación_BIOS

Simulador visual del funcionamiento de BIOS/UEFI y diagnóstico de hardware. Desarrollado con Python + PySide6.

## Estructura del proyecto

```
Simulación_BIOS/
├── core/          # Lógica: POST, diagnóstico, componentes, estados
├── hardware/      # Módulos específicos de hardware
├── ui/            # Interfaz gráfica (ventanas, vistas)
├── styles/        # QSS (tema BIOS/UEFI)
├── resources/     # Iconos e imágenes
│   ├── icons/     # SVGs minimalistas para componentes
│   └── images/
├── tests/         # Pruebas
├── main.py        # Punto de entrada
├── requirements.txt
└── .gitignore
```

## Componentes con iconos

- Procesador (`procesador.svg`)
- Memoria RAM (`memoria_ram.svg`)
- Tarjeta gráfica (`tarjeta_grafica.svg`)
- Placa base (`placa_base.svg`)
- Almacenamiento (`almacenamiento.svg`)
- Ventiladores (`ventiladores.svg`)
- Puertos USB (`puertos_usb.svg`)
- Red (`red.svg`)

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Notas

Los SVGs usan `stroke="currentColor"` para permitir tintado dinámico según estado (funcional/precaución/falla) desde QSS.
