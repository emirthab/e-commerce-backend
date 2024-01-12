from celery_task import celery_app as app
from smtplib import SMTP
from config import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@app.task(time_limit=15)
def send_mail_task(email_address: str, subject: str, content: str):
    from_address = config.SMTP_FROM_ADDRESS

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = email_address
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain'))

    try:
        server = SMTP(config.SMTP_HOST, config.SMTP_PORT)
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.sendmail(from_address, email_address, msg.as_string())
        server.quit()
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print("E-posta gönderilirken bir hata oluştu:", str(e))
