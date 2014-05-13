import datetime
from django.db import models
from django import forms
from django.contrib.auth.models import User

class Tree(models.Model):
    name = models.CharField(max_length = 255)
    url = models.CharField(max_length = 255)
    user = models.ForeignKey(User, blank = True, null = True, on_delete=models.SET_NULL)
    private = models.BooleanField()
    date = models.DateField(auto_now_add = True)
    number_words = models.IntegerField(default = 0)
    number_nodes = models.IntegerField(default = 1)


class Node(models.Model):
    tree = models.ForeignKey(Tree)
    time = models.DateTimeField(auto_now_add = True)
    nest_level = models.IntegerField()
    parent = models.ForeignKey('Node', blank = True, null = True)
    order = models.IntegerField()
    content = models.TextField(blank = True)
    image = models.ImageField(blank = True, null = True, upload_to = '/media')
    content_type = models.CharField(blank = True, max_length = 50)

class NodeForm(forms.Form):
    content = forms.CharField()
    nest_level = forms.CharField()

class UserForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())