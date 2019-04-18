# -*-- coding:utf-8 -*--
from email.utils import formataddr


user_name = 'xxx@xxx.com'
password = 'xxxxxx'


mail_host = 'smtp.exmail.qq.com'
send_from = user_name

to_someone = 'xxx1@xxx.com'
to_test = 'xxx2@xxx.com'
to_backend = 'xxxx3@qq.com'

from_someone = formataddr(['xxx', send_from])
someone = formataddr(['xxx', to_someone])
test_cc = formataddr(['测试组', to_test])
backend_cc = formataddr(['应用后端', to_backend])

send_to = [
    to_someone,
    to_test,
    to_backend,
]

