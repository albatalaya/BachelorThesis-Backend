# BachelorThesis:Backend
Backend of the app.
Sound analysis in Python to detect approaching vehicles through the audio that the Frontend sends.

## About the thesis
### OPTICAL WARNING OF BICYCLE RIDERS CONCERNING MOTORIZED VEHICLES CLOSING FROM BEHIND USING THE SMARTPHONE'S MICROPHONE
Deaf cyclists do not receive acoustic warnings of motor vehicles approaching from behind. This can be very dangerous because they can get startled and wobble, making them loose stability and more exposed to possible accidents. 
The purpose of this thesis is a proof of concept, not a product. The aim is to investigate whether it is possible to detect approaching vehicles with a smartphone microphone through an app and to announce them visually to the deaf cyclist through AR-glasses.
The result of the work is a smartphone app, developed in Ionic/Angular, that detects approaching vehicles through a local server coded in Python/Flask, and displays a visual warning on AR-glasses via wireless connection to the smartphone. The final accuracy of the detection is of 87%.

## Video Demo
https://www.youtube.com/watch?v=WKyUsdZbQ0Y

## Built with
- Python
- Flask

## Getting started
### Prerequisites
Python
### Server
* Clone this repository: `git clone https://github.com/albatalaya/BachelorThesis-Backend.git`.
* Install [ffmpeg](https://www.ffmpeg.org/) and copy/paste the ffmpeg.exe and ffprobe.exe in the same folder as the server.py
* Run `pip install Flask` to install Flask.
* Run `python server.py` on the root folder

## Frontend and Sound Analysis Repositories
https://github.com/albatalaya/BachelorThesis-Frontend <br/>
https://github.com/albatalaya/BachelorThesis-SoundAnalysis

## Written Document
The Written document with the final report of my Bachelor Thesis, can be found inside this folder with the name "Bachelor Thesis - Alba Talaya Vidal.pdf".

2022, Vienna
