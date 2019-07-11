# -*- coding: utf-8 -*-

__author__ = 'Jim'

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import Tuple, Optional

from feng_libs.const.mailer import QQ_32_MAIL


def send_from_me(to_emails: Tuple[str, ...], notify_mail: Tuple[str, ...], subject: str, content: Optional[str] = None,
                 attach_files: Optional[Tuple[str, ...]] = None):
    """
    自己的邮件服务. 密码就不公开了...
    :param to_emails:
    :param notify_mail:
    :param subject:
    :param content:
    :param attach_files:
    :return:
    """

    return Mailer.send(QQ_32_MAIL['from'], to_emails=to_emails, server=QQ_32_MAIL['server'],
                       server_host=QQ_32_MAIL['server_host'], user=QQ_32_MAIL['user'], password=QQ_32_MAIL['password'],
                       subject=subject, content=content, notify_emails=notify_mail, attach_files=attach_files,
                       encoding=QQ_32_MAIL['mail_encoding'])


class Mailer:
    """
    邮件服务
    """

    @staticmethod
    def send(from_email: str, to_emails: Tuple[str, ...], server: str, server_host: int, user: str, password: str,
             subject: str, content: str, notify_emails: Optional[Tuple[str, ...]] = None,
             attach_files: Optional[Tuple[str, ...]] = None, encoding: str = "utf-8"):
        """

        :param from_email: 发送方，可以是邮件地址，可以是别名
        :param to_emails: 接收方邮件地址.
        :param server: 邮件服务器地址
        :param server_host: 邮件服务器端口
        :param user: 发送方邮件名
        :param password: 发送方邮件密码
        :param subject: 主题
        :param content: 内容
        :param notify_emails: 抄送邮件
        :param attach_files: 附件全路径
        :param encoding: 编码
        :return:
        """
        msg = MIMEMultipart()

        msg['Subject'] = subject
        msg['FROM'] = from_email
        msg['To'] = ",".join(to_emails)
        msg['Cc'] = ','.join(notify_emails)
        msg['Date'] = formatdate()

        attach_html = MIMEText(content, 'html', encoding)
        msg.attach(attach_html)

        if attach_files:
            for attach_item in attach_files:
                attach_file = MIMEText(open(attach_item, 'rb').read(), 'base64', 'utf-8')
                attach_file["Content-Disposition"] = 'attachment; filename = "{}" '.format(
                    os.path.basename(attach_item))

                msg.attach(attach_file)

        try:
            smtp_server = smtplib.SMTP_SSL(server, server_host)
            smtp_server.login(user=user, password=password)
            smtp_server.sendmail(user, to_emails + notify_emails, msg.as_string())
            smtp_server.quit()
            print("发送邮件成功")
        except smtplib.SMTPConnectError as e:
            print("邮件发送失败，连接失败: {} {}", e.smtp_code, e.smtp_error)
        except smtplib.SMTPAuthenticationError as e:
            print("邮件发送失败，认证错误: {} {}", e.smtp_code, e.smtp_error)
        except smtplib.SMTPSenderRefused as e:
            print("邮件发送失败，发件人被拒绝: {} {}", e.smtp_code, e.smtp_error)
        except smtplib.SMTPRecipientsRefused as e:
            print("邮件发送失败，收件人被拒绝: {}", "\n".join(
                ["To %s: %s" % (each, err) for each, err in e.recipients.items()]))
        except smtplib.SMTPDataError as e:
            print("邮件发送失败，数据接收拒绝: {} {}", e.smtp_code, e.smtp_error)
        except smtplib.SMTPException as e:
            print("邮件发送失败: {}", str(e))
        except Exception as e:
            print("邮件发送异常: {}", str(e))
