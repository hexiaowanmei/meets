import base64

strs = '../utils/test.text'


def get_wz(strs):
    with open(strs, 'r') as f:
        imgdata = base64.b64decode(f.read())
        file = open('../media/upload/1.jpg', 'wb')
        file.write(imgdata)
        file.close()


if __name__ == '__main__':
    get_wz(strs)
