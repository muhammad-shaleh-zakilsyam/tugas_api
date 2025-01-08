from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Konfigurasi API Hugging Face
HF_API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HF_API_KEY = "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"  # Ganti dengan API key Anda

# Fungsi untuk memanggil API Hugging Face
def query_huggingface(payload):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    return response.json()

# Fungsi untuk membersihkan respons (menghapus pengulangan pertanyaan)
def clean_response(response_text, user_input):
    # Cek jika respons mengulang pertanyaan dan hapus bagian tersebut
    if response_text.lower().startswith(user_input.lower()):
        # Menghapus bagian yang mengulang pertanyaan
        return response_text[len(user_input):].strip()
    return response_text

# Route untuk halaman utama
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint untuk chatbot
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "Message is required"}), 400
    
    # Menambahkan prompt agar chatbot berperan sebagai Naruto
    prompt = (
        f"Anda asisten virtual jawablah pertanyaan berikut."
        f"{user_input}"
    )
    
    # Kirim permintaan ke API Hugging Face dengan prompt baru
    response = query_huggingface({"inputs": prompt})
    
    # Pastikan response bukan list kosong
    if isinstance(response, list) and response:
        bot_reply = response[0].get("generated_text", "Saya tidak tahu bagaimana menjawab itu.")
    else:
        bot_reply = "Saya tidak tahu bagaimana menjawab itu."

    # Membersihkan respons jika mengulang pertanyaan
    cleaned_reply = clean_response(bot_reply, user_input)

    return jsonify({"reply": cleaned_reply})

# Jalankan aplikasi Flask
if __name__ == "__main__":
    app.run(debug=True)
