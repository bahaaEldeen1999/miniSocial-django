from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as logMeIn
from django.contrib.auth import logout as logMeOut
from django.contrib.auth.models import User
from .models import Post,Comment

# destroy the log in session from the request 
def logout(request):
    logMeOut(request)
    return redirect('login')

# add post to database
def addPost(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        text = request.POST["text"] 
        genre = request.POST["genre"] 
        header = request.POST["header"]
        post = Post.objects.create(user=request.user,text=text,header=header,genre=genre)
        return redirect('index')
    return redirect('index')

# add comment to a post to database
def addComment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        text = request.POST["comment"] 
        postId = request.POST["postId"]
        post = Post.objects.filter(id=postId)
        post = post[0]
        comment = Comment.objects.create(post=post,user=request.user,text=text)
        return redirect('index')
    return redirect('index') 

# get all posts from db with their comments to view in the home page
def getAllPosts():
    posts = Post.objects.all()
    data = []
    for post in posts:
        comments = getPostComments(post)
        data.append((post,comments))
    return data

# get all user posts with comments to view in comments view
def getUserPost(user):
    posts = Post.objects.filter(user=user)
    data = []
    for post in posts:
        comments = getPostComments(post)
        data.append((post,comments))
    return data
# get user posts without comments overhead to view in admin view
def getUserPostWithoutComments(user):
    posts = Post.objects.filter(user=user)
    return posts
# get the comments of specific post
def getPostComments(post):
    comments = Comment.objects.filter(post=post)
    return comments

# index page view
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = getAllPosts()
    return render(request,'index.html',{'user':request.user,'posts':posts})
# comments page view
def comments(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = getUserPost(request.user)
    return render(request,'comments.html',{'user':request.user,'posts':posts})
# posts page view
def posts(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = getUserPostWithoutComments(request.user)
    return render(request,'posts.html',{'user':request.user,'posts':posts})
# update the post and edit it
def updatePost(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        text = request.POST["text"] 
        genre = request.POST["genre"] 
        header = request.POST["header"]
        postId = request.POST["postId"]
        try:
            post = Post.objects.get(user=request.user,id=postId)
            post.text = text
            post.header = header
            post.genre = genre
            post.save()
            return redirect('posts')
        finally:
            return redirect('posts')
    return redirect('posts')

# update and edit the user
def updateUser(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        user = request.user
        username = request.POST["username"] 
        email = request.POST["email"] 
        password = request.POST["password"]
        
        # check if there is duplicate mails
        if user.username != email:
            try:
                check = User.objects.get(username=email)
                # send validation error
                return redirect('posts')
            except:
                try:
                    user.email = username
                    user.username = email
                    if password != "":
                        user.set_password(password)
                    user.save()
                except: 
                    return redirect('posts')
    return redirect('posts')
# login view handler
def login(request):
    if  request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request,username=email, password=password)
        if user is not None:
            logMeIn(request,user)
            return redirect('index')
        return redirect('login')
    else:
        return render(request,'registration/login.html')
# signup view handler
def signup(request):
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            # check if there is duplicate mails
            check = User.objects.get(username=email)
            # send validation error
            return render(request,'registration/signup.html')
        except:
            user = User.objects.create_user(username=email,email=name,password=password)
            user.save()
            return redirect('login')
        
    return render(request,'registration/signup.html')



