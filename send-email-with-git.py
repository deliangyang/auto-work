# -*-- coding:utf-8 -*--
import smtplib
import os
import sys
from bullet import VerticalPrompt
from bullet import Bullet
from bullet import YesNo
from email.mime.text import MIMEText

from config import *


def get_git_log(pro_path, author, env):
    types = 'feat|fix|docs|style|refactor|perf|test|chore|revert'
    command = "cd %s && git checkout %s && git pull && git log --author=%s | grep -P '(%s)' | head && cd -"\
              % (pro_path, env, author, types)
    result = os.popen(command).readlines()
    return list(map(lambda x: x.strip(), result))


def parse_message(subject, content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = from_someone
    message['To'] = someone
    message['Cc'] = ','.join([test_cc, backend_cc])
    message['Subject'] = subject
    return message


def send_mail(sf, st, msg):
    server = smtplib.SMTP_SSL(mail_host, 465)
    server.login(user_name, password)
    server.sendmail(sf, st, msg.as_string())
    return True


def parse_config():
    cli = VerticalPrompt(
        [
            Bullet("choice env? ",
                   choices=['test', 'new-test']),
        ],
        spacing=1
    )
    result = cli.launch()
    _, subj = result[0]
    if subj == 'new-test':
        subj = 'test-next'

    log = ["  "] + get_git_log('/mnt/api-site', 'ydl', subj)
    cli = VerticalPrompt(
        [
            Bullet("choice git log: ",
                   choices=log),
            YesNo("send? "),
        ],
        spacing=1
    )
    result = cli.launch()
    _, text = result[0]
    _, yes_or_no = result[1]
    return subj, text, yes_or_no


if __name__ == '__main__':
    _subject, _content, yes = parse_config()
    if len(sys.argv) >= 2:
        _content += "\n" + sys.argv[1]
    _subject = 'party %s 有更新' % _subject
    _msg = parse_message(_subject, _content)
    print((_subject, _content, _msg.as_string()))
    if yes and send_mail(send_from, send_to, _msg):
        print('success')
    else:
        print('fail')
