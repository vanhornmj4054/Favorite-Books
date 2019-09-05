from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class LoginManager(models.Manager):
	def user_validator(self, postData):
		errors = {}
		if len(postData['first_name']) < 2:
			errors["first_name"] = "First name must be at least 2 characters"
		if len(postData["last_name"]) < 2:
			errors["last_name"] = "Last name must be at least 2 characters"
		if len(postData["password"]) < 8:
			errors["password_len"] = "Password must be at least 8 characters"
		if postData["password"] != postData["password_confirm"]:
			errors["password"] = "Passwords do not match"

		user = User.objects.filter(email=postData['email'])
		if len(user) != 0:
			errors["login_password"] = "This email has already been registered"
		# if not EMAIL_REGEX.match(postData['email']):
		# 	errors["login_email"] = "invalid user email"
		return errors

	def book_validator(self, postData):
		errors = {}
		if len(postData['title']) < 1:
			errors['title'] = "This book requires a title"
		if len(postData['description']) < 5:
			errors['description'] = "Description must be at least 5 characters"

		return errors
				

class User(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.EmailField(max_length=45)
	password = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = LoginManager()


class Book(models.Model):
	title = models.CharField(max_length=45)
	description = models.TextField()
	uploaded_by = models.ForeignKey(User, related_name="books_uploaded")
	users_who_like = models.ManyToManyField(User, related_name="liked_books")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = LoginManager()

	


