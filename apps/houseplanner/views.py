from django.shortcuts import render, redirect, HttpResponse
from .models import House, User, Expense, Message, Comment, Event
from IPython import embed
from django.contrib import messages
import random
import string
from IPython import embed
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import HttpResponseRedirect
# Create your views here.

# render home page
def index(request):
	# User.objects.all().delete()
	# House.objects.all().delete()
	return render(request, 'houseplanner/index.html')

# render login page
def login(request):
	return render(request, 'houseplanner/login.html')

# render dashboard
def dashboard(request):
	# Message.objects.all().delete()
	# Comment.objects.all().delete()
	user = User.objects.get(id=request.session['user'])
	house = User.objects.get(id=request.session['user']).house
	housemates = User.objects.filter(house=house)
	messages= Message.objects.filter(user__house=house).order_by("-created_at")
	# messages = Message.objects.all()
	comments= Comment.objects.filter(user__house=house).order_by("-created_at")
	events = Event.objects.filter(user__house=house).order_by("start")
	context = {
		'user': user,
		'house': house,
		'housemates': housemates,
		'messages': messages,
		'comments': comments,
		'events': events
	}
	return render(request, 'houseplanner/dashboard.html', context)

############################################################################################################
############################################################################################################
############################################################################################################

#render edit user page
def edit_user(request):
	user = User.objects.get(id=request.session['user'])
	house = User.objects.get(id=request.session['user']).house
	housemates = User.objects.filter(house=house)
	context = {
		'user': user,
		'house': house,
		'housemates': housemates
	}
	return render(request, 'houseplanner/edit_info.html', context)

#process edits to user information
def change_info(request):
	postData = {
		'user': User.objects.get(id=request.session['user']),
		'first_name': request.POST['first_name'],
		'last_name': request.POST['last_name'],
		'email': request.POST['email'],
		'phone': request.POST['phone']
	}
	user = User.objects.editinfo(postData)
	if user == True:
		messages.success(request, 'Your information has been updated')
		return redirect('/dashboard')
	else:
		for message in user['error']:
			messages.error(request, message)
		return redirect('/edit_user')

############################################################################################################
############################################################################################################
############################################################################################################

# render charge interface
def group_charge(request):
	user = User.objects.get(id=request.session['user'])
	house = user.house
	housemates = User.objects.filter(house=house)
	context = {
		'user': user,
		'housemates': housemates
	}
	return render(request, 'houseplanner/group_charge.html', context)


# render joining or creating a house page after successful registration
def join_create(request):
	user = User.objects.get(id=request.session['user'])
	# while code generated not in database already
	code = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(5)]).upper()
	while(House.objects.filter(house_code=code).exists()):
		code = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(5)]).upper()
	context = {
		'user': user,
		'code': code
	}
	return render(request, 'houseplanner/joincreate.html', context)

# process log in and regstration
def process_logreg(request):
	if request.POST['action'] == 'register':
		postData = {
			'first_name': request.POST['first_name'],
			'last_name': request.POST['last_name'],
			'email': request.POST['email'],
			'password': request.POST['password'],
			'confirm_pw': request.POST['confirm_pw'],
			'birthdate': request.POST['birthdate']
		}
		user = User.objects.register(postData)
		if 'error' in user:
			for message in user['error']:
				messages.error(request, message)
			return redirect('/login')
		if 'theuser' in user:
			request.session['user'] = user['theuser'].id
			return redirect('/join_create')
	elif request.POST['action'] == 'login':
		postData = {
			'email': request.POST['email'],
			'password': request.POST['password']
		}
		user = User.objects.login(postData)
		if 'error' in user:
			for message in user['error']:
				messages.error(request, message)
			return redirect('/login')
		if 'theuser' in user:
			request.session['user'] = user['theuser'].id
			if User.objects.get(id=request.session['user']).house == None:
				return redirect('/join_create')
			else:
				return redirect('/dashboard')
	return redirect('/dashboard')


# creates a new house and adds user in making them admin
def create_house(request, code):
	nickname = request.POST['nickname']
	postData = {
		'nickname': nickname,
		'code': code
	}
	house = House.objects.create(nickname=nickname, house_code=code)
	User.objects.filter(id=request.session['user']).update(house=house)
	return redirect('/dashboard')

def join_house(request):
	code = request.POST['house_code']
	if House.objects.filter(house_code=code).exists():
		house = House.objects.get(house_code=code)
		User.objects.filter(id=request.session['user']).update(house=house)
		return redirect('/dashboard')
	else:
		messages.error(request, "House does not exist!")
		return redirect('/join_create')



############################################################################################################
###################################MESSAGE BOARD############################################################
############################################################################################################	

# processes posting a message
def post_message(request):
	user = User.objects.get(id=request.session['user'])
	house = User.objects.get(id=request.session['user']).house
	message = Message.objects.filter(user__house = house).order_by('-created_at')
	if request.POST['message_field']:
		Message.objects.create(message=request.POST['message_field'], user=user)
		context = {
			'messages': message
		}
	else:
		pass
	return redirect('/dashboard')

#processes posting a comment
def post_comment(request, id):
	user =  User.objects.get(id=request.session['user'])
	message = Message.objects.get(id=id)
	Comment.objects.create(comment=request.POST['comment_field'], user=user, message=message)
	comment = Comment.objects.filter(message=message)
	context = {
		'comments' : comment
	}
	return render(request, 'houseplanner/comment.html', context)

def view_message(request, id):
	message = Message.objects.get(id=id)
	comments = Comment.objects.filter(message=message)
	context = {
		'user': User.objects.get(id=request.session['user']),
		'message': message,
		'comments': comments
	}
	return render(request, 'houseplanner/message.html', context)
############################################################################################################
############################################################################################################
############################################################################################################

# renders expense history page
def expense_history(request):
	user = User.objects.get(id=request.session['user'])
	house = user.house
	expenses = Expense.objects.filter(user__house=house).order_by("-created_at")
	context = {
		'user': user,
		'house': house,
		'expenses': expenses
	}
	return render(request, 'houseplanner/expenses.html', context)


# create transactions 
def create_transactions(request):
	postData = {
		'expense_name': request.POST['expense_name'],
		'amount': request.POST['amount'],
		'due_date': request.POST['due_date'],
		'user': User.objects.get(id=request.session['user'])
	}
	expense = Expense.objects.createExpense(postData)
	if 'expense' in expense:
		return redirect('/expenses')
	elif 'error' in expense:
		for message in expense['error']:
			messages.error(request, message)
		return redirect('/group_charge')

def delete_expense(request, id):
	Expense.objects.get(id=id).delete()
	return redirect('/expenses')

# render calendar 
def calendar(request):
	# Event.objects.all().delete()
	user = User.objects.get(id=request.session['user'])
	context = {
		'user': user,
	}
	return render(request, 'houseplanner/calendar.html', context)

# grabs events from database, changes them to JSON data and sends it back to html
# filter out only events made by users in the house
def calendarEvents(request):
	user = User.objects.get(id=request.session['user'])
	house = user.house
	housemates = User.objects.filter(house=house)
	print housemates
	events = []
	for housemate in housemates:
		if Event.objects.filter(user=housemate).exists():
			user_events = Event.objects.filter(user=housemate);
			for event in user_events:
				events.append(event)
	print events
	eventObjects = []
	for event in events:
		eventObjects.append({'id':event.id, 'title': event.title, 'start': event.start, 'end': event.end, 'url': '/event/'+ str(event.id)})
	return JsonResponse(eventObjects, safe=False)

# add an event to the calendar
def add_event(request):
	if request.POST['end'] == "":
		end = request.POST['start']
	else:
		end = request.POST['end']
	print "end is" + end
	postData = {
		'title': request.POST['title'],
		'start': request.POST['start'],
		'end': end,
		'startTime': request.POST.get('start_time', False),
		'endTime': request.POST.get('end_time', False),
		'description': request.POST['description'],
		'user': User.objects.get(id=request.session['user'])
	}
	event = Event.objects.createEvent(postData)
	if 'event' in event:
		return redirect('/calendar')
	elif 'error' in event:
		for message in event['error']:
			messages.error(request, message)
		return redirect('/calendar')

# update an event after dropping and releasing
def event_info(request, id):
	user = User.objects.get(id=request.session['user'])
	event = Event.objects.get(id=id)
	start_date = event.start[:10]
	end_date = event.end[:10]
	start_time = event.start[11:]
	end_time = event.end[11:]
	context = {
		'user': user,
		'event': event,
		'start_date': start_date,
		'end_date': end_date,
		'start_time': start_time,
		'end_time': end_time
	}
	return render(request, 'houseplanner/event.html', context)

def delete_event(request, id):
	Event.objects.get(id=id).delete()
	return redirect('/calendar')

def delete_message(request, id):
	Message.objects.get(id=id).delete()
	return redirect('/dashboard')

def delete_comment(request, id):
	Comment.objects.get(id=id).delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# logs user out and redirects to login page
def logout(request):
	request.session.clear()
	return redirect('/')







