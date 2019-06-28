import redis

from meets.settings import REDISINFO


class OPRedis(object):

    def __init__(self):
        if not hasattr(OPRedis, 'pool'):
            OPRedis.getRedisCoon()
            pass
        self.coon = redis.Redis(connection_pool=OPRedis.pool)

    @staticmethod
    def getRedisCoon():
        OPRedis.pool = redis.ConnectionPool(host=REDISINFO['host'], password=REDISINFO['password'],
                                            port=REDISINFO['port'], db=REDISINFO['db'])

    def setredis(self, key, value, time=None):
        if time:
            res = self.coon.setex(key, value, time)
        else:
            res = self.coon.set(key, value)
        return res

    def getredis(self, key):
        res = self.coon.get(key)
        return res.decode() if res else res

    def delredis(self, key):
        res = self.coon.delete(key)
        return res


if __name__ == '__main__':
    opr = OPRedis()
    res = opr.setredis('123712365', '232')
    print(res)
    res = opr.getredis('123712365')
    print(res)
    res = opr.delredis('12312365')
    print(res)