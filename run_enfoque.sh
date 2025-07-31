#!/bin/bash

############################################################
# SCRIPT DE INICIO PARA TEST DE ENFOQUE - UBUNTU
# Autor: Francisco Martínez Puchades
# Fecha: Julio 2025
# Descripción: Ejecuta el test de enfoque con OpenCV en entorno X11.
############################################################

# --- Paso 1: Clonar el repositorio (si aún no lo tienes) ---
# git clone https://github.com/fm-puchades/test_enfoque.git
# cd test_enfoque

# --- Paso 2: Instalar dependencias necesarias ---
# Solo necesitas hacer esto una vez (requiere Python 3.8+)
# sudo apt update
# sudo apt install python3-pip -y
# pip install --user opencv-python numpy requests

# --- Paso 3: Establecer entorno gráfico clásico (opcional si usas Wayland) ---
export QT_QPA_PLATFORM=xcb

# --- Paso 4: Ejecutar el script principal ---
echo "---------------------------------------------"
echo "  Ejecutando Test de Enfoque (Versión CLI)  "
echo "---------------------------------------------"

cd ~/test_enfoque
python3 enfoque.py

echo "---------------------------------------------"
echo "  Test de enfoque finalizado"
echo "---------------------------------------------"
