# 이메일 보내기 앱
import smtplib # Sinle Nail Transefer Protocol메일전송프로토콜
from email.mime.text import MIMEText # Multipurpose Interntet

send_email = 'dldyd1101@naver.com'
send_pass ='' # 임시 저장번호
recv_email = 'dldyd1101@gmail.com'
smtp_name = 'smtp.naver.com'
smtp_port = 587 # 포트번호

text = '''메일 내용입니다. 긴급입니다.
조심하세요~ 빨리 연락주세요!!
'''
msg = MIMEText(text)
msg['Subject'] = '메일 제목입니다'
msg['From'] = send_email # 보내는메일
msg['To'] = recv_email # 받는메일
print(msg.as_string())

mail = smtplib.SMTP(smtp_name, smtp_port) #SMTP 객체생성
mail.starttls() # 전송계층보안 시작
mail.login(send_email, send_pass)
mail.sendmail(send_email, recv_email, msg=msg.as_string())
mail.quit()
print('전송완료!')
