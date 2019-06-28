import random

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError


class TengXun(object):
    def __init__(self, appid=1400110000, appkey="cc5577ac225ee0aecfeddfd91e70adf1"):
        self.appid = appid
        self.appkey = appkey

    def send_message(self, code, mobile):
        sms_sign = "社交APP"
        # 短信模板ID，需要在短信应用中申请
        template_id = 287938
        ssender = SmsSingleSender(self.appid, self.appkey)
        params = [code]  # 当模板没有参数时，`params = []`
        try:
            result = ssender.send_with_param(86, str(mobile), template_id, params, sign=sms_sign, extend="",
                                             ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)
        return result


def Random_verify(counts=6):
    code=''
    for x in range(counts):
        code += str(random.randint(0, 9))

    return code


if __name__ == "__main__":
    teng_xun = TengXun(1400110000, "cc5577ac225ee0aecfeddfd91e70adf1")
    code = Random_verify()
    while True:
        results = teng_xun.send_message(code, 'mobile')
        if results['result'] == 0:
            print('hhhh')
            break



