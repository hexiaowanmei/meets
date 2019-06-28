from django_redis import get_redis_connection
import os, django
import base64, random
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meets.settings")  # 项目名称
django.setup()


def locatebyLatLng(lat, lng, pois=0):
    '''
    根据经纬度查询地址
    '''
    items = {'location': lat + ',' + lng, 'ak': 'XhDg0CerOl020ANVfHnl6aaXs4o47Au9', 'output': 'json'}
    res = requests.get('http://api.map.baidu.com/geocoder/v2/', params=items)
    result = res.json()
    # print(result)
    # print('--------------------------------------------')
    # result = result['result']['formatted_address'] + ',' + result['result']['sematic_description']
    # result_site = result['result']['addressComponent']['city']
    result_s = result['result']['formatted_address']

    return result_s


conn = get_redis_connection('default')

x = locatebyLatLng(lat='30.454546', lng='105.075959')


# print(x)


def geoadd(lng, lat, sites):
    add_site = conn.geoadd('site', lng, lat, sites)  # 增加位置信息
    return '添加成功'


# print(geoadd('105.075959', '30.454546', '四川省资阳市乐至县'))


def geopos(site2):
    user_msg = conn.geopos('site', site2)  # 显示坐标位置信息
    return user_msg


# print(geopos( 'beijing'))


def geodist(site1, site2):
    user_distance = conn.geodist('site', site1, site2, 'km')  # 计算两地之间的距离
    return user_distance


# print(geodist('chengdu', 'beijing'))


def georadiusbymember(condition, num):
    user_radius = conn.georadiusbymember('site', condition, num, 'km', 'withdist')  # 计算范围内的距离
    # for i in user_radius:
    #     print(i[0].decode())
    return user_radius


image = "iVBORw0KGgoAAAANSUhEUgAAACwAAAAOCAYAAABU4P48AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAF6SURBVEhL1ZY9coMwEIWfchZIkckJxAmAhoojiNJu3KV0lwZK+xRU6ATmBJkUEXdRVj8MmGFsk9ge+5vReFlb2of0diymCTwRL0CHKmJgjKGQPnszJAqqw1iEqvOphZDgexJjRweq9QGrwKcWcmfB/+cCwf0xDiMan2dXIZp870ZBM6ecsIQs7Lzx2rLwa428ekawKZBgTxEvFbQqwSlu1+G830VDx61Qmh/RrO0So8YZBH2060//ohK1KUyILHYBcVqwrK1YgxHJwjVa//z1MxUj0OzMwgFe311mGTEyo5gq1kZxX5uX2Ax6L/QwTVK2WYZxmHYNf0Pow78SO8XYk2Lpt5fnKW3BwGWC228oH8756mrEG2enfYLEbS/y9HhjTgvuF6DDSaIKHTXYdsZX1yNAmtuCDp5jovfcDgdYHTQa1w0IrYc5SqVh7XoDgjS3jW0QH6sjO1jMX/NDoUpNgum6IHTjU2MeSLDSZD9zr7FDzKklnuzyA/wCcpDKoLig94YAAAAASUVORK5CYII="
#
s = '1234567890qwertyuiopasdfghQWERTYUIOPASDFGHJKLZXCVBNMjkl'


def base_image(image):
    img = ''
    for i in range(10):
        img += random.choice(s)

    data = base64.b64decode(image)
    # path = '/media/upload/%s.jpg' % img
    with open('./media/upload/%s.jpg' % img, 'wb') as f:
        f.write(data)
        f.close()

    return '/media/upload/' + img + '.jpg'

# print(base_image(image))
