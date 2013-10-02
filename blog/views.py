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

# from resume_app.models import Users
def index(request):
	return render(request, 'blog/index.html', {'request':request})

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
				return HttpResponseRedirect(reverse('blog:index'))
			context['error_message'] = 'Password mismatch <br />'
		else:
			context['error_message'] = 'Please fill in all fields <br />'
		return render(request, 'blog/signup.html', context)
	return render(request, 'blog/signup.html', {'request': request})

def login(request):
	context = {'request': request}
	if request.method == 'POST':
		userexists = False
		if request.POST['username']:
			try:
				user = User.objects.get(username=request.POST['username'])
				userexists = True
			except ObjectDoesNotExist:
				pass
		hashed_pass = ''
		if request.POST['password']:
			hashed_pass = hashlib.sha224(request.POST['password']+'key').hexdigest()
		if userexists and hashed_pass == user.password:
			request.session['user'] = user.username
			return HttpResponseRedirect(reverse('blog:index'))
		context['username'] = request.POST['username']
		context['error_message'] = "Username or password incorrect <br/>"
	return render(request, 'blog/login.html', context)


def logout(request):
	try:
		del request.session['user']
	except KeyError:
		pass
	return HttpResponseRedirect(reverse('blog:index'))

