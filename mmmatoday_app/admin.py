from django.contrib import admin

# Register your models here.
from .models import Gym, Article, TrainingPost, Comment, Message

admin.site.register(Gym)
admin.site.register(Article)
admin.site.register(TrainingPost)
admin.site.register(Comment)
admin.site.register(Message)