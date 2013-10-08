from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=120)
	password = models.CharField(max_length=120)
	name = models.CharField(max_length=120)
	admin = models.BooleanField(default=False)
	root = models.BooleanField(default=False)
	def is_admin(self):
		print self.username
		print self.admin
		return self.admin
	def __unicode__(self):
		return self.username

class Post(models.Model):
	subject = models.CharField(max_length=120)
	subject_rendered = models.TextField(default="")
	author = models.ForeignKey(User)
	kind = models.CharField(default='post', max_length=120)
	link = models.CharField(default='', max_length=255)
	content = models.TextField()
	content_rendered = models.TextField(default="")
	date = models.DateTimeField('date created')
	date_str = models.CharField(max_length=120)
	deleted = models.BooleanField(default=False)
	# tags = models.ManyToManyField(Tag)
	def __unicode__(self):
		return self.subject

# class Tag(models.Model):
# 	descript = models.CharField(max_length=120)
# 	def __unicode__(self):
# 		return self.descript