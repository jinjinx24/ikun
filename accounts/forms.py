from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='请输入有效的邮箱地址')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class UserDetailForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='请输入有效的邮箱地址')
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'address', 'gender']
        labels = {
            'avatar': '头像',
            'phone': '电话',
            'address': '住址',
            'gender': '性别',
        }

