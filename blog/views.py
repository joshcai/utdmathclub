# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.files import File
import os
import datetime
import hashlib

from blog.models import User, Post

def render_post(content):
	array_str = content.splitlines()
	new_content = ""
	for temp in array_str:
		if temp=="":
			new_content+="<br />\n"
		else:
			new_content+="<p>"+temp+"</p>\n"
	return new_content

def render_subject(subject, link):
	if link:
		subject ='<a href="'+link+'">'+subject+'</a>'
	subject = '<h3 class="topfix">'+subject+'</h3>'
	return subject

def get_user(request):
	if 'user' in request.session:
		user = User.objects.filter(username=request.session['user'])[0]
		return user
	return None

def newpost(request):
	if 'user' in request.session:
		if request.method == 'POST':
			if request.POST['subject'] and request.POST['content']:
				d = datetime.datetime.now()
				p = Post(subject=request.POST['subject'], subject_rendered=render_subject(request.POST['subject'], request.POST['link']),
					content=request.POST['content'], content_rendered=render_post(request.POST['content']), 
					date=d, date_str=d.strftime('%B %d, %Y'),
					author=get_user(request),
					link=request.POST['link'],
					kind='post'
					)
				p.save()
				return HttpResponseRedirect(reverse('blog:blog'))
			else:
				context={
					'subject': request.POST['subject'],
					'content': request.POST['content'],
					'error_message': "Please fill in all fields",
					'request': request,
					'url': reverse('blog:newpost'),
				}
				return render(request, 'blog/newpost.html', context)
		return render(request, 'blog/newpost.html', {'request': request, 'url': reverse('blog:newpost')})
	else:
		return HttpResponseRedirect(reverse('blog:index'))

def root(request):
	if 'user' in request.session:
		print User.objects.filter(root=True)
		rooted = User.objects.filter(root=True)
		if not rooted:
			user = User.objects.filter(username=request.session['user'])[0]
			user.root = True
			user.admin = True
			user.save()
	return HttpResponseRedirect(reverse('blog:index'))


def newannounce(request):
	if 'user' in request.session:
		if request.method == 'POST':
			if request.POST['subject'] and request.POST['content']:
				d = datetime.datetime.now()
				p = Post(subject=request.POST['subject'],subject_rendered=render_subject(request.POST['subject'], request.POST['link']), 
					content=request.POST['content'], content_rendered=render_post(request.POST['content']), 
					date=d, date_str=d.strftime('%B %d, %Y'),
					author=get_user(request),
					link=request.POST['link'],
					kind='announce'
					)
				p.save()
				return HttpResponseRedirect(reverse('blog:index'))
			else:
				context={
					'subject': request.POST['subject'],
					'content': request.POST['content'],
					'error_message': "Please fill in all fields",
					'request': request,
					'url': reverse('blog:newannounce'),
				}
				return render(request, 'blog/newpost.html', context)
		return render(request, 'blog/newpost.html', {'request': request, 'url': reverse('blog:newannounce')})
	else:
		return HttpResponseRedirect(reverse('blog:index'))

def index(request):
	posts = Post.objects.order_by('-date').filter(kind='announce').filter(deleted=False)
	admin = ''
	if 'user' in request.session:
		user = get_user(request)
		if user.admin:
			admin = 'yay'
	return render(request, 'blog/index.html', {'request':request, 'nav': 'home', 'posts':posts, 'admin':admin})

def users(request):
	users = User.objects.all()
	return render(request, 'blog/users.html', {'request':request, 'users':users})

def blog(request):
	posts = Post.objects.order_by('-date').filter(kind='post').filter(deleted=False)
	return render(request, 'blog/blog.html', {'request':request, 'nav': 'blog', 'posts': posts})

def about(request):
	return render(request, 'blog/about.html', {'request':request, 'nav': 'about'})

def makeadmin(request):
	if request.method == 'POST':
		if 'username' in request.POST:
			user1 = User.objects.filter(username=request.POST['username'])[0]
			user1.admin = True
			user1.save()
		return HttpResponseRedirect(reverse('blog:index'))
	user = get_user(request)
	if user.root:
		return render(request, 'blog/makeadmin.html', {'request': request})
	else:
		return HttpResponseRedirect(reverse('blog:index'))

def signup(request):
	if request.method == 'POST':
		context={
			'username': request.POST['username'],
			'name': request.POST['name'],
			'request':request,
		}
		if request.POST['name'] and request.POST['username'] and request.POST['password'] and request.POST['password_confirm']:
			# d = datetime.datetime.now()
			if request.POST['password'] == request.POST['password_confirm']:
				u = User(username=request.POST['username'],
					password=hashlib.sha224(request.POST['password']+'key').hexdigest(),
					name=request.POST['name'],
					# date=d,
					# date_str=d.strftime('%B %d, %Y')
				)
				u.save()
				request.session['user'] = u.username
				request.session['user_obj'] = u
				return HttpResponseRedirect(reverse('blog:index'))
			context['error_message'] = 'Password mismatch'
		else:
			context['error_message'] = 'Please fill in all fields'
		return render(request, 'blog/signup.html', context)
	return render(request, 'blog/signup.html', {'request': request})

def login(request):
	context = {'request': request}
	if request.method == 'POST':
		userexists = False
		if request.POST['username']:
			try:
				user = User.objects.filter(username=request.POST['username'])[0]
				userexists = True
			except ObjectDoesNotExist:
				pass
		hashed_pass = ''
		if request.POST['password']:
			hashed_pass = hashlib.sha224(request.POST['password']+'key').hexdigest()
		if userexists and hashed_pass == user.password:
			request.session['user'] = user.username
			request.session['user_obj'] = user
			return HttpResponseRedirect(reverse('blog:index'))
		context['username'] = request.POST['username']
		context['error_message'] = "Username or password incorrect"
	return render(request, 'blog/login.html', context)


def logout(request):
	try:
		del request.session['user']
	except KeyError:
		pass
	return HttpResponseRedirect(reverse('blog:index'))

def delete(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	if 'user' in request.session and request.session['user'] == post.author.username:
		post.deleted = True
		post.save()
	return HttpResponseRedirect(reverse('blog:blog'))


def update(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	if 'user' in request.session and request.session['user'] == post.author.username:
		context={
			'post': post,	
			'url': reverse('blog:update', kwargs={'post_id': post_id}),
			'request': request,
		}
		if request.method == 'POST':
			if request.POST['subject'] and request.POST['content']:
				post.subject = request.POST['subject']
				post.content = request.POST['content']
				post.content_rendered = render_post(request.POST['content'])
				post.subject_rendered = render_subject(request.POST['subject'], request.POST['link'])
				post.save()
				if post.kind == 'post':
					return HttpResponseRedirect(reverse('blog:blog'))
				else:
					return HttpResponseRedirect(reverse('blog:index'))
			else:
				context['subject'] = request.POST['subject']
				context['content'] = request.POST['content']
				context['error_message'] = "Please fill in all fields<br />"
		return render(request, 'blog/update.html', context) 
	else:
		return HttpResponseRedirect(reverse('blog:index'))