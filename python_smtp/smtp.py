# smtplib 은 SMTP를 사용하기 위한 모듈
# MIMEText 는 메일을 보낼 때 메세지의 제목과 본문을 성정하는 모듈
import smtplib
from email.mime.text import MIMEText

# 세션을 만들기 위해 SMTP 인스턴스를 이용하여 SMTP 연결을 캡슐화,
# 첫번째 파라미터는 gmail을 사용하기 위한 SMTP변수,
# 두번째 파라미터는 포트 번호, gmail은 587번 포트를 쓴다.
s = smtplib.SMTP('smtp.gmail.com', 587)


# TLS 보안 시작, 보안상의 이유로 SMTP연결을 TLS(전송 계층 보안) 모드로 설정
# 해야 한다.
s.starttls()

# gmail 계정을 인증, 근데 그냥 비번 치면 안됨, gmail 계정을 다른 디바이스에서
# 쓰려면 IMAP을 설정해줘야 한다.
s.login('gmailアドレス', 'アプリ・パスワード')

# IMAP 설정은 gmail계정의 설정에서 '전달 및 POP/IMAP'카테고리에서
# IMAP 엑세스를 'IMAP 사용'으로 바꿔줘야 한다.

# 그리고 그냥 비번을 치면 안된다. 구글 계정에서 2단계 인증을 완료하면 앱 비번을
# 생성할 수 있다. 앱은 메일, 기기는 MAC으로 설정, 나온 비밀번호를 사용

# 보낼 메세지 설정
msg = MIMEText('内容')
msg['Subject'] = '題名'

# 메일 보내기
s.sendmail("gmailアドレス", "受信者のメールアドレス", msg.as_string())

# 세션 종료
s.quit()