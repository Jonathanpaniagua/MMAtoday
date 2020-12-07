from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.

def index(request):
    return redirect('/loginpage')

def loginpage(request):
    return render(request, 'loginpage.html')

def regpage(request):
    return render(request, 'regpage.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/regpage')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'], 
                email=request.POST['email'], 
                password=hashed_pw)
            request.session['user_id'] = user.id
            return redirect('/news')
    return redirect(request, '/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.filter(email=request.POST['email'])
            if len(user) > 0:
                user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                    request.session['user_id'] = user.id
                    return redirect('/news')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

#NEWS PAGE

def news(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'all_articles': Article.objects.all(),
        'current_page': "news",
    }
    return render(request, 'news.html', context)

#GYM PAGE

def gyms(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'all_gyms': Gym.objects.all(),
        'current_page': "gym",
    }
    return render(request, 'gyms.html', context)

#TRAINING PAGE

def training(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'training_feed': TrainingPost.objects.all().order_by("-updated_at"),
        'comments': Comment.objects.all(),
        'user': User.objects.get(id=request.session['user_id']),
        'current_page': "training",
    }
    return render(request, 'trainingfeed.html', context)

# TRAINING POSTS

def createpost(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    errors = TrainingPost.objects.trainingpost_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
                messages.error(request, value)
    else:
        TrainingPost.objects.create(trainingpost=request.POST['trainpost'], poster=User.objects.get(id=request.session['user_id']))
    return redirect('/training')

def deletepost(request, id):
    destroyed_trainingpost = TrainingPost.objects.get(id=id)
    destroyed_trainingpost.delete()
    return redirect('/training')

# def editpost(request, id):
#     if request.method == "POST":
#         errors = TrainingPost.objects.trainingpost_validator(request.POST)
#         if len(errors) > 0:
#             for key, value in errors.items():
#                 messages.error(request, value)
#             return redirect('/training')
#         else:
#             edit_trainingpost = TrainingPost.objects.get(id=id)
#             edit_trainingpost.message = request.POST['trainpost']
#             edit_trainingpost.save()
#     return redirect('/training')

# COMMENT

def postcomment(request, post_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
                messages.error(request, value)
    else:
        Comment.objects.create(comment=request.POST['comment'], commenter=User.objects.get(id=request.session['user_id']), training_post=TrainingPost.objects.get(id=post_id))
    return redirect('/training')

def deletecomment(request, id):
    if 'user_id' not in request.session:
        messages.error(request, 'You need to log in!')
        return redirect('/')
    else:
        destroyed = Comment.objects.get(id=id)
        user = User.objects.get(id=request.session['user_id'])
        if request.method == "POST" and destroyed.commenter == user: 
            destroyed.delete()
    return redirect('/training')

#INBOX

def inbox(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'my_inbox': Message.objects.filter(receiver=request.session['user_id']).order_by("-updated_at"),
        'user': User.objects.get(id=request.session['user_id']),
        'current_page': "inbox",
    }
    return render(request, 'inbox.html', context)

    # 'my_inbox': Message.objects.all().order_by("-updated_at")

def createmessage(request, receiverid):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    errors = Message.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
                messages.error(request, value)
    else:
        Message.objects.create(message=request.POST['msg'], subject=request.POST['subject'], sender=User.objects.get(id=request.session['user_id']), receiver=User.objects.get(id=receiverid))
    return redirect('/inbox')

def viewmessage(request, id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'one_message': Message.objects.get(id=id),
        'user': User.objects.get(id=request.session['user_id']),
        'current_page': "inbox",
    }
    return render(request, 'viewmessage.html', context)

def deletemessage(request, msg_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You need to log in!')
        return redirect('/')
    else:
        destroyed = Message.objects.get(id=msg_id)
        user = User.objects.get(id=request.session['user_id'])
        destroyed.delete()
        # print(Message.receiver)
        # print(user)
    return redirect('/inbox')


#USER PROFILE

def viewuser(request, id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        "user": User.objects.get(id=id),
        'current_page': "profile",
    }
    return render(request, 'viewprofile.html', context)

def edituser(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        'current_page': "profile",
    }
    return render(request, 'editprofile.html', context)

def updateuser(request, id):
    if request.method == "POST":
        errors = User.objects.update_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edituser')
        context = {
        "user": User.objects.get(id=id),
        }
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user_to_update = User.objects.get(id=request.session['user_id'])
        user_to_update.first_name = request.POST['first_name']
        user_to_update.last_name = request.POST['last_name']
        user_to_update.email = request.POST['email']
        user_to_update.password = hashed_pw
        user_to_update.save()
    return redirect('/edituser', context)