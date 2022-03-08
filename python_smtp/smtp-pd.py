import smtplib
from email.mime.text import MIMEText
import pandas as pd

s = smtplib.SMTP('smtp.gmail.com', 587)

s.starttls()

s.login('gmailアドレス', 'アプリ・パスワード')

df_pop = pd.read_excel('email.xlsx')
df_list = df_pop.values.tolist()

for i in df_list:
    msg = MIMEText('内容')
    msg['Subject'] = i[0] + '様、送りたい題名'
    s.sendmail("gmailアドレス", i[1], msg.as_string())

s.quit()
