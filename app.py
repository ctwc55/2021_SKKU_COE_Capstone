from flask import Flask, render_template
import subprocess
import youtube_dl

#flask run --host=0.0.0.0 --port=5000
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/yt")
def yt_to_text():
    link="https://www.youtube.com/watch?v=fz8QtmDztSo"
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


if __name__ == '__main__':
    app.run(host='0.0.0.0')