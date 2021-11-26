#!/usr/bin/env python
# coding: utf-8

from pydub import AudioSegment
import os
import base64
from mutagen.mp3 import MP3
from IPython.display import Audio

def audio_cut(base_mp3_file, member_part):
  #인풋받아오기!!!

  #인풋으로 base64 코드 저장된 txt의 이름/ 음원길이 / 멤버별 파트 list
  # base_mp3_file = input()
  # end_time = input()
  # member_part = input() #이부분 사실 잘 모르겠....

  #base_mp3_file = "badboy_base64.txt"
  #end_time = 237
  #member_part = [[5.05,50.25],[72,100]]


  #print("음원 저장 완료")

  #새로운 mp3 저장용 파일
  mp3_file = open("soundtrack.mp3", "wb")
  #받아온 base64 코드 디코딩하기
  decode_string = base64.b64decode(open(base_mp3_file, "rb").read())
  #mp3 파일 아예 저장하기-아몰랑 일단 저장해
  mp3_file.write(decode_string)
  audio = MP3("soundtrack.mp3")
  end_time =  audio.info.length
  mp3_file.close()

  #print("음원 저장 완료")

  # 멤버별 파트 set list를 리스트화 시키기
  timetrack = [0]

  #print(len(member_part))
  for i in range(len(member_part)):
    timetrack.append(list(member_part)[i][0]*1000)
    timetrack.append(list(member_part)[i][1]*1000)

  timetrack.append(end_time*1000)
  print(timetrack)


  # In[57]:


  #음원 편집 용 파트!!!!
  # Opening file and extracting segment
  # AudioSegment.converter = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"
  # AudioSegment.ffmpeg = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"
  # AudioSegment.ffprobe = "C:\\Program Files\\ffmpeg\\bin\\ffprobe.exe"
  song = AudioSegment.from_file("soundtrack.mp3")

  #print("음원 열람 완료")


  for i in range(len(timetrack)-1):
    #timetrack에서 index 0부터 (0,1) (1,2) ... 식으로 잘라내고 saving 까지
    extract = song[timetrack[i]:timetrack[i+1]]
    #저장명은 곡명-extract+몇번째조각인지.mp3
    extract.export("soundtrack"+str(i)+".mp3", format="mp3")

  # print(str(i)+"번째 조각 잘라내기")
    if i == len(timetrack):
      break

  #print("음원 segment 잘라내기 완료")

  #extract = song[startTime:endTime]
  # Saving
  #extract.export( file_name+'-extract.mp3', format="mp3")


  # In[ ]:


  for i in range(len(timetrack)-1):
    if i % 2 == 1:
      str1 = "soundtrack"+str(i)+".mp3"
      Audio(str1)
      os.system("python -m spleeter separate -h")
      os.system("python -m spleeter separate -o output/"+str1)
  print("끝")

  # 이렇게 하면               output/benatural/vocals.wav
  # 홀수번째 파일에 대해서만  output/benatural/accompaniment.wav 파일 두개 생김


  # In[84]:


  #위에 애들을 voice conversion에 넣어주려고 저장하는 코드..!!!!

  for g in range(len(timetrack)-1):
  #g = 0 
    if g % 2 == 1:
      file_name = "soundtrack"+str(g)
      vocals = AudioSegment.from_file("output/"+file_name+"/vocals.wav")
      extract.export( file_name+'-vocals.wav', format="wav")

      mrs = AudioSegment.from_file("output/"+file_name+"/accompaniment.wav")
      extract.export( file_name+'-mrs.wav', format="wav")
  return timetrack
