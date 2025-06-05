from flask import Flask, render_template, request, redirect, send_file
from bs4 import BeautifulSoup
import qrcode
import uuid
import os
import requests
import subprocess
import glob



app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate_qr', methods=["POST"])
def generate_qr():
    data = request.form["qrdata"]
    filename = f"{uuid.uuid4()}.png"
    img = qrcode.make(data)
    img.save(filename)
    return send_file(filename, mimetype="image/png", as_attachment=True)

#=== SPOTIFY ===
@app.route('/spotify', methods=["POST"])
def download_spotify():
    url = request.form.get("url")
    if not url:
        return "No URL provided", 400
    try:
        # Hapus file lama dulu biar ga numpuk
        for f in glob.glob("*.mp3"):
            os.remove(f)

        # Unduh lagu
        result = subprocess.run(["spotdl", url], capture_output=True, text=True)
        print(result.stdout)

        # Cari file MP3 hasil unduhan
        mp3_files = glob.glob("*.mp3")
        if not mp3_files:
            return "Download gagal atau lagu dilindungi DRM.", 500

        return send_file(mp3_files[0], as_attachment=True)

    except Exception as e:
        return f"Error: {e}", 500

#Tiktok

@app.route('/home')
def home():
    return '''
    <h2>Download Video TikTok Tanpa Watermark</h2>
    <form method="POST" action="/tiktok">
        <input type="text" name="url" placeholder="Masukkan link TikTok" required>
        <button type="submit">Download</button>
    </form>
    '''

@app.route('/tiktok', methods=['POST'])
def download_tiktok():
    url = request.form.get('url')
    if not url:
        return "❌ Tidak ada URL TikTok yang diberikan", 400

    try:
        # Hapus file mp4 lama biar gak numpuk
        for f in glob.glob("*.mp4"):
            os.remove(f)

        # Jalankan yt-dlp untuk download video TikTok tanpa watermark
        subprocess.run([
            "yt-dlp", "-o", "tiktok_video.%(ext)s", url
        ], check=True)

        # Cari file hasil download
        files = glob.glob("tiktok_video.*")
        if files:
            return send_file(files[0], as_attachment=True)
        else:
            return "❌ Gagal mendownload video TikTok", 500

    except Exception as e:
        return f"🔥 Terjadi kesalahan: {e}", 500


# === INSTAGRAM ===
@app.route('/instagram', methods=["POST"])
def download_instagram():
    link = request.form.get("iglink")
    if not link:
        return "No Instagram URL provided", 400
    try:
        # Hapus file lama
        for file in glob.glob("instagram_*.*"):
            os.remove(file)

        filename = "instagram_video.%(ext)s"
        subprocess.run(["yt-dlp", "-o", filename, link], check=True)

        # Cari file yang sudah didownload
        downloaded_files = glob.glob("instagram_video.*")
        if downloaded_files:
            return send_file(downloaded_files[0], as_attachment=True)
        else:
            return "Gagal menemukan file video Instagram", 500
    except Exception as e:
        return f"Download gagal: {e}", 500




# === YOUTUBE ===
@app.route('/youtube', methods=["POST"])
def download_youtube():
    link = request.form.get("ytlink")
    if not link:
        return "No YouTube URL provided", 400
    try:
        # Hapus file lama
        for file in glob.glob("youtube_*.*"):
            os.remove(file)

        filename = "youtube_video.%(ext)s"
        subprocess.run(["yt-dlp", "-o", filename, link], check=True)

        # Cari file yang sudah didownload
        downloaded_files = glob.glob("youtube_video.*")
        if downloaded_files:
            return send_file(downloaded_files[0], as_attachment=True)
        else:
            return "Gagal menemukan file video YouTube", 500
    except Exception as e:
        return f"Download gagal: {e}", 500


# === JALANKAN SERVER ===
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4444)
