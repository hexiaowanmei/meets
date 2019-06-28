from aip import AipImageCensor


# 图片审核
filePath = '../media/upload/aa.jpg'


def get_picture(filePath):
    with open(filePath, 'rb') as f:
        return f.read()


APP_ID = '16295532'
API_KEY = 'gWSlD06wqf8yADLNw1PSdIhI'
SECRET_KEY = 'pqxslzYtZvoDrpEN3qtebSexw8vqDlR7'


client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)


result = client.imageCensorUserDefined(get_picture(filePath))
print(result)

if __name__ == '__main__':
    get_picture(filePath)


