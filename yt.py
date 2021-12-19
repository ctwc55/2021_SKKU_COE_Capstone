import os
import re
from konlpy.tag import Okt
from collections import Counter

def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_KEY_PATH")

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        profanity_filter=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result()

    yt_tnt = {}
    uttered_texts = ""

    for result in response.results:
        alternative = result.alternatives[0]

        transcript = result.alternatives[0].transcript
        uttered_texts += transcript
        transcripts = [x.strip() for x in re.split("[.!?]", transcript)]
        del transcripts[-1]

        time_idx = 0
        for text in transcripts:
            start_times = alternative.words[time_idx].start_time.total_seconds()
            yt_tnt["%02d:%02d"%(int(start_times//60),int(start_times%60))] = text+transcript[transcript.find(text)+len(text)]
            time_idx += len(text.split())
            print("%02d:%02d"%(int(start_times//60),int(start_times%60)),text+transcript[transcript.find(text)+len(text)])


        print("Transcript: {}".format(transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
        print("Start time: {}".format(alternative.words[0].start_time.total_seconds()))


        #time_info = alternative.words[0].start_time.total_seconds() 
        #yt_tnt[f"{int(time_info//60)}:{int(time_info%60)}"] = result.alternatives[0].transcript

    return yt_tnt, uttered_texts


def get_common_nouns(uttered_text):
    okt = Okt()
    noun = okt.nouns(uttered_text)
    for i, n_len in enumerate(noun):
        if len(n_len) < 2:
            noun.pop(i)
    
    count = Counter(noun)

    three_common_nouns = count.most_common(3)
    print(three_common_nouns)

    tcn = {}
    for i,noun in enumerate(three_common_nouns):
        tcn[f"tcn{i}"] = noun[0]

    return tcn