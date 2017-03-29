from django.shortcuts import render, redirect
from .models import House, User, Expense, Message, Comment
from IPython import embed
from django.contrib import messages
import random
import string
from IPython import embed
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
	user = User.objects.get(id=request.session['user'])
	house = User.objects.get(id=request.session['user']).house
	context = {
		'user': user,
		'house': house
	}
	return render(request, 'houseplanner/dashboard.html', context)

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

# render calendar 
def calendar(request):
	user = User.objects.get(id=request.session['user'])
	context = {
		'user': user,
	}
	return render(request, 'houseplanner/calendar.html', context)

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
	
# create transactions 
def create_transactions(request):
	print request.POST['expense_name']
	print request.POST['amount']
	print request.POST['due_date']
	user = User.objects.get(id=request.session['user'])
	embed()
	return redirect('/charge')

# logs user out and redirects to login page
def logout(request):
	request.session.clear()
	return redirect('/login')







