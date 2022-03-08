# Section13-2
# 업그레읻드 타이핑 게임 제작
# 타이핑 게임 제작 및 기본 완성

import datetime
import csv
import random
import time
# 사운드 출력 필요 모듈
import winsound
import sqlite3
import datetime

# DB 생성 & Auto Commit
# 본인 DB 경로
conn =sqlite3.connect('C:/python_voca/resource.db',isolation_level=None)

# Cursor = conn.cursor()
cursor = conn.cursor()

#  autoincrement 자동으로 1씩 증가하는 시퀀스
cursor.execute('create table IF NOT exists records(id INTEGER PRIMARY KEY AUTOINCREMENT,  cor_cnt INTEGER, record text, regdate text)')

b = [] # 영어 단어 리스트(1000개 로드)

n = 1 # 게임 시도 횟수
cor_cnt = 0 # 정답 개수

with open('./resource/jaresource.csv','r') as f:
    reader = csv.reader(f)
    for c in reader:
        line = []
        line.append(c)
        b.append(line)
words = b




a = input("Enter 누르면 시작\n문제 수: 5개, 제한 시간: 40초, 합격점: 3점 이상") # enter game start!
print(a)

start = time.time()

while n <= 5:
    random.shuffle(words)

    print()

    print("*Question # {}".format(n))
    print(words[0][0][0])    # 문제 출력

    x = input() # 타이핑 입력

    end = time.time() # end time
    et = end - start # 총 게임시간
    et = format(et,".3f") # 소수 셋째 자리 출력(시간)
    tf = float(str(datetime.timedelta(seconds=40))[5:])

    if str(words[0][0][1]).strip() == str(x).strip():
        print('pass!')
        # 정답 소리 재생
        cor_cnt += 1
        winsound.PlaySound('./resource/muyaho.wav',winsound.SND_FILENAME)
        print("남은 시간",tf - float(et), '초')
    else:
        print('wrong!')
        winsound.PlaySound('./resource/bad.wav',winsound.SND_FILENAME)
        # 오답 소리 재생
        print("남은 시간: ",tf - float(et)," 초")
    print()

    n += 1


et = end - start # 총 게임시간
et = format(et,".3f") # 소수 셋째 자리 출력(시간)

if cor_cnt >= 3:
    print('합격')
else:
    print("불합격")

# 기록 DB 삽입
cursor.execute('INSERT INTO records("cor_cnt","record","regdate")values(?,?,?)',(cor_cnt, et, datetime.datetime.now().strftime('%Y-%m-%m %H:%M%S')))


# 수행 시간 출력
print("게임 시간 :", et, "초", " 정답 개수 : {}".format(cor_cnt))

# 시작 지점
if __name__ == '__main__':
    pass
