#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pydub import AudioSegment
import os
import base64

#인풋받아오기!!!

#인풋으로 base64 코드 저장된 txt의 이름/ 음원길이 / 멤버별 파트 list
#base_mp3_file = input()
#end_time = input()
#member_part = input() //이부분 사실 잘 모르겠....

base_mp3_file = "badboy_base64.txt"
end_time = 237
member_part = [[5.05,50.25],[72,100]]

#멤버별 파트 set list를 리스트화 시키기
timetrack = [0]

#print(len(member_part))
for i in range(len(member_part)):
  timetrack.append(list(member_part)[i][0]*1000)
  timetrack.append(list(member_part)[i][1]*1000)

timetrack.append(end_time*1000)
print(timetrack)

print("음원 저장 완료")

#새로운 mp3 저장용 파일
mp3_file = open("soundtrack.mp3", "wb")
#받아온 base64 코드 디코딩하기
decode_string = base64.b64decode(open(base_mp3_file, "rb").read())
#mp3 파일 아예 저장하기-아몰랑 일단 저장해
mp3_file.write(decode_string)

print("음원 저장 완료")

#음원 편집 용 파트!!!!
# Opening file and extracting segment
song = AudioSegment.from_file("soundtrack.mp3" )
print("음원 열람 완료")


for i in range(len(timetrack)-1):
  #timetrack에서 index 0부터 (0,1) (1,2) ... 식으로 잘라내고 saving 까지
  extract = song[timetrack[i]:timetrack[i+1]]
  #저장명은 곡명-extract+몇번째조각인지.mp3
  extract.export("soundtrack"+str(i)+".mp3", format="mp3")
  print(str(i)+"번째 조각 잘라내기")
  #if i == len(timetrack):
  #  print(a)
    #break

print("음원 segment 잘라내기 완료")

#extract = song[startTime:endTime]
# Saving
#extract.export( file_name+'-extract.mp3', format="mp3")

