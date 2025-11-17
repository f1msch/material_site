# payments/wechatpay_service.py
import hashlib
import time
import random
import string
import requests
import json
from django.conf import settings
from xml.etree import ElementTree


class WeChatPayService:
    def __init__(self):
        self.appid = settings.WECHAT_APP_ID
        self.mch_id = settings.WECHAT_MCH_ID
        self.api_key = settings.WECHAT_API_KEY
        self.notify_url = settings.WECHAT_NOTIFY_URL

        # 根据环境选择域名
        if settings.DEBUG:
            self.base_url = "https://api.mch.weixin.qq.com/sandboxnew"
        else:
            self.base_url = "https://api.mch.weixin.qq.com"

    def generate_nonce_str(self, length=32):
        """生成随机字符串"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_sign(self, params):
        """生成签名"""
        # 参数按ASCII码排序
        sorted_params = sorted(params.items())
        # 拼接成URL参数形式
        stringA = '&'.join([f"{key}={value}" for key, value in sorted_params if value])
        # 加上key
        stringSignTemp = f"{stringA}&key={self.api_key}"
        # MD5加密并转成大写
        return hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()

    def create_unified_order(self, order_id, amount, description, client_ip):
        """统一下单"""
        try:
            url = f"{self.base_url}/pay/unifiedorder"

            params = {
                'appid': self.appid,
                'mch_id': self.mch_id,
                'nonce_str': self.generate_nonce_str(),
                'body': description,
                'out_trade_no': order_id,
                'total_fee': int(float(amount) * 100),  # 转为分
                'spbill_create_ip': client_ip,
                'notify_url': self.notify_url,
                'trade_type': 'MWEB' if settings.DEBUG else 'JSAPI',  # 沙箱环境用MWEB
            }

            # 生成签名
            params['sign'] = self.generate_sign(params)

            # 构造XML数据
            xml_data = self.dict_to_xml(params)

            # 发送请求
            response = requests.post(url, data=xml_data.encode('utf-8'),
                                     headers={'Content-Type': 'application/xml'})

            if response.status_code == 200:
                result = self.xml_to_dict(response.content)
                if result.get('return_code') == 'SUCCESS' and result.get('result_code') == 'SUCCESS':
                    return {
                        'success': True,
                        'prepay_id': result.get('prepay_id'),
                        'payment_data': self.get_jsapi_params(result.get('prepay_id'))
                    }
                else:
                    return {
                        'success': False,
                        'error': result.get('err_code_des', '微信支付下单失败')
                    }
            else:
                return {
                    'success': False,
                    'error': '网络请求失败'
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_jsapi_params(self, prepay_id):
        """获取JSAPI支付参数"""
        params = {
            'appId': self.appid,
            'timeStamp': str(int(time.time())),
            'nonceStr': self.generate_nonce_str(),
            'package': f'prepay_id={prepay_id}',
            'signType': 'MD5'
        }
        params['paySign'] = self.generate_sign(params)
        return params

    def dict_to_xml(self, dict_data):
        """字典转XML"""
        xml = ["<xml>"]
        for k, v in dict_data.items():
            xml.append(f"<{k}><![CDATA[{v}]]></{k}>")
        xml.append("</xml>")
        return "".join(xml)

    def xml_to_dict(self, xml_data):
        """XML转字典"""
        try:
            root = ElementTree.fromstring(xml_data)
            result = {}
            for child in root:
                result[child.tag] = child.text
            return result
        except Exception as e:
            return {}