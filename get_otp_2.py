#!/usr/bin/env
# -*- coding:utf-8 -*-
import requests
import re
import json
import urllib3

# 忽略证书警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MAIL163:
    def __init__(self, username, password):
        self.session = requests.Session()

        self.username = username
        self.password = password
        self.sid = 'xAwrrcqYRwYqkDMmVaYYxqkJLGLHQDTI'

    # def login(self):
    #     loginUrl = "https://mail.163.com/entry/cgi/ntesdoor?style=-1&df=mail163_letter&net=&language=-1&from=web&race=&iframe=1&product=mail163&funcid=loginone&passtype=1&allssl=true&url2=https://mail.163.com/errorpage/error163.htm"
    #     headers = {
    #         'Referer': "https://email.163.com/",
    #         'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
    #     }
    #
    #     postData = {
    #         'savelogin': "0",
    #         'url2': "http://mail.163.com/errorpage/error163.htm",
    #         'username': self.username,
    #         'password': self.password
    #     }
    #
    #     response = self.session.post(loginUrl, headers=headers, data=postData, verify=False)
    #     print(response.text)
    #     #提取sid，获取邮件信息需要使用它
    #     pattern = re.compile(r'sid=(.*?)&', re.S)
    #     self.sid = re.search(pattern, response.text).group(1)

    # 通过sid码获得邮箱收件箱信息
    def messageList(self):
        listUrl = 'https://mail.163.com/js6/s?sid=%s&func=mbox:listMessages' % self.sid
        # 新的请求头
        Headers = {
            'Accept': "text/javascript",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "mail.163.com",
            'Referer': "https://mail.163.com/js6/main.jsp?sid=%s&df=mail163_letter" % self.sid,
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
        }

        response = self.session.post(listUrl, headers=Headers, verify=False)
        print(f"response: {response.text}")
        pattern = re.compile(
            "id..'(.*?)',.*?from..'(.*?)',.*?to..'(.*?)',.*?subject..'(.*?)',.*?sentDate..(.*?),\n.*?receivedDate..(.*?),.*?hmid..(.*?),\n",
            re.S)
        mails = re.findall(pattern, response.text)
        print(mails)
        for mail in mails:
            mid = mail[0]
            print('-' * 45)
            print('id:', mid)
            print('发件人:', mail[1], '主题:', mail[3], '发送时间:', mail[4])
            print('收件人:', mail[2], u'接收时间:', mail[5])
            self.message(mid)

    def message(self, mid):
        Headers = {
            'Accept': "text/javascript",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "mail.163.com",
            'Referer': "https://mail.163.com/js6/main.jsp?sid=%s&df=mail163_letter" % self.sid,
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
        }

        #cookie加上这个，才能获取邮件详情
        cookie = {
            'Coremail.sid': self.sid,
        }

        url = 'https://mail.163.com/js6/read/readhtml.jsp?mid=%s&userType=ud&font=15&color=064977' % mid
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookie)
        response = self.session.get(url, headers=Headers, verify=False)

        print('邮件详情 =====>')
        print(response.text)


if __name__ == "__main__":
    mail = MAIL163('Lois15023130051', 'L1p82nlf')
    # mail.login()
    mail.messageList()
