from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
from threading import Thread

# Inicializar Flask y cargar el modelo Whisper
app = Flask(__name__)
CORS(app)  # Permite peticiones desde cualquier origen
model = whisper.load_model("small")  # Usa "tiny", "small", etc., si prefieres otros tamaños

@app.route("/transcribe", methods=["POST"])
def transcribe():
    # Verifica que se haya enviado un archivo
    if "file" not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400

    file = request.files["file"]
    file_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)  # Crea el directorio temporal si no existe
    file.save(file_path)  # Guarda el archivo en el servidor

    try:
        # Transcribir el archivo de audio
        result = model.transcribe(file_path)
        os.remove(file_path)  # Limpia el archivo temporal
        return jsonify({"text": result["text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ejecutar Flask (sin hilos adicionales, Render lo manejará)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
