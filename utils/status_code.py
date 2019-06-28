
class JsonRep():

    def __init__(self, code=200, msg='', count=0, data=[]):
        self.return_json = dict()
        self.code = code
        self.msg = msg
        self.count = count
        self.data = data
        pass

    def SUCCESS(self, msg='', count=0, data=list()):
        self.return_json['code'] = self.code
        self.return_json['msg'] = self.msg
        self.return_json['status'] = True
        self.return_json['count'] = count
        self.return_json['data'] = data
        return self.return_json

    def FAILED(self, code=-1, msg='', data=list()):
        self.return_json['code'] = code
        self.return_json['msg'] = msg
        self.return_json['status'] = False
        self.return_json['count'] = 0
        self.return_json['data'] = data
        return self.return_json