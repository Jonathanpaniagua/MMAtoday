from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(reqPOST['first_name']) == 0 or len(reqPOST['last_name']) == 0 or len(reqPOST["email"]) == 0 or len(reqPOST['password']) == 0 or len(reqPOST['password_conf']) == 0:
            errors["req_fields"] = "All fields are required"
        if len(reqPOST['first_name']) < 2:
            errors["first_name"] = "First name must be at least 2 characters"
        if len(reqPOST['last_name']) < 2:
            errors["last_name"] = "Last name must be at least 2 characters"
        if len(reqPOST['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters"
        if reqPOST['password'] != reqPOST['password_conf']:
            errors['password_conf'] = "Passwords need to match"
        email_check = self.filter(email=reqPOST['email'])
        if email_check:
            errors['email'] = "Email already in use"    
        if not EMAIL_REGEX.match(reqPOST["email"]):
            errors['regex'] = "Email is not in correct format"
        return errors
    
    def login_validator(self, reqPOST):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(reqPOST["email"]) == 0 or len(reqPOST['password']) == 0:
            errors["req_fields"] = "All fields are required"
        if not EMAIL_REGEX.match(reqPOST["email"]):
            errors['regex'] = "Email is not in correct format"
        email_check = self.filter(email = reqPOST['email'])
        if len(email_check)==0:
            errors['email'] = "Account does not exist!"
        return errors
    
    def update_validator(self, reqPOST):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST["email"]):
            errors['regex'] = "Email is not in correct format"
        email_check = self.filter(email = reqPOST['email'])
        if len(email_check)==0:
            errors['email'] = "Account does not exist!"
        if len(reqPOST['first_name']) < 2:
            errors["first_name"] = "First name must be at least 2 characters"
        if len(reqPOST['last_name']) < 2:
            errors["last_name"] = "Last name must be at least 2 characters"
        if len(reqPOST['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters"
        if reqPOST['password'] != reqPOST['password_conf']:
            errors['password_conf'] = "Passwords need to match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=50, unique=True)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __str__(self):
        return self.first_name + self.last_name 

class TrainingPostManager(models.Manager):
    def trainingpost_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['trainpost']) < 5:
            errors['trainpost'] = "Post must be longer than 5 characters"
        return errors

class TrainingPost(models.Model):
    trainingpost = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TrainingPostManager()

    def __str__(self):
        return self.trainingpost

class CommentManager(models.Manager):
    def comment_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['comment']) < 5:
            errors['comment'] = "Comment must be longer than 5 characters"
        return errors

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    commenter = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    training_post = models.ForeignKey(TrainingPost, related_name='post_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()

    def __str__(self):
        return self.comment

class MessageManager(models.Manager):
    def message_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['msg']) < 5:
            errors['msg'] = "Message must be longer than 5 characters"
        if len(reqPOST['subject']) < 2:
            errors['subject'] = "Subject must be longer than 2 characters"
        return errors

class Message(models.Model):
    message = models.CharField(max_length=255)
    subject = models.CharField(max_length=40)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

    def __str__(self):
        return self.message

class Gym(models.Model):
    gym_name = models.CharField(max_length=255)
    member = models.ForeignKey(User, related_name='user_gyms', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gym_name

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title