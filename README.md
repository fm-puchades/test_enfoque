# 🧪 Sistema de Test de Enfoque para Cámaras Industriales CM4

Este repositorio implementa un sistema completo para el **test de enfoque automático y verificación visual** en cámaras utilizadas en procesos de medición y detección de chapas. El sistema permite **capturar imágenes en streaming MJPEG**, aplicar técnicas de análisis de nitidez mediante el **Laplaciano**, y registrar automáticamente los resultados con ROI visuales.

---

## 📁 Estructura del Proyecto

```
├── enfoque.py             # Módulo principal de análisis y testeo de enfoque
├── camera_stream_server.py # Servidor MJPEG de vídeo streaming desde cámara local
├── cliente_cv2.py         # Cliente de prueba: captura y muestra una imagen del stream
├── cartaajuste.png        # Imagen de ajuste inicial para tests (requerida)
├── config.json            # Configuración de stream (opcional)
├── LOG/                   # Carpeta para almacenar capturas registradas
└── modules/               # Carpeta de modulos estandar
   ├── resize_img.py          # Utilidad para reescalar y recortar imágenes manteniendo aspecto
   └── timestamp.py           # Utilidad para generar marcas de tiempo legibles

```

---

## 🧠 Características

- 📷 **Streaming HTTP MJPEG** desde cámara conectada
- 🔍 Detección de enfoque usando **varianza del Laplaciano**
- 🧠 ROI automático y análisis dinámico
- 💾 Registro de capturas etiquetadas (fecha, nitidez, estado)
- 👁️ Cliente ligero para testeo desde red
- 🔧 Adaptable con parámetros por JSON (`config.json`)
- 🔐 Autenticación HTTP básica (usuario: `cameraman`)

---

## ▶️ Ejecución

### 1. Iniciar servidor de streaming:
```bash
python camera_stream_server.py
```
- Dirección: [http://localhost:8000](http://localhost:8000)
- Usuario: `cameraman`, Contraseña: `cam46610`

### 2. Lanzar el test de enfoque:
```bash
python enfoque.py
```

### 3. Cliente remoto simple:
```bash
python cliente_cv2.py
```
Este cliente se conecta al servidor, convierte la imagen a escala de grises y la muestra.

---

## ⚙️ Requisitos

- Python 3.8+
- OpenCV (`opencv-python`)
- Requests
- NumPy

Instalación de dependencias:
```bash
pip install opencv-python numpy requests
```

---

## 📦 Configuración Avanzada

Puedes definir un archivo `config.json` para ajustar:
```json
{
  "params": [
    {
      "url": "http://10.10.51.211:8000/stream.mjpg",
      "varianza": 0.75
    }
  ]
}
```

---

## 🧩 Módulos Clave

- `Enfoque`: Clase principal para iniciar captura, aplicar ROI, calcular enfoque dinámico y registrar.
- `StreamingServer`: Servidor MJPEG con autenticación opcional.
- `resize_img`: Función de recorte proporcional para generar datasets normalizados.
- `timestamp`: Marca de tiempo para registros.

---

## 🧪 Registro y Resultados

Durante el test de enfoque:
- Pulsa `r` para guardar captura en la carpeta `/LOG/`
- Pulsa `q` o `ESC` para salir

Los archivos se guardan como:
```
registo_enfoque_<fecha-hora>.jpg
```

---

## 🧑‍💻 Autor

**Francisco Martínez Puchades**  
📅 Enero 2025  
🔬 TECNOLOGÍA DE CORTE E INGENIERÍA SL

---

## 📜 Licencia

Este proyecto se distribuye bajo licencia privada. Uso exclusivo interno o bajo autorización expresa.
