# robocup2023-face-recognition
Facial Recognition using Deepface for EIC RoboCup@Home 2023


## Install
    [Clone and cd to this repo]
    conda create -n face-recog python=3.9.16
    conda activate face-recog
    pip install -r requirements.txt

## Run
### Server
    conda activate face-recog
    python3 main.py
### Live Client
    python3 client_live.py
    [press r and type in name to register face]
