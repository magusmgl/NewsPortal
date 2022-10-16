import json

from django.shortcuts import render
from django.http import HttpResponse

from News.models import (
    User,
    Post,
    Author,
    Comment
)


# Create your views here.
def AuthorsApiViews(request):
    '''для Get запроса выводит список авторов,
        для Post - создает нового автора'''
    if request.method == 'GET':
        # data = json.dumps([{'id': author.id,
        #                     'user': author.user,
        #                     'rating': author.user_rating}
        #                    for author in Author.objects.all()])
        return HttpResponse(content=Author.objects.all(), status=200)
    if request.method == 'POST':
        data = request.POST
        user = User.objects.create_user(username=data.get('username'),
                                        first_name=data.get('firstname'),
                                        last_name=data.get('last_name'),
                                        email=data.get('email'),
                                        password=data.get('password'))
        author = Author.objects.create(
            user=user,
            user_rating=data.get('user_rating')
        )
        return HttpResponse(status=201)
        # json_params = json.loads(request.body)
        # user = User.objects.create_user(username=json_params['username'],
        #                                 first_name=json_params['firstname'],
        #                                 last_name=json_params['last_name'],
        #                                 email=json_params['email'],
        #                                 password=json_params['password'])
        # author = Author.objects.create(
        #     user=user,
        #     user_rating=json_params['user_rating']
        # )
        # return HttpResponse(json.dumps({'id': author.id,
        #                     'user': author.user,
        #                     'rating': author.user_rating}), status=201)


def AuthorDetailApiViews(_, pk):
    '''Get запрос для получения информации о конкретном авторе'''
    try:
        data = Author.objects.get(pk=pk)
    except:
        return HttpResponse(content={'error': f'Author with pk:{pk} does not exists'},
                            status=404)
    return HttpResponse(content=data, status=200)


def PostsAuthorApiViews(_, author_pk):
    '''Get запрос, получает список всех статей автора'''
    try:
        data = Post.objects.filter(author=author_pk)
    except:
        return HttpResponse(content={'error': f'Author with pk:{author_pk} does not exists'},
                            status=404)
    return HttpResponse(content=data, status=200)


def PostsApiViews(request):
    if request.method == 'GET':
        data = Post.objects.all()
        return HttpResponse(content=data, status=200)


def PostDeatailApiViews(_, pk):
    try:
        data = Post.objects.get(pk=pk)
    except:
        return HttpResponse(content={'error': f'Post with pk:{pk} does not exists'},
                            status=404)
    return HttpResponse(content=data, status=200)


def PostEditApiViews(request, pk):

    try:
        data = request.POST
        post = Post.objects.get(pk=pk)
        post.text = data.get('text')
        post.save()
    except:
        return HttpResponse(content={'error': f'Post with pk:{pk} does not exists'},
                            status=404)
    return HttpResponse(status=200)

def PostDeleteApiViews(_, pk):
    try:
        Post.objects.get(pk=pk).delete()
    except:
        return HttpResponse(content={'error': f'Post with pk:{pk} does not exists'},
                            status=404)
    return HttpResponse(status=200)
