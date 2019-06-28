from django.contrib.sessions.models import Session
from django.test import TestCase

# Create your tests here.
#...
sess = Session.objects.get(pk='vlb8dh9e9t8xk1pa42j1oo2bqcggi0rp')
print(sess.session_data)
print(sess.get_decoded())

def check_index(request):
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        user_friend = User.objects.filter(pk=friend_id).first()
        user = get_token(request)
        SUCCESS = JsonRep().SUCCESS(count=0, data=[])
        dynamictalk = DynamicTalk.objects.filter(user_id=friend_id).all()
        friend_dict = {}
        result = []
        if dynamictalk:
            dynamictalk_count = dynamictalk.count()
            for cls in dynamictalk:
                dict = {}
                dt = datetime.datetime.now()
                age = dt.year - user_friend.birth.year
                pictures = user_friend.userimg_set.filter(Q(img_type=3) & Q(dynamictalk_id=cls.id)).all()
                if pictures:
                    images = []
                    for picture in pictures:
                        images.append(picture.img.name)
                    img = user.userimg_set.filter(img_type=1).first()
                    dict['img'] = img.img.name
                    dict['username'] = user_friend.username
                    dict['gender'] = user_friend.gender
                    dict['age'] = age
                    dict['content_text'] = cls.content_text
                    dict['images'] = images
                    dict['create_time'] = cls.create_time
                    dict['dynamictalk_count'] = dynamictalk_count
                    result.append(dict)
                else:
                    img = user.userimg_set.filter(img_type=1).first()
                    dict['img'] = img.img.name
                    dict['username'] = user_friend.username
                    dict['gender'] = user_friend.gender
                    dict['age'] = age
                    dict['content_text'] = cls.content_text
                    dict['images'] = []
                    dict['create_time'] = cls.create_time
                    dict['dynamictalk_count'] = dynamictalk_count
                    result.append(dict)
            return JsonResponse({'code': 200, 'msg': '请求成功', 'data': friend_dict})
        else:
            return JsonResponse({'code': 200, 'msg': '请求成功', 'data': friend_dict})
