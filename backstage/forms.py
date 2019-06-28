from django import forms
from django.contrib.auth.hashers import check_password

from backstage.models import BackUser


class Register(forms.Form):
    username = forms.CharField(max_length=10, required=True, min_length=2,
                               error_messages={
                                   'required': '用户名必填',
                                   'max_length': '最多十个字符',
                                   'min_length': '最少两个字符',
                               })

    password = forms.CharField(max_length=10, required=True, min_length=6,
                               error_messages={
                                   'required': '密码必填',
                                   'max_length': '最多10个字符',
                                   'min_length': '最少6个字符',
                               })
    password1 = forms.CharField(max_length=10, required=True, min_length=6,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '最多10个字符',
                                    'min_length': '最少6个字符',
                                })

    def clean_username(self):
        username = self.cleaned_data['username']
        user = BackUser.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError('该用户已被注册')
        # return self.cleaned_data['username']

        pwd = self.cleaned_data.get('password')

        pwd1 = self.cleaned_data.get('password1')
        if pwd != pwd1:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data



    def clean(self):
        username = self.cleaned_data.get('username')

        pwd = self.cleaned_data.get('password')

        pwd1 = self.cleaned_data.get('password1')
        if pwd != pwd1:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data


class Login(forms.Form):
    username = forms.CharField(max_length=10, required=True, min_length=2,
                               error_messages={
                                   'required': '用户名必填',
                                   'max_length': '最多十个字符',
                                   'min_length': '最少两个字符',
                               })
    password = forms.CharField(max_length=10, required=True, min_length=6,
                               error_messages={
                                   'required': '密码必填',
                                   'max_length': '最多10个字符',
                                   'min_length': '最少6个字符',
                               })

    def clean(self):
        username = self.cleaned_data['username']
        user = BackUser.objects.filter(username=username).first()
        userpwd = self.cleaned_data['password']

        # password = User.objects.filter(password=userpwd).first()
        password = check_password(userpwd, user.password)
        if not user:
            raise forms.ValidationError({'username': '用户不存在'})
        if not password:
            raise forms.ValidationError({'userpwd': '密码不正确'})
        return self.cleaned_data
