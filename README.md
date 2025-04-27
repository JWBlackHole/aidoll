# Aidoll Mobile App

This is the mobile application for the Aidoll product, allowing users to interact with the AI-powered doll via Bluetooth. The app is built using the Kivy framework and provides a simple UI for sending commands to the doll.

## Features

- **Connect to AI Doll**: Establish a Bluetooth connection with the AI doll.
- **Cue Me**: Capture a photo and start recording audio. Tap again to stop recording.
- **Notifications**: Receive notifications from the AI doll.
- **Mute**: Send mute commands to the doll to silence it.

## Requirements

- Python 3
- Kivy
- Android device with Bluetooth support

## How to Run

1. Clone this repository.
2. Install dependencies: `pip install kivy`
3. Run the app: `python main.py`

## Notes

- Ensure Bluetooth permissions are granted on your Android device.
- Replace the placeholder Bluetooth MAC address in `main.py` with your AI doll's address.
