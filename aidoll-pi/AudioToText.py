import boto3
import time
import requests

class AudioTranscriber:
    def __init__(self, bucket_name, region='ap-southeast-2'):
        self.bucket_name = bucket_name
        self.region = region
        self.s3 = boto3.client('s3')
        self.transcribe = boto3.client('transcribe', region_name=region)

    def upload_audio(self, local_file_path, s3_key):
        self.audio_file = local_file_path
        self.s3_key = s3_key
        self.s3.upload_file(local_file_path, self.bucket_name, s3_key)
        print(f"Uploaded {local_file_path} to s3://{self.bucket_name}/{s3_key}")

    def start_transcription(self, job_name, media_format='m4a', language_code='zh-TW'):
        self.job_name = job_name
        self.transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{self.bucket_name}/{self.s3_key}'},
            MediaFormat=media_format,
            LanguageCode=language_code
        )
        print(f"Started transcription job: {job_name}")

    def wait_for_completion(self):
        print("Waiting for transcription to complete...")
        while True:
            status = self.transcribe.get_transcription_job(TranscriptionJobName=self.job_name)
            state = status['TranscriptionJob']['TranscriptionJobStatus']
            if state in ['COMPLETED', 'FAILED']:
                break

        self.transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        # print(f"Transcription {state}: {self.transcript_file_uri}")
        return state

    def get_transcribed_text(self):
        response = requests.get(self.transcript_file_uri)
        result_json = response.json()
        text = result_json['results']['transcripts'][0]['transcript']
        # print("Transcribed Text:", text)
        return text

    def delete_transcription_job(self):
        self.transcribe.delete_transcription_job(TranscriptionJobName=self.job_name)
        print(f"Deleted transcription job: {self.job_name}")

