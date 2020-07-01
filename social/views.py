from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as logMeIn
from django.contrib.auth import logout as logMeOut
from django.contrib.auth.models import User
from .models import Post,Comment

def logout(request):
    logMeOut(request)
    return redirect('login')


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


def getAllPosts():
    posts = Post.objects.all()
    data = []
    for post in posts:
        comments = getPostComments(post)
        data.append((post,comments))
    return data

def getUserPost(user):
    posts = Post.objects.filter(user=user)
    data = []
    for post in posts:
        comments = getPostComments(post)
        data.append((post,comments))
    return data

def getUserPostWithoutComments(user):
    posts = Post.objects.filter(user=user)
    return posts

def getPostComments(post):
    comments = Comment.objects.filter(post=post)
    return comments


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = getAllPosts()
    return render(request,'index.html',{'user':request.user,'posts':posts})

def comments(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = getUserPost(request.user)
    return render(request,'comments.html',{'user':request.user,'posts':posts})

def posts(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = getUserPostWithoutComments(request.user)
    return render(request,'posts.html',{'user':request.user,'posts':posts})

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


def updateUser(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        user = request.user
        username = request.POST["username"] 
        email = request.POST["email"] 
        password = request.POST["password"]
        try:
            # check if there is duplicate mails
            if user.username != email:
                check = User.objects.get(username=email)
                # send validation error
                return redirect('posts')
        finally:
            try:
                user.email = username
                user.username = email
                if password != "":
                    print(password)
                    user.set_password(password)
                user.save()
            except: 
                return redirect('posts')
    return redirect('posts')

def login(request):
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



