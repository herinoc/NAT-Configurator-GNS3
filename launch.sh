#!/bin/bash

# Dapatkan path absolut ke direktori ini
BASEDIR="$(cd "$(dirname "$0")" && pwd)"

# Path ke Python dari venv
VENV_PYTHON="$BASEDIR/venv/bin/python"
VENV_PATH="$BASEDIR/venv/bin:$PATH"

# File Python utama
APP="$BASEDIR/app/main.py"

# Pastikan root bisa akses GUI
xhost +SI:localuser:root

# Jalankan aplikasi sebagai root
export QT_QPA_PLATFORM=xcb
sudo --preserve-env=DISPLAY,XAUTHORITY,QT_QPA_PLATFORM PATH=$VENV_PATH $VENV_PYTHON "$APP"

# Hapus akses GUI dari root setelah selesai
xhost -SI:localuser:root
