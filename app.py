from flask import Flask, render_template, request
import os
import subprocess
import youtube_dl

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
        os.rename(old_filename[0], 'audiofile.wav')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')