#!/home/vv/anaconda3/envs/spider/bin/python

import datetime
import json
import time
import requests
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from Mail_send import Mail


# rsa算法加密
def encrypt(password, public_key):
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()


class LixinLibraryReserve(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.uuid = ''
        self.day = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        self.client = requests.session()
        self.client.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        })
        self.url = {
            'login': 'http://kjyy.lixin.edu.cn/ic-web/login/user',
            'resvInfo': 'http://kjyy.lixin.edu.cn/ic-web/reserve/resvInfo',
            'resv': 'http://kjyy.lixin.edu.cn/ic-web/reserve',
            'del': 'http://kjyy.lixin.edu.cn/ic-web/reserve/delete',

            # 木兰1楼
            'Mulan_1F_101': 'http://kjyy.lixin.edu.cn/ic-web/reserve?roomIds=102622058',
            'Mulan_1F_102': 'http://kjyy.lixin.edu.cn/ic-web/reserve?roomIds=102622072',
            'Mulan_1F_book': 'http://kjyy.lixin.edu.cn/ic-web/reserve?roomIds=102622081',

            # 木兰2楼
            'Mulan_2F_book': 'http://kjyy.lixin.edu.cn/ic-web/reserve?roomIds=102622100',
            'Mulan_2F_data': 'http://kjyy.lixin.edu.cn/ic-web/reserve?roomIds=102622091',

            # 木兰3楼
            'Mulan_3F_book': 'http://kjyy.lixin.edu.cn/ic-web/reserve?roomIds=102622104',

            # 文博楼3楼
            'Wenbo_3F_A_1': 'http://kjyy.lixin.edu.cn/ic-web/reserve?roomIds=100792125',
            'Wenbo_3F_A_2': 'http://kjyy.lixin.edu.cn/ic-web/reserve?roomIds=100792127',
            'Wenbo_3F_A_3': 'http://kjyy.lixin.edu.cn/ic-web/reserve?roomIds=100792131',

        }
        self.proxy_dict = {
            "http": "http://" + self.username + ":" + self.password + "@202.121.252.52:443",
            "https": "http://" + self.username + ":" + self.password + "@202.121.252.52:443",
        }

    # 登录系统
    def login(self, select_room):
        """
        :param select_room: '2F_data’ or '2F_book' or '102'
        :return:
        """
        self.client.headers.update({
            'Referer': 'http://kjyy.lixin.edu.cn/',
            'Host': 'kjyy.lixin.edu.cn'
        })

        # 获得publicKey
        r1 = self.client.get('http://kjyy.lixin.edu.cn/ic-web/login/publicKey')
        key = json.loads(r1.text)['data']
        publicKey = key['publicKey']
        nonceStr = key['nonceStr']
        psd = '{};{}'.format(self.password, nonceStr)

        # 使用公钥加密密码
        public_key = '-----BEGIN PUBLIC KEY-----\n' + publicKey + '\n-----END PUBLIC KEY-----'
        password = encrypt(psd, public_key)
        # print('password:', password)

        # post登录请求信息
        login_data = {
            "bind": 0,
            "captcha": "",
            "logonName": self.username,
            "password": password,
            "consoleType": 16,
            "type": "",
            "unionId": ""
        }

        # get个人信息需携带的参数
        userInfo_data = {
            'beginDate': '2023-05-29',
            'endDate': self.day
        }

        # get房间携带参数
        roomInfo_data = {
            'resvDates': datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'),
            'sysKind': 8,
        }

        # 获取登录信息，包括token
        re_login = self.client.post(self.url['login'], json=login_data)
        data_re_login = json.loads(re_login.text)
        self.client.headers.update({
            'token': data_re_login['data']['token']
        })

        # 查询个人信息
        try:
            re_userInfo = self.client.get(self.url['resvInfo'], params=userInfo_data)
            data = json.loads(re_userInfo.text)
            if data['message'] == '查询成功':
                print(self.username + '图书馆系统登录成功！')
                # 查询房间信息
                re_roomInfo = self.client.get(self.url[select_room], params=roomInfo_data)
                room_data = json.loads(re_roomInfo.text)

                # 返回 图书馆座位信息 和 系统个人ID
                return room_data, data['data'][0]['appAccNo']
            else:
                print(self.username + '登录失败，请检查错误！')
                print('错误信息：{}'.format(data))

        except Exception as e:
            print(e)

    # 预约座位
    def post_reserve(self, acc_no, begin_time, end_time, dev_id):
        """
        :param acc_no: 图书馆系统识别用户的id，int,len=9
        :param begin_time: 开始时间,str,  '1970-01-01 00:00:00'
        :param end_time: 结束时间,str,  '1970-01-01 00:00:00'
        :param dev_id: 座位id,str, len=9

        :return:
        """
        post_data = {
            "sysKind": 8,
            "appAccNo": acc_no,
            "memberKind": 1,
            "resvMember": [acc_no],
            "resvBeginTime": begin_time,
            "resvEndTime": end_time,
            "testName": "",
            "captcha": "",
            "resvProperty": 0,
            "resvDev": [dev_id],
            "memo": ""
        }
        try:
            resp = self.client.post(self.url['resv'], json=post_data)
            if json.loads(resp.text)['message'] == '新增成功':
                return 1, json.loads(resp.text)['message']
            else:
                print(json.loads(resp.text))
                return 0, json.loads(resp.text)['message']
        except Exception as e:
            print(e)

    # 预约并规范化时间
    def reserve(self, acc_no, day, set_bt, set_et, dev_id):
        """

        :param acc_no: 图书馆系统识别用户的id，int,len=9
        :param day: 日期
        :param set_bt: 开始时间
        :param set_et: 结束时间
        :param dev_id: 座位id
        :return:
        """
        if day == "tomorrow":
            date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1), '%Y-%m-%d')
        else:
            date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

        bt = '{} {}'.format(date, set_bt)
        et = '{} {}'.format(date, set_et)

        print('你的预约时间为: {bt} 到 {et}\n'
              '座位号: {dev_id}'.format(bt=bt, et=et, dev_id=dev_id))

        # 请求预约座位
        res, info = self.post_reserve(acc_no=acc_no,
                                      begin_time=bt,
                                      end_time=et,
                                      dev_id=dev_id)

        return res, info


def start():
    mail_heads = []
    mail = Mail('添加你的密码','添加发送方邮箱地址')
    with open('/home/vv/ww/project/python/SLU_Library_reserve/config.json', 'r', encoding='utf-8') as fp:
        cfg = json.load(fp)
        for datas in cfg['userinfo']:
            if datas["state"] == 1:
                SLU_reserve = LixinLibraryReserve(datas['username'], datas['password'])
                task = datas['habit'][0]
                room_datas, accNo = SLU_reserve.login(task['room'])
                dev_id = ''
                for data in room_datas['data']:
                    if data["devName"] == task['seat_id']:
                        dev_id = data["devId"]
                        break
                res, info = SLU_reserve.reserve(acc_no=accNo,
                                                day=task['day'],
                                                set_bt=task['bt'],
                                                set_et=task['et'],
                                                dev_id=dev_id,
                                                )
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                if res:
                    content = '座位号: {seat_id}\n' \
                              '预约时间为: {bt} 到 {et}\n' \
                              '预约成功！'.format(bt=task['bt'],
                                                 et=task['et'],
                                                 seat_id=task['seat_id'])
                    subject = '图书馆约座成功！！！'
                else:
                    content = info
                    subject = '图书馆约座失败！！！'

                head = {
                    "subject": subject,
                    "content": content,
                    "receiver": datas['email']
                }
                mail_heads.append(head)
    for head in mail_heads:
        mail.send(head["subject"], head["content"], head["receiver"])


if __name__ == '__main__':
    start()
