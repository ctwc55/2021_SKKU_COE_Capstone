import os

def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/google-cloud-speech-cert/skku-coe-capstone-2021-3333962c72ea.json"

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result()

    for result in response.results:
        alternative = result.alternatives[0]
        print("Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
        print("Start time: {}".format(alternative.words[0].start_time.total_seconds()))

    return response

