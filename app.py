from flask import Flask, render_template, request
from dotenv import load_dotenv
from google.cloud import storage
import os
import subprocess
from google.cloud.storage import bucket
import yt_dlp
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
        link = val["url"]

        video_id = link.split('v=')[-1]

        remain_files = [file for file in os.listdir('./') if file.endswith('.wav')]
        for file in remain_files:
            os.remove(file)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '320',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        old_filename = [file for file in os.listdir('./') if file.endswith('.wav')]
        os.rename(old_filename[0], 'sample.wav')

        subprocess.call("ffmpeg -i sample.wav -ar 16000 -ac 1 audiofile.wav", shell=True)

        load_dotenv()

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_KEY_PATH")

        bucket_name = os.environ.get("BUCKET_NAME")
        source_file_name = os.environ.get("FILE_LOCATION")
        destination_blob_name = "audiofile.wav"

        storage_client = storage.Client()
        buckets = storage_client.bucket(bucket_name)
        blob = buckets.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        yt_tnt, uttered_text = yt.transcribe_gcs("gs://skku-coe-capstone-2021/audiofile.wav")

        yt_tnt["video_id"] = video_id

        tcn = yt.get_common_nouns(uttered_text)

        subprocess.call("rm sample.wav", shell=True)
        subprocess.call("rm audiofile.wav", shell=True)

    return render_template('yt.html', result = yt_tnt, tcn = tcn)


if __name__ == '__main__':
    app.run(host='0.0.0.0')