from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Название", widget=forms.TextInput(attrs={'class':'form-input'}))
    slug = forms.SlugField(max_length=255, label ="slug(Для администратора)")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}), label="Содержимое")
    is_published = forms.BooleanField(label="Публикация",required=False,initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Ассортименты",empty_label="")


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username','email','password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ExpertForm(forms.Form):
    product1mark = forms.IntegerField()
    product2mark = forms.IntegerField()
    product3mark = forms.IntegerField()