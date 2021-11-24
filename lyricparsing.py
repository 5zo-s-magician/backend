# %%
import urllib.request #웹에 접근하기 위한 모듈
from bs4 import BeautifulSoup as bs #웹 크롤링을 위한 모듈
import re
import traceback
import sys
import ssl

def second_to_float(second_string):
      #second_string = 00:00.00
  minute = int(second_string[0:2])
  second = float(second_string[3:8])

  seconds = 60*minute + second
  return round(seconds, 2)

def lyric_parsing(wav_title, wav_seconds):
  print(wav_seconds, wav_title)
  # wav_title = input()
  # wav_seconds = input()
  #wav_title = 'bae bae'
  #wav_seconds = 170

  # akmu give love 230
  # bae bae 170
  # bts idol 230
  # bang bang ariana 200
  # bigbang blue 242
  # bigbang badboy 237
  # what makes you beautiful 200
  # love the way you lie 263

  wav_title = wav_title.replace(" ", "+")
  print(wav_title)

  LYRICS_URL = "https://www.megalobiz.com/search/all?qry=" + wav_title + "&searchButton.x=0&searchButton.y=0" #주소설정
  ssl._create_default_https_context = ssl._create_unverified_context
  context = ssl._create_unverified_context()

  response = urllib.request.urlopen(LYRICS_URL, context=context)
  LYRICS_HTML = response.read()
  soup = bs(LYRICS_HTML)
  # soup

  all_tr = soup.findAll('div', attrs={'class', 'entity_full_member_box'})
  # all_tr
  # print(len(all_tr))

  for tr in all_tr:
    try:
      get_time = tr.find('a', attrs={'class', 'entity_name'})
      tmp_str = get_time.contents[-1]
      time_str = tmp_str.split('[')
      # print(len(time_str[1]))
      if len(time_str[1]) < 25:
        real_time = time_str[1].split(']')
        real_time = real_time[0]
        # print(real_time)
        minute = real_time.split(':')
        # print(minute[0])
        # print(minute[1])
        total_seconds = float(minute[0])*60.0 + float(minute[1])
        # print(total_seconds)

        if total_seconds > wav_seconds - 3 and total_seconds < wav_seconds + 3:
          get_detail = tr.find('div', attrs={'class', 'details'})
          get_lyrics = get_detail.findAll('div')
          get_lyric = get_lyrics[1].find('span')
          # print("#########")
          # print(get_lyric.contents[0])
          first_line = get_lyric.contents[0]
          second_line = get_lyric.contents[1]
          third_line = get_lyric.contents[2]
          # print(second_line)
          # print(third_line)

          # print(str(first_line)[1] != '0' and str(first_line)[0:4] != "<br/")
          # print(str(second_line)[1] != '0' and str(second_line)[0:4] != "<br/")
          # print(str(third_line)[1] != '0' and str(third_line)[0:4] != "<br/")
          # print(str(third_line)[0] != '\n')
          # print(str(third_line)[0:4])
          if (str(first_line)[1] != '0' and str(first_line)[0:4] != "<br/" and (str(first_line)[0] != '\n' or (str(first_line)[0] == '\n' and str(first_line)[2] != '0'))) or (str(second_line)[1] != '0' and str(second_line)[0:4] != "<br/" and (str(second_line)[0] != '\n' or (str(second_line)[0] == '\n' and str(second_line)[2] != '0'))) or (str(third_line)[1] != '0' and str(third_line)[0:4] != "<br/" and (str(third_line)[0] != '\n' or (str(third_line)[0] == '\n' and str(third_line)[2] != '0'))):
            lyric_link = get_time.get('href')
            lyric_code = get_time.get('href').split('.')
            lyric_code = lyric_code[-1]
            # print(lyric_code)

            lyric_link = "https://www.megalobiz.com" + lyric_link
            # print(lyric_link)
            response2 = urllib.request.urlopen(lyric_link)
            LYRIC_HTML = response2.read()
            soup2 = bs(LYRIC_HTML)
            # print(soup2)

            # all_lyrics = soup2.find('span', attrs={'id', 'lrc_'+lyric_code+'_lyrics'})
            all_lyrics = soup2.find('div', attrs={'class', 'lyrics_details entity_more_info'})
            # print("길이: "+ len(all_lyrics.contents))
            count = 1
            for all_lyric in all_lyrics.contents:
              # final_dic = {'수현':[], '찬혁':[], '찬혁, 수현': []}
              final_dic = {}

              # print(all_lyric)
              tmp_lyrics_string = str(all_lyric)
              if '<font color' in tmp_lyrics_string: # 폰트색으로 파트 나뉘어져있을 때
                tmp_member = ''
                member_list = []
                second_list = []
                tmp_lyrics_list = []
                tmp_lyrics_list = tmp_lyrics_string.split('[')
                start_index = 0
                end_index = 0
                i = 0
                for line in tmp_lyrics_list:
                  # print(line)
                  if(line[0] == '0'):
                    second = line[0:8]
                    second_list.append(second_to_float(second))
                  m = re.search('<font color="#CD850D">(.+?)</font>', line)
                  # if tmp_member != '':
                  if m:
                    found = m.group(1)
                    member_list.append(found)

                    if((tmp_member!='' and tmp_member != found) or (tmp_member != '' and '<span/>' in line) ):
                      print(tmp_member)
                      end_index = i
                      if(not(tmp_member in final_dic)):
                        print("hi")
                        final_dic[tmp_member] = []
                      final_dic[tmp_member].append([second_list[start_index], second_list[end_index]])
                      print(str(second_list[start_index]) + ' ~ ' + str(second_list[end_index]))
                      start_index = i

                    tmp_member = found
                    i = i + 1
                  else:
                    if(tmp_member != ''):
                      if('</span>' in line):
                        print(tmp_member)
                        end_index = i
                        if(not(tmp_member in final_dic)):
                          print("hi")
                          final_dic[tmp_member] = []
                        final_dic[tmp_member].append([second_list[start_index], second_list[end_index]])
                        print(str(second_list[start_index]) + ' ~ ' + str(second_list[end_index]))
                        
                        start_index = i
                      else:
                        member_list.append(tmp_member)
                        i = i + 1


                member_set = set(member_list)
                member_list2 = list(member_set)
                print(member_list2)
                print(member_list)
                print(second_list)
                print(final_dic)

              else: # 문단별로 파트가 나뉘어져 있을 때
                # print(tmp_lyrics_string)
                tmp_member = ''
                member_list = []
                second_list = []
                tmp_lyrics_list = []
                tmp_lyrics_list = tmp_lyrics_string.split('<br/>')
                start_index = 0
                end_index = 0
                i = 0
                for line in tmp_lyrics_list:
                  print(line)
                  if(line[1:3] == '[0'):
                    second = line[2:10]
                    second_list.append(second_to_float(second))
                  # m = re.search('[(.+?)]', line)
                  # found = m.group(1)
                  # if tmp_member != '':
                  if not('[al:' in line) and not('[ti:' in line) and not('[re:' in line) and not('[ve:' in line) and not('[leng' in line) and not('[by:' in line) and not('<span' in line) and not('[0' in line):
                    member_list.append(line)

                    if((tmp_member!='' and tmp_member != line) or (tmp_member != '' and '<span/>' in line) ):
                      # print(tmp_member)
                      end_index = i - 1
                      if(not(tmp_member in final_dic)):
                        # print("hi")
                        final_dic[tmp_member] = []
                      print(tmp_member)
                      # print(second_list)
                      # print(start_index)
                      # print(end_index)
                      final_dic[tmp_member].append([second_list[start_index], second_list[end_index]])
                      print(str(second_list[start_index]) + ' ~ ' + str(second_list[end_index]))
                      start_index = i

                    tmp_member = line
                    if(line[1:3] == '[0'):
                      i = i + 1
                  else:
                    if(tmp_member != ''):
                      if('</span>' in line):
                        print(tmp_member)
                        end_index = i - 1
                        if(not(tmp_member in final_dic)):
                          # print("hi")
                          final_dic[tmp_member] = []
                        final_dic[tmp_member].append([second_list[start_index], second_list[end_index]])
                        print(str(second_list[start_index]) + ' ~ ' + str(second_list[end_index]))
                        
                        start_index = i
                      else:
                        member_list.append(tmp_member)
                        if(line[1:3] == '[0'):
                          i = i + 1

              
                member_set = set(member_list)
                member_list2 = list(member_set)
                print(member_list2)
                print(member_list)
                print(second_list)
                print(final_dic)

              if final_dic != {}:
                return final_dic 
    except Exception as e:
      print(traceback.format_exc())
      pass
  