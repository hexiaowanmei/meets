import urllib
import json
from aip import AipImageCensor


APP_ID = '16295532'
API_KEY = 'gWSlD06wqf8yADLNw1PSdIhI'
SECRET_KEY = 'pqxslzYtZvoDrpEN3qtebSexw8vqDlR7'

client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)


class BaiDu_check(object):
	def __init__(self):
		self.APP_ID = '16295532'
		self.API_KEY = 'gWSlD06wqf8yADLNw1PSdIhI'
		self.SECRET_KEY = 'pqxslzYtZvoDrpEN3qtebSexw8vqDlR7'
		
	def check_Image(self, filepath):
		Image_client = AipImageCensor(self.APP_ID, self.API_KEY, self.SECRET_KEY)
		result = Image_client.imageCensorUserDefined(self.get_file_content(filepath))
		return result

	def get_file_content(self, filepath):
		with open(filepath, 'rb') as f:
			return f.read()

	def get_access_token(self):
		host = 'https://aip.baidubce.com/oauth/2.0/token?'
		data = {
			'grant_type': 'client_credentials',
			'client_id': self.API_KEY,
			'client_secret': self.SECRET_KEY,
		}
		url = host + urllib.parse.urlencode(data)
		request = urllib.request.Request(url)
		request.add_header('Content-Type', 'application/json; charset=UTF-8')
		response = urllib.request.urlopen(request)
		content = response.read()
		if (content):
			return json.loads(content.decode('UTF-8'))['access_token']

	def check_txt(self, access_token):
		host = 'https://aip.baidubce.com/rest/2.0/antispam/v2/spam?'
		data = {
			'access_token': access_token,
		}
		url = host + urllib.parse.urlencode(data)
		request = urllib.request.Request(url)
		request.add_header('Content-Type', 'application/x-www-form-urlencoded')
		
		_data = bytes(urllib.parse.urlencode({'content': 'content'}), encoding='utf8')
		response = urllib.request.urlopen(request, data=_data)
		content = response.read()
		if (content):
			return json.loads(content.decode('UTF-8'))


if __name__ == '__main__':
	check = BaiDu_check()
	result = check.check_Image('../media/upload/aa.jpg')
	print(result)
	access_token = check.get_access_token()
	print(check.check_txt(access_token))


    
"""
16347595
QjZq19yQjkzUSilIAYid1px8
6LNVDGDzHjYpZzYGMWg20oR94aS0PNdj
"""