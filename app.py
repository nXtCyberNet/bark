from flask import Flask, request, send_file, jsonify
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import os

# Preload Bark models
preload_models()

# Initialize Flask app
app = Flask(__name__)

@app.route("/generate-audio", methods=["POST"])
def generate_audio_endpoint():
    """
    Generate an audio file from the provided text and return it for download.
    """
    try:
        # Get JSON data
        data = request.json
        text_prompt = data.get("text", "")

        if not text_prompt:
            return jsonify({"error": "Text prompt is required"}), 400

        # Generate audio
        audio_array = generate_audio(text_prompt)

        # Save the file
        filename = "bark_generation.wav"
        write_wav(filename, SAMPLE_RATE, audio_array)

        # Return the file as a response
        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return """
    <h1>Welcome to the Audio Generator API</h1>
    <p>Use the endpoint <code>/generate-audio</code> to generate a WAV file.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
