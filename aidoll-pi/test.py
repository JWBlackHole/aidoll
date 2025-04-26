from AudioToText import AudioTranscriber

transcriber = AudioTranscriber(bucket_name='alexisgood')

# transcriber.upload_audio('michelle.m4a', 'audio/input_audio.m4a')
# transcriber.start_transcription(job_name='audio_to_text_job')

transcriber.upload_audio('557.mp4', 'audio/input_audio.mp4')
transcriber.start_transcription(job_name='audio_to_text_job', media_format='mp4', language_code='en-US')

if transcriber.wait_for_completion() == 'COMPLETED':
    text = transcriber.get_transcribed_text()
    print('text:', text)

transcriber.delete_transcription_job()

