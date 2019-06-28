import re

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from requests import Response

from user.models import User


class UserShow(MiddlewareMixin):

    def process_request(self, request):
        print("middle_ware2.process_request")

    def process_response(self, request, response):
        print("middle_ware2.process_response")
        return response




# class SessionToDbMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         # 同步session中的商品信息和数据库中购物车表的商品信息
#         # 1.判断用户是否登录，登录才做数据同步操作
#         user_id = request.session.get('user_id')
#         if user_id:
#             # 2.同步
#             # 判断session中的商品是否存在于数据库中，如果存在就更新，不存在就创建
#             # 同步数据库中的数据到session中
#             session_goods = request.session.get('goods')
#             if session_goods:
#                 for se_goods in session_goods:
#                     # se_goods的结构[goods_id, num, is_select]
#                     cart = ShoppingCart.objects.filter(user_id=user_id, goods_id=se_goods[0]).first()
#                     if cart:
#
#                         if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
#                             cart.nums = se_goods[1]
#                             cart.is_select = se_goods[2]
#                             cart.save()
#                     else:
#                         # 创建
#                         ShoppingCart.objects.create(user_id=user_id, goods_id=se_goods[0],
#                                                     nums=se_goods[1], is_select=se_goods[2])
#
#                     # 同步数据库中的数据到session中
#                     db_carts = ShoppingCart.objects.filter(user_id=user_id)
#                     # if db_carts:
#                     #     new_session_goods = [[cart.goods.id, cart.nums, cart.is_select]for cart in db_carts]
#                     #     request.session['goods'] = new_session_goods
#
#                     result = []
#                     for cart in db_carts:
#                         data = [cart.goods_id, cart.nums, cart.is_select]
#                         result.append(data)
#
#         return response
#
#
# class Browse(MiddlewareMixin):
#
#     def process_response(self, request, response):
#
#
#
#         return response
#
#
#
#
#
#
