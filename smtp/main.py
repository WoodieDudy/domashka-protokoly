import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

import yaml
import os

from creads import PASSWORD, EMAIL_ADDRESS


MAIL_INFO_DIR = Path('mail_info')
with open(MAIL_INFO_DIR / 'config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

with open(MAIL_INFO_DIR / 'message.txt') as file:
    source_message = file.read()


msg = MIMEMultipart()
msg['From'] = EMAIL_ADDRESS
msg['Subject'] = config['subject']

msg.attach(MIMEText(source_message, 'plain'))

for attachment_file in config['attachments']:
    with open(MAIL_INFO_DIR / attachment_file, 'rb') as file:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_file)}')
    msg.attach(attachment)

server = smtplib.SMTP('smtp.yandex.ru', 587)
server.starttls()
server.login(EMAIL_ADDRESS, PASSWORD)

for recipient in config['recipients']:
    msg['To'] = recipient
    server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())

server.quit()
