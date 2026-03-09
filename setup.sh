#!/bin/bash

echo "🚀 Iniciando Configuración: F.R.I.D.A.Y. (Claude MX Edition)"

mkdir -p models downloads

# Descargar modelo Claude de México si no existe
if [ ! -f "models/friday.onnx" ]; then
  echo "🎙️ Descargando voz de Claude (MX)..."
  curl -L https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/claude/low/es_MX-claude-low.onnx -o models/friday.onnx
  curl -L https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/claude/low/es_MX-claude-low.onnx.json -o models/friday.onnx.json
else
  echo "✅ El sistema de voz ya está configurado."
fi

chmod +x setup.sh
echo "✔️ Listo. Ejecuta 'python main.py' para iniciar el sistema."
