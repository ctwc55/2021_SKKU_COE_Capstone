from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import subprocess
import youtube_dl
import yt

#flask run --host=0.0.0.0 --port=5000
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/yt", methods = ['POST', 'GET'])
def yt_to_text():
    if request.method == 'POST':
        val = request.form
        print(val)
        link = val["url"]
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '320',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        old_filename = [file for file in os.listdir('./') if file.endswith('.wav')]
        os.rename(old_filename[0], 'sample.wav')

        subprocess.call("ffmpeg -i sample.wav -ar 16000 -ac 1 audiofile.wav", shell=True)

        load_dotenv()

        OBJECT_LOCATION = "/home/ubuntu/Projects/2021_SKKU_COE_Capstone/audiofile.wav"
        OAUTH2_TOKEN = os.environ.get("OAUTH2_TOKEN")
        OBJECT_CONTENT_TYPE = "audio/x-wav"
        BUCKET_NAME = "skku-coe-capstone-2021"
        OBJECT_NAME = "audiofile.wav"
        subprocess.call(f"curl -X POST --data-binary @{OBJECT_LOCATION} -H \"Authorization: Bearer {OAUTH2_TOKEN}\" -H \"Content-Type: {OBJECT_CONTENT_TYPE}\" \"https://storage.googleapis.com/upload/storage/v1/b/{BUCKET_NAME}/o?uploadType=media&name={OBJECT_NAME}\"", shell=True)

        yt.transcribe_gcs("gs://skku-coe-capstone-2021/audiofile.wav")

        subprocess.call("rm sample.wav", shell=True)
        subprocess.call("rm audiofile.wav", shell=True)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')