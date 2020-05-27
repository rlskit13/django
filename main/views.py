from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tutorial, TutorialCategory, TutorialSeries, Poll
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, CreatePollForm

# Create your views here.

def single_slug(request, single_slug):
	categories = [c.category_slug for c in TutorialCategory.objects.all()]
	if single_slug in categories:
		matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)

		series_urls = {}
		for m in matching_series.all():
			part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
			series_urls[m] = part_one.tutorial_slug
		
		return render(request, "main/category.html", {"part_ones": series_urls})

	tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
	if single_slug in tutorials:
		this_tutorial = Tutorial.objects.get(tutorial_slug = single_slug)
		tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published")
		this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)

		return render(request, "main/tutorial.html", {"tutorial": this_tutorial, "sidebar":tutorials_from_series, "this_tutorial_idx": this_tutorial_idx})
		
		return HttpResponse(f"{single_slug} is a tutorial")
	
	return HttpResponse(f"{single_slug} does not correspond to anything")


def pollhome(request):
	if request.user.is_authenticated:
		polls = Poll.objects.all()
		context = {
	        'polls' : polls
	    }
		return render(request, 'poll/home.html', context)
	else:
		messages.info(request, f"Please login or register new account.")
		return redirect("main:login_request")

def create(request):
	if request.user.is_authenticated:
		form = CreatePollForm()
		context = {'form' : form}
		#context = {}
		if request.method == 'POST':
			form = CreatePollForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('pollhome')
			else:
				form = CreatePollForm()
			context = {'form' : form}
		return render(request, 'poll/create.html', context)
	else:
		messages.info(request, f"Please login or register new account.")
		return redirect("main:login_request")

def vote(request, poll_id):
	poll = Poll.objects.get(pk=poll_id)
	if request.method == 'POST':
		selected_option = request.POST['poll']
		if selected_option == 'option1':
			poll.option_one_count += 1
		elif selected_option == 'option2':
			poll.option_two_count += 1
		elif selected_option == 'option3':
			poll.option_three_count += 1
		else:
			return HttpResponse(400, 'Invalid form')
		poll.save()

		return redirect('result', poll.id)

	context = {
        'poll' : poll
    }
	return render(request, 'poll/vote.html', context)

def result(request, poll_id):
	poll = Poll.objects.get(pk=poll_id)
	context = {'poll':poll}
	return render(request, 'poll/results.html', context)


def homepage(request):
	if request.user.is_authenticated:
		return render(request=request, template_name='main/categories.html', 
			context={"categories": TutorialCategory.objects.all})
	else:
		messages.info(request, f"Please login or register new account.")
		return redirect("main:login_request")


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"New Account Created: {username}")
			login(request, user)
			messages.info(request, f"You are now logged in as {username}")
			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")





	form = NewUserForm
	return render(request, "main/register.html", context={"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully")
	return redirect("main:login_request")

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect("main:homepage")
			else:
				messages.error(request, "Invalid username or password")

		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")

	form = AuthenticationForm()
	return render(request, "main/login.html", {"form":form})

