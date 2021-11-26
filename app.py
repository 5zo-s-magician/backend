# from flask import Flask
# app = Flask(__name__)
# @app.route('/')
# @app.route('/home')
# def home():
#     return 'Hello, World!'
# @app.route('/user/<user_name>/<int:user_id>')
# def user(user_name, user_id):
#     return f'Hello, {user_name}({user_id})!'
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
import lyricparsing
import audio_cut
import voice_conversion
import final_mp3
import base64
from mutagen.mp3 import MP3

import wave
import numpy as np
import pytsmod as tsm
import soundfile as sf  # you can use other audio load packages.
import os
from pydub import AudioSegment
import contextlib
import librosa

app = Flask(__name__)
 
@app.route('/', methods = ['POST'])
def getSong():
    #json 데이터를 받아옴
    song = request.get_json()
    song_base64 = song['base64']
    song_name = song['song_name']

    # =-------------------------------------------------------------------------
    # 음원 파일 길이 알아내기
    f = open("base64.txt","w")
    f.write(song_base64)
    f.close()

    mp3_file = open("song.mp3", "wb")
    decode_string = base64.b64decode(open("base64.txt", "rb").read())
    mp3_file.write(decode_string)
    audio = MP3("song.mp3")
    song_length =  audio.info.length

    data = lyricparsing.lyric_parsing(song_name, song_length)
    #data = lyricparsing.lyric_parsing("akmu give love", 230)
    
    return jsonify(data)
 
@app.route('/new_song', methods = ['POST'])
def editSong():
    song = request.get_json()
    member_time = song['time']
    target = song['target']
    base64 = song['base64']

    # 음원 자르고 엠얼 제거
    f = open("base64.txt","w")
    f.write(base64)
    f.close()



    timetrack = audio_cut.audio_cut("base64.txt",member_time)

    # voice conversion
    voice_conversion.voice_conversion(target)

    # 다시 취합
    final_mp3.final_mp3(timetrack)

    return jsonify({})

if __name__ == "__main__":
    app.run(debug=True)

