from twilio.rest import Client
import requests

# Twilio account credentials
account_sid = "AC58c72fb9cc90d1aed4c8f618d5c42b2e"
auth_token = "bf90502fa03b42bc6eb3b1b4d8e240e0"
client = Client(account_sid, auth_token)

# Get recording URL
recording_sid = 'RE7717eaee16c796127bf6814c508e1585'  # Replace with the SID of the recording you want to get the URL for

calla = 'CA3c03136ef7b2af8b40398384029252ab'

recordings = client.recordings.list(call_sid=calla)

tamano = len(recordings)
print('El tamaño es: ', tamano)

recording = recordings[0]
recording_sid = recording.sid

print("la ultima llamada es: ", recording_sid)           

# Construct the recording URL
recording_url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Recordings/{recording_sid}.wav'

# Download the recording
response = requests.get(recording_url, auth=(account_sid, auth_token))

# Save the recording to a file
filename = f'{recording_sid}.wav'
with open(filename, 'wb') as file:
    file.write(response.content)

print(f'Recording downloaded and saved as {filename}')


