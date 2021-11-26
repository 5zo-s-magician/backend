#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install pydub
#!apt install ffmpeg
from pydub import AudioSegment
# MR+VOCAL overlay


#sound1 = AudioSegment.from_file("/path/to/my_sound.wav")
#sound2 = AudioSegment.from_file("/path/to/another_sound.wav")
#files_path = '/content/drive/MyDrive/capd/'
#file_name = 'badboy' -> 잘라낸 이름 곡명-extract-숫자.mp3
#mr제거 후 생기는 파일  output/잘라낸 이름 곡명-extract-숫자/vocals.wav 랑 accompaniment.wav
#이걸 합쳐서 곡명-extract-숫자-new.mp3로 만든다
def final_mp3(timetrack):
  #수정한 list 다시 받아오기
  #timetrack = input()
  #귀찮으니까 변수화하기
  segment = len(timetrack) -1 

  #조각들 불러와서 바로 append 해주기- 짝수번째 segment는 .mp3 그대로, 홀수번째 segment는 new-voclas.wav 랑 mrs.wav 불러와서 overlay 해주기
  clips = []
  for i in range(segment):
    #file_path_remmr = '/content/output/'
    #file_name_remmr = file_name+'-extract-'+a
    file_name = "soundtrack"+str(i)

    if i % 2 == 0: #mp3 그대로 불러와서 바로 clip에 append 
      clip = AudioSegment.from_file(file_name+".mp3")
      clips.append(clip)
  
    elif i % 2 == 1:
      vocals=AudioSegment.from_file("./voice_conversion_result/voice_conversion_pitch_right/shift_fitch.wav")
      mrs=AudioSegment.from_file(file_name+'-mrs.wav')
      combined = vocals.overlay(mrs)
      #combined.export(file_name_remmr+'-new.mp3',format="mp3")
      clips.append(combined)

  #list화 된 clip들 pydub 이용해서 전체 연결하기
  final_clip = clips[0]
  for i in range(len(clips)):
    final_clip = final_clip + clips[i]

  final_clip.export("final.mp3",format="mp3")

