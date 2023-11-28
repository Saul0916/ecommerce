from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import UserProfile, Item
from django.shortcuts import get_object_or_404

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            existing_user = User.objects.filter(username=username).exists()
            if not existing_user:
                messages.error(request, "User does not exist")
            else:
                messages.error(request, "Wrong password")
    else:
        form = UserCreationForm()
    return render(request, 'Users/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                form.save()
                messages.success(request, "Registration successful. Login now?")
                return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'Users/register.html', {'form': form})

@login_required
def purchase_item(request):
    user_profile = UserProfile.objects.get(user=request.user)
    coins = user_profile.coins
    item_count = Item.objects.filter(user_profile=user_profile).count()
    if request.method == 'POST' and 'purchase_button' in request.POST:
        if coins >= 10:
            user_profile.coins -= 10
            Item.objects.create(user_profile=user_profile)
            user_profile.save()
            coins = user_profile.coins
            item_count += 1
    return render(request, 'Users/purchase_item.html',{'coins':coins,'item_count':item_count})

@login_required
def home(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            item_count = Item.objects.filter(user_profile=user_profile).count()
            coins = user_profile.coins
        except UserProfile.DoesNotExist:
            item_count = 0
            coins = 0
    else:
        item_count = 0
        coins = 0
    return render(request,'Users/home.html',{'item_count': item_count, 'coin_balance': coins})
