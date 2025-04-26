import requests
import json

base_url="https://persona-sound.data.gamania.com/api/v1/public/voice"
speaker="puyang"

url = "https://persona-sound.data.gamania.com/api/v1/public/voice?speaker_name=puyang&text=%E4%BD%A0%E5%A5%BD&model_id=6&mode=file"

payload = {}
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhd3NfaGFja2F0aG9uIiwiZXhwaXJlcyI6MTc0NTc0ODAwMH0.9qpg1xraE_d_Hua2brAmCfRlQSce6p2kdipgq8j1iqo'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)