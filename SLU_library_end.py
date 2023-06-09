#!/home/vv/anaconda3/envs/spider/bin/python

import datetime
import json
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
            'end': 'http://kjyy.lixin.edu.cn/ic-web/reserve/endAhaed',

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
        print('password:', password)

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

        # 获取登录信息，包括token
        re_login = self.client.post(self.url['login'], json=login_data)
        data_re_login = json.loads(re_login.text)
        self.client.headers.update({
            'token': data_re_login['data']['token']
        })

        # 查询个人信息
        re_userInfo = self.client.get(self.url['resvInfo'], params=userInfo_data)
        data = json.loads(re_userInfo.text)
        if data['message'] == '查询成功':
            # 返回座位uuid
            return data['data'][0]['uuid']
        else:
            print('查询失败，请检查错误！')
            print('错误信息：{}'.format(data))

    # 删除座位
    def post_delete(self, uuid):
        post_data = {
            "uuid": uuid,
        }
        resp = self.client.post(self.url['end'], json=post_data)
        print(json.loads(resp.text))

    # 取消预约
    def delete(self, uuid):
        # 请求预约座位
        self.post_delete(uuid=uuid)
        return


def start():
    receivers=[]
    mail = Mail('添加你的密码','添加发送方邮箱地址')
    with open('/home/vv/ww/project/python/SLU_Library_reserve/config.json', 'r', encoding='utf-8') as fp:
        cfg = json.load(fp)
        for datas in cfg['userinfo']:
            SLU_reserve = LixinLibraryReserve(datas['username'], datas['password'])
            for task in datas['habit']:
                uuid = SLU_reserve.login(task['room'])
                SLU_reserve.delete(uuid=uuid)
            receivers.append(datas['email'])
    for receiver in receivers:
        mail.send('图书馆签退成功', '签退成功', receiver)


if __name__ == '__main__':
    start()
