import poplib
import email
import os
import re
from email.header import decode_header

from creads import PASSWORD, EMAIL_ADDRESS


def parse_email(msg):
    data = {}
    subject = decode_header(msg.get('Subject'))[0]
    if subject[1]:
        data['subject'] = subject[0].decode(subject[1])
    else:
        data['subject'] = subject[0]

    from_ = decode_header(msg.get('From'))[0]
    if from_[1]:
        data['from'] = from_[0].decode(from_[1])
    else:
        data['from'] = from_[0]

    date = decode_header(msg.get('Date'))[0]
    if date[1]:
        data['date'] = date[0].decode(date[1])
    else:
        data['date'] = date[0]

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                data['body'] = body.decode()

            if part.get_content_type() == "application/octet-stream":
                file_name = decode_header(part.get("Content-Disposition"))[0][0].split(';')[1].split('=')[1]
                if file_name:
                    os.makedirs('attachments', exist_ok=True)
                    filepath = os.path.join('attachments', file_name).replace("\"", "")
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
    else:
        data['body'] = msg.get_payload(decode=True)

    return data


def pretty_print_email(email_data):
    # if isinstance(email_data['body'], bytes):
    #     email_data['body'] = email_data['body'].decode('utf-8')
    email_data['body'] = re.sub('[\n\t  ]{2,}', '\n', email_data['body'])

    print('Subject:', email_data['subject'])
    print('From:', email_data['from'])
    print('Date:', email_data['date'])
    print('Body:', email_data['body'])


def read_last_message(user, password, server, port):
    pop_server = poplib.POP3_SSL(server, port)
    pop_server.user(user)
    pop_server.pass_(password)

    num_messages = len(pop_server.list()[1])

    if num_messages < 1:
        print("No messages in mailbox.")
        return None

    raw_email = pop_server.retr(num_messages)[1]
    raw_email = b'\n'.join(raw_email)
    message = email.message_from_bytes(raw_email)
    pop_server.quit()
    return message


if __name__ == "__main__":
    message = read_last_message(EMAIL_ADDRESS, PASSWORD, 'pop.yandex.com', 995)
    if message:
        email_data = parse_email(message)
        pretty_print_email(email_data)
