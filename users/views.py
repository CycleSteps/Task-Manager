from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile
import random


def index(request):
    """
    Redirects the user to the appropriate view based on their authentication status.
    
    If the user is authenticated, they are redirected to the 'dashboard' view.
    If the user is not authenticated, they are redirected to the 'signIn' view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('signIn')



class SignIn(View):
    """
    Handles user sign-in functionality.
    
    The `SignIn` class provides two methods:
    
    - `get(self, request)`: Renders the authentication template if the user is not authenticated, otherwise redirects the user to the dashboard.
    - `post(self, request)`: Authenticates the user with the provided username and password. If the authentication is successful, the user 
    is logged in and redirected to the dashboard. If the authentication fails, a 403 Forbidden response is returned with an 
    "Invalid Credential" error message.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'auth.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            response = JsonResponse({"error": "Invalid Credential"})
            response.status_code = 403
            return response



class SignUp(View):
    """
    Handles user sign-up functionality.
    
    The `SignUp` class provides two methods:
    
    - `get(self, request)`: Redirects the authenticated user to the 'boards' view, otherwise redirects the user to the 'signIn' view.
    - `post(self, request)`: Creates a new user with the provided username, email, and password. If the user creation is successful, the user is logged in and redirected to the 'boards' view. If the user creation fails due to a duplicate user or server error, a 403 Forbidden response is returned with an "Duplicate User or Server error" error message.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('boards')
        else:
            return redirect('signIn')

    def post(self, request):
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            user = User.objects.create_user(username, email, password)
            user.save()

            login(request, user)

            n = random.randint(16, 45)
            pf_url = f'/media/users/{n}.jpg'
            pf = Profile(user=user, profile_photo=pf_url)
            pf.save()

            return redirect('boards')

        except:
            response = JsonResponse({"error": "Duplicate User or Server error"})
            response.status_code = 403
            return response


class SignOut(View):
    def get(self, request):
        logout(request)
        return redirect('signIn')
