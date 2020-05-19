

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from confirm.forms import RegistrationForm, AccountAuthenticationForm

from datetime import datetime


# Create your views here.
def home(response):
    if response.user.is_authenticated:
        FMT='%d %H %M %S'
        now=datetime.now().strftime(FMT)
        now=[int(i) for i in now.split(' ')]
        now=60*(60*(24*now[0]+now[1])+now[2])+now[3]# it is not accurate

        time=response.user.last_login        
        time=time.strftime(FMT)
        time=[int(i) for i in time.split(' ')]
        time=60*(60*(24*time[0]+time[1])+time[2])+time[3]# it is not accurate
        return render(response, 'home.html' ,{"username": response.user.username , "confirmed":response.user.confirmed , "time":now-time-10800})
    return render(response, 'home.html' ,{})

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('confirm:home')
		else:
			context['form'] = form

	else:
		form = RegistrationForm()
		context['form'] = form
	return render(request, 'register.html', context)


def login_view(request):
    
	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("confirm:home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("confirm:home")

	else:
		form = AccountAuthenticationForm()

	context['form'] = form





	# print(form)
	return render(request, "login.html", context)


    
def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form=UserCreationForm()
    return render(response, 'register.html',{"form":form})
    
#def login(response):
#    return render(response, 'login.html',{})
    
def logedin(response):
    response.user.confirmed=datetime.now()
    response.user.save()
    return redirect('confirm:home')
    

def logout_view(response):
    logout(response)
    return redirect("confirm:home")
