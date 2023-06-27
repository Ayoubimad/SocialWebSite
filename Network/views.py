import json
import os
from datetime import timedelta
from sqlite3 import IntegrityError

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *


@login_required(login_url='login/')
def home(request):
    user = request.user
    followed_users = user.follows.all()
    start_date = timezone.now() - timedelta(days=2)
    posts = Post.objects.filter(creator__in=followed_users, date_created__gte=start_date).order_by("-date_created")
    context = {
        'user': user,
        'posts': posts,
    }
    return render(request=request, template_name='home.html', context=context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


@login_required(login_url='login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        profile = request.FILES.get("profile")
        cover = request.FILES.get('cover')
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.profile_pic = profile or os.path.join("..", "static", "images", "no_pic.png")
            user.cover = cover or os.path.join("..", "static", "images", "no_cover.jpeg")
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return redirect('home')
    else:
        return render(request, "register.html")


@login_required(login_url='login/')
def saved(request):
    posts = Post.objects.filter(savers=request.user)
    return render(request=request, template_name='saved.html', context={
        'posts': posts
    })


@login_required(login_url='login/')
def profile_view(request, username):
    username = get_object_or_404(User, username=username)
    posts = Post.objects.filter(creator=username).order_by("-date_created")
    chat = Chat.objects.filter(
        Q(participants=username) & Q(participants=request.user)
    ).first()

    if chat is None:
        chat = Chat.objects.create()
        chat.participants.add(username, request.user)
    return render(request, 'profile.html', {
        'us': username,
        'posts': posts,
        'chat': chat
    })


@login_required(login_url='login/')
def edit_profile(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        profile_pic = request.FILES.get('profile')
        cover = request.FILES.get('cover')

        user = request.user

        if firstname:
            user.first_name = firstname

        if lastname:
            user.last_name = lastname

        if email:
            user.email = email

        if bio:
            user.bio = bio

        if profile_pic:
            user.profile_pic = profile_pic

        if cover:
            user.cover = cover

        user.save()
    return render(template_name='edit_profile.html', request=request, context={})


@login_required(login_url='login/')
def search(request):
    user = User.objects.get(id=request.user.id)
    suggestions = user.get_suggested_followers()
    query = request.GET.get('query', '')
    if query:
        users = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        ).exclude(id=request.user.id)

        posts = Post.objects.filter(
            Q(content_text__icontains=query)
        ).order_by('-date_created')

        return render(request=request, template_name='search.html', context={
            'users': users,
            'posts': posts,
        })

    return render(request=request, template_name='search.html', context={
        'suggestions': suggestions
    })


@login_required(login_url='login/')
def follow_unfollow(request, pk):
    user = get_object_or_404(User, id=request.user.id)
    us = get_object_or_404(User, id=pk)
    if us in user.follows.all():
        user.follows.remove(us)
    else:
        user.follows.add(us)
    return redirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
@login_required(login_url='login/')
def like_post(request, post_id):
    if request.method == 'PUT':
        post = get_object_or_404(Post, pk=post_id)
        post.likers.add(request.user)
        post.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)


@csrf_exempt
@login_required(login_url='login/')
def unlike_post(request, post_id):
    if request.method == 'PUT':
        post = get_object_or_404(Post, pk=post_id)
        post.likers.remove(request.user)
        post.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)


@csrf_exempt
@login_required(login_url='login/')
def save_post(request, post_id):
    if request.method == 'PUT':
        post = get_object_or_404(Post, pk=post_id)
        post.savers.add(request.user)
        post.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)


@csrf_exempt
@login_required(login_url='login/')
def unsave_post(request, post_id):
    if request.method == 'PUT':
        post = get_object_or_404(Post, pk=post_id)
        post.savers.remove(request.user)
        post.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)


@login_required(login_url='login/')
def create_post(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        try:
            if text != '' or pic is not None:
                Post.objects.create(creator=request.user, content_text=text, content_image=pic)
        except Exception:
            redirect('profile', request.user.username)
        return redirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def get_comments(request, post_id):
    if request.method == 'GET':
        try:
            post = get_object_or_404(Post, id=post_id)
            comments = Comment.objects.filter(post=post).order_by('-comment_time').all()
            return JsonResponse([c.serialize() for c in comments], safe=False)
        except:
            return HttpResponse(status=500)


@csrf_exempt
def delete_comment(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            comment_id = int(data["comment_id"])
            comment = get_object_or_404(Comment, id=comment_id)
            post = comment.post
            comment.delete()
            post.comment_count -= 1
            post.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)


@csrf_exempt
def add_comment(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            commentText = data["commentText"]
            post_id = int(data["post_id"])
            post = get_object_or_404(Post, id=post_id)
            if commentText != '':
                comment = Comment.objects.create(commenter=request.user, post=post, comment_content=commentText)
                post.comment_count += 1
                post.save()
                return JsonResponse(comment.serialize(), safe=False)
            else:
                return HttpResponse(status=203)
        except:
            return HttpResponse(status=500)


@login_required(login_url='login/')
def chats(request):
    chats_list = Chat.objects.filter(participants=request.user).order_by("-last_updated")
    return render(request=request, template_name='chats.html', context={'chats': chats_list})


@login_required(login_url='login/')
def get_messages(request, chat_id):
    if request.method == 'GET':
        try:
            messages = Message.objects.filter(chat_id=chat_id).order_by('timestamp').all()
            return JsonResponse([m.serialize() for m in messages], safe=False)
        except:
            return HttpResponse(status=500)


@csrf_exempt
def add_message(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            messageText = data["messageText"]
            chat_id = int(data["chat_id"])
            chat = get_object_or_404(Chat, id=chat_id)
            if messageText != '':
                message = Message.objects.create(sender=request.user, chat=chat, content=messageText)
                chat.last_updated = timezone.now
                chat.save()
                return JsonResponse(message.serialize(), safe=False)
            else:
                return HttpResponse(status=203)
        except:
            return HttpResponse(status=500)
