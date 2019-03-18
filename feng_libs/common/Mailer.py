#! coding=utf-8

import mimetypes
import os
from email.encoders import encode_base64
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL


__all__ = ['Mailer']


class Mailer(object):
    """ 发送邮件服务

    """

    QQ_32_MAIL = {
        "hostname": "smtp.qq.com",
        "hostport": "465",
        "user": "326695231@qq.com",
        "passwd": "zzmwxzeelhdkbhhj",
        "from": "326695231@qq.com",
        "mail_subject": "来自峰哥的邮件",
        "mail_encoding": "utf-8"
    }

    @staticmethod
    def Send_from_me(mail_list=[], notify_addr=[], subject="",
                          content="", attachs=None):
        ''' 使用自己的邮箱发送邮件
        mail_list 收件人列表
        notify_addr 抄送人列表
        subject 邮件标题
        content 邮件正文
        attachs 邮件附件 [(local_path, filename)]
        '''
        return Mailer.Send(
            server=Mailer.QQ_32_MAIL["hostname"],
            port=Mailer.QQ_32_MAIL["hostport"],
            user=Mailer.QQ_32_MAIL["user"],
            passwd=Mailer.QQ_32_MAIL["passwd"],
            from_email=Mailer.QQ_32_MAIL["from"],
            to_emails=mail_list,
            notify_emails=notify_addr,
            subject=(subject if subject
                     else Mailer.QQ_32_MAIL["mail_subject"]),
            content=content,
            attachs=attachs,
            encoding=Mailer.QQ_32_MAIL["mail_encoding"])

    @staticmethod
    def Send(server="", port=0, user="", passwd="", from_email="",
             to_emails=[], notify_emails="", subject="", content="",
             attachs=None, encoding="utf-8"):
        ''' 发送邮件
        server 邮件服务器地址
        port 邮件服务商端口
        user 登陆用户
        passwd 用户key。不同邮件服务商之间可能使用 key 或者 密码
        from_email 发送人
        to_emails 收件人列表
        notify_emails 抄送人列表
        subject 邮件标题
        content 邮件正文
        attachs 邮件附件 [(local_path, filename)]
        '''

        # 构造邮件
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = ", ".join(to_emails)
        msg["Cc"] = ", ".join(notify_emails)

        # 构造正文
        body = MIMEText(content, _subtype='html', _charset=encoding)
        msg.attach(body)

        # 获取附件
        if attachs:
            content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split("/", 1)

            if not isinstance(attachs, list):
                attachs = [attachs]

            for attach_item in attachs:
                if isinstance(attach_item, tuple):
                    local_file, filename = attach_item[0], attach_item[1]
                else:
                    local_file, filename = (
                        attach_item, os.path.split(attach_item)[1]
                    )

                file_msg = MIMEBase(main_type, sub_type)
                data = open(local_file, "rb")
                file_msg.set_payload(data.read())  # 加载文件内容
                data.close()
                encode_base64(file_msg)  # 编码
                file_msg.add_header('Content-Disposition',
                                    'attachment', filename=filename)  # 添加头信息

                msg.attach(file_msg)

        # 登陆 smtp
        smtp = SMTP_SSL(server, port)
        smtp.ehlo(server)
        smtp.login(user, passwd)

        # 发送邮件
        smtp.sendmail(from_email, to_emails + notify_emails, msg.as_string())

        smtp.quit()

    @staticmethod
    def table_head():
        ''' 邮件发送中 需要填写表格内容的时候加载相应css '''
        return '''<style type="text/css">
            table
            {
                border-collapse: collapse;
                margin: 0 auto;
                text-align: center;
            }
            table td, table th
            {
                border: 1px solid #cad9ea;
                color: #666;
                height: 30px;
            }
            table thead th
            {
                background-color: #CCE8EB;
                width: 100px;
            }
            table tr:nth-child(odd)
            {
                background: #fff;
            }
            table tr:nth-child(even)
            {
                background: #F5FAFA;
            }
        </style>'''


if __name__ == "__main__":
    Mailer.Send_from_me(
        mail_list=["326695231@qq.com"],
        notify_addr=["326695231@qq.com"],
        subject="测试测试",
        content="就是测试了",)
        # attachs="F:\tmp\后台资源投入周反馈表-20190126.xlsx")
