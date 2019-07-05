from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.models import User
from . import models


def parse_tags(o):
    o.tags = o.tags.split(',')
    return o


def index(request):
    new_posts = models.Post.objects.order_by('-on_publish')[:settings.NUMBER_OF_NEW_POST]
    view_posts = models.Post.objects.order_by('-n_views')[:settings.NUMBER_OF_VIEW_POST]
    new_posts = list(map(parse_tags, new_posts))
    view_posts = list(map(parse_tags, view_posts))

    context = {}
    if new_posts:
        context = {
            "newest_post": new_posts[0],
            "new_posts": new_posts,
            "view_posts": view_posts
        }
    return render(request, 'index.html', context=context)


def category(request):
    context = {
        'categories': models.Category.objects.all()
    }
    return render(request, 'category.html', context=context)


def category_view(request, category_id, page_id):
    category = models.Category.objects.get(id=category_id)
    if category is None:
        return Http404()
    _all = Paginator(models.Post.objects.filter(category=category).all(), settings.POST_PER_PAGE)
    posts = _all.get_page(page_id)
    for post in posts:
        post.tags = post.tags.split(',')

    context = {
        'category': category,
        'page_id': page_id,
        'posts': posts,
    }
    return render(request, 'category_view.html', context=context)


def post(request, post_id):
    post = models.Post.objects.get(id=post_id)
    if post is None:
        return Http404()
    post.n_views += 1
    post.save()

    context = {
        'post': parse_tags(post)
    }
    return render(request, 'post.html', context=context)


def about(request):
    admin = User.objects.all()[0]

    context = {
        'admin': admin
    }
    return render(request, 'about.html', context=context)


def search(request):
    keyword = request.GET.get('keyword', '')
    posts = models.Post.objects.filter(title__contains=keyword)
    posts = list(map(parse_tags, posts))

    context = {
        'keyword': keyword,
        'posts': posts
    }
    return render(request, 'search.html', context=context)

def email_register(request):
    global emailRegister
    email = request.GET.get('email')
    if email:
        subscriber = models.Subscriber(email)
        subscriber.save()
    return redirect('index')


def handler404(request, exception):
    return render(request, 'errors/404.html')


def handler500(request):
    return render(request, 'errors/500.html')
