from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re
import bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, postData):
		errors = []
		dateNow = datetime.datetime.today().strftime('%Y-%m-%d')
		if len(postData['first_name']) < 2:
			errors.append('First name must at least 2 letters')
		if not postData['first_name'].isalpha():
			errors.append('First name cannot contain numbers')
		if len(postData['last_name']) < 2:
			errors.append('Last name must at least 2 letters')
		if not postData['last_name'].isalpha():
			errors.append('Last name cannot contain numbers')
		if not EMAIL_REGEX.match(postData['email']):
			errors.append('Invalid Email')
		if len(postData['password']) < 8:
			errors.append('Password must be at least 8 charcters')
		if postData['password'] != postData['confirm_pw']:
			errors.append('Passwords do not match!')
		if postData['birthdate'] > dateNow:
			errors.append('Invalid date')


		if not errors:
			password = postData['password'].encode()
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			if self.filter(email=postData['email']).exists():
				errors.append('Email is already registered.')
				return { 'error': errors }
			else:
				user = self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], hash_pw = hashed, birthdate=postData['birthdate'])
				return { 'theuser': user }
		else:
			return { 'error': errors }

	def login(self, postData):
		errors = []
		if self.filter(email=postData['email']).exists():
			password = postData['password'].encode('utf-8')
			stored_hashed = User.objects.get(email=postData['email']).hash_pw
			if bcrypt.hashpw(password.encode('utf-8'), stored_hashed.encode()) != stored_hashed:
				errors.append('Incorrect password')
			else:
				user = self.get(email=postData['email'])
		else:
			errors.append('Email is not registered')

		if not errors:
			return { 'theuser': user }
		else:
			return { 'error': errors }

	def editinfo(self, postData):
		errors = []
		if len(postData['first_name']) < 2:
			errors.append('First name must at least 2 letters')
		if not postData['first_name'].isalpha():
			errors.append('First name cannot contain numbers')
		if len(postData['last_name']) < 2:
			errors.append('Last name must at least 2 letters')
		if not postData['last_name'].isalpha():
			errors.append('Last name cannot contain numbers')
		if not EMAIL_REGEX.match(postData['email']):
			errors.append('Invalid Email')
		if not len(postData['phone']) == 10:
			errors.append('Please enter a 10 digit phone number')
		elif not postData['phone'].isdigit():
			errors.append('Phone number must be digits')
		if errors == []:
			user =  postData['user']
			user.first_name = postData['first_name']
			user.last_name = postData['last_name']
			user.email = postData['email']
			user.phone = postData['phone']
			user.save()
			return True
		else:
			return {"error": errors}

class ExpenseManager(models.Manager):
	def createExpense(self, postData):
		errors = []
		current_date = datetime.datetime.today().strftime('%Y-%m-%d')
		if len(postData['expense_name']) < 1:
		    errors.append("Expense name must not be blank!")
		if len(postData['amount']) < 1:
		    errors.append("Amount must not be blank!")
		elif int(postData['amount']) <= 0:
			errors.append("Amount can not be zero or a negative number!")
		elif not postData['amount'].isdigit():
		    errors.append("Amount must be digit")

		if not errors:
			if postData['due_date'] == "":
				expense = Expense.objects.create(name = postData['expense_name'], amount=float(postData['amount']), user=postData['user'])
			else:
				expense = Expense.objects.create(name = postData['expense_name'], amount=float(postData['amount']), due_date = postData['due_date'], user=postData['user'])
			return { 'expense': expense }
		else:
			return { 'error': errors }

class CommentManager(models.Manager):
	pass

class MessageManager(models.Manager):
	pass

class EventManager(models.Manager):
	def createEvent(self, postData):
		errors = []
		current_date = datetime.datetime.today().strftime('%Y-%m-%d')
		if len(postData['title']) < 1:
			errors.append('Event title cannot be blank!')
		if postData['start'] == "":
			errors.append('must have a start date')

		if not errors:
			if postData['startTime']:
				start = postData['start'] + "T" + postData['startTime']
			else:
				start = postData['start']
			if postData['endTime']:
				end = postData['end'] + "T" + postData['endTime']
			else:
				end = postData['end']
			if len(postData['end']) < 1:
				end = postData['start']
			# embed()
			event = Event.objects.create(title=postData['title'], description=postData['description'], start=start, end=end, user=postData['user'], startDate=postData['start'])
			return { 'event': event }
		else:
			return { 'error': errors }



class House(models.Model):
	nickname = models.CharField(max_length=255)
	house_code = models.CharField(max_length=10)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	hash_pw = models.CharField(max_length=255)
	birthdate = models.DateField()
	user_level = models.CharField(max_length=255)
	phone = models.CharField(max_length=16, null=True)
	objects = UserManager()
	house = models.ForeignKey(House, related_name="house", null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Expense(models.Model):
	name = models.CharField(max_length=255)
	amount = models.IntegerField()
	due_date = models.DateField(null=True)
	user = models.ForeignKey(User)
	objects = ExpenseManager()
	charges = models.ManyToManyField(User, related_name="charges")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
	message = models.TextField()
	user = models.ForeignKey(User)
	objects = MessageManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
	comment = models.TextField()
	user = models.ForeignKey(User)
	message = models.ForeignKey(Message)
	objects = CommentManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Event(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(null=True)
	start = models.CharField(max_length=255)
	startDate = models.DateField()
	startTime = models.TimeField(null=True)
	end = models.CharField(max_length=255, null=True)
	endDate = models.DateField(null=True)
	endTime = models.TimeField(null=True)
	user = models.ForeignKey(User)
	objects = EventManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
