import smtplib
from email.mime.text import MIMEText
from email.header import Header
import base64


class Mail(object):
    def __init__(self,mail_pass,sender,mail_host="smtp.qq.com"):
        # 第三方 SMTP 服务
        self.mail_pass = mail_pass  # 填写在qq邮箱设置中获取的授权码
        self.sender = sender  # 填写发送方邮箱地址
        self.mail_host = mail_host  # 填写邮箱服务器:这个是qq邮箱服务器，直接使用smtp.qq.com

    def send(self, subject,txt,receiver):
        # subject = '图书馆约座成功'  # 发送的主题
        content = str(txt)  # 邮件内容
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header(
            f'=?utf-8?B?{base64.b64encode(receiver.encode()).decode()}=?= <'+self.sender+">")  # 必须填发送者邮箱
        message['To'] = Header(receiver, 'utf-8')  # 邮件接收者姓名
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)  # 建立smtp连接，qq邮箱必须用ssl边接，因此边接465端口
            smtpObj.login(self.sender, self.mail_pass)  # 登陆
            smtpObj.sendmail(self.sender, receiver, message.as_string())  # 发送
            smtpObj.quit()
            print('邮件发送成功！！')
        except smtplib.SMTPException as e:
            print(e.__traceback__.tb_lineno, e)
            print('邮件发送失败！！')


# if __name__ == '__main__':
#     mail = Mail('wnsynzjhshtbdegi','1741063814@qq.com')
#     mail.send('图书馆约座成功','发送内容',"1741063814@qq.com")


