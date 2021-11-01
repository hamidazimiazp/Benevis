from django.shortcuts import get_list_or_404, render, redirect, get_object_or_404
from django.views import View

from .models import Relation, User
from .forms import UserRegisterForm
from .forms import UserLoginForm
from .forms import ProfileForm
from twitte.models import Twitte 
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.hashers import make_password
from .utils import grecaptcha_verify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json


class UserRegister(View):
    def __init__(self):
        super().__init__()
        self.template_name = "accounts/register.html"


    def get(self, request):
        if not request.user.is_authenticated: 
            form = UserRegisterForm()
            context = {
                "form" : form,
            }

            return render(request, self.template_name, context)
        else:
            messages.error(request, "برای ساخت اکانت جدید ابتدا باید خارج شوید.", "warning")
            return redirect("core:home")

    def post(self, request):
        form = UserRegisterForm(request.POST)

        context = {
            "form" : form,
        }

        if form.is_valid():
            if  grecaptcha_verify(request):
                cd = form.cleaned_data
                email = cd["email"]
                username = cd["username"]
                password = cd["password2"]

                User.objects.create(email=email,
                                    username=username,
                                    password=make_password(password))
                                    
                messages.success(request, "با موفقیت ثبت نام شدید", 'info')
                return redirect("accounts:login")
            else:
                messages.success(request, "آیا شما ربات هستید؟", 'warning')
                return render(request, self.template_name, context)

        else:
            return render(request, self.template_name, context)


class UserLogin(View):
    def __init__(self):
        super().__init__()
        self.template_name = "accounts/login.html"


    def get(self, request):
        if not request.user.is_authenticated: 
            form1 = UserLoginForm()
            form2 = UserRegisterForm()
            context = {
                "form1" : form1,
                "form2" : form2,
            }
            return render(request, self.template_name, context)
        else:
            messages.error(request, "شما از قبل وارد شده اید", "warning")
            return redirect("core:home")
        

    def post(self, request):
        form = UserLoginForm(request.POST)
        next = request.GET.get("next")

        context = {
            "form" : form
        }

        if form.is_valid():
            if  grecaptcha_verify(request):
                cd = form.cleaned_data
                email = cd["email"]
                password = cd["password"]
                
                user = authenticate(request, email = email, password = password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, "شما با موفقیت وارد شدید", "success")
                    if next:
                        return redirect(next)
                    return redirect("accounts:dashboard", user.username)
                else:
                    messages.error(request, "اطلاعات وارد شده نادرست است", "warning")
            else:
                    messages.error(request, "آیا شما ربات هستید؟", "warning")


        return render(request, self.template_name, context)
            

class UserLogout(LoginRequiredMixin, View):
    def get(self, request):
        user_logout(request)
        messages.success(request, "شما با موفقیت خارج شدید", "info")
        return redirect("accounts:login")


class UserDahboard(LoginRequiredMixin, View):
    template_name = "accounts/dashboard.html"
    
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        following = user.following.all()
        followers = user.followers.all()

        is_following = False
        relation = Relation.objects.filter(from_user = request.user, to_user = user)

        if relation.exists():
            is_following = True
    
        twittes = Twitte.objects.filter(user=user).order_by('-created')

        for item in twittes:
            item.can_like = item.user_can_vote(request.user)


        initial = {
            "username" : user.username,
            "first_name" : user.profile.first_name,
            "last_name" : user.profile.last_name,
            "bio" : user.profile.bio,
            "age" : user.profile.age,
            "phone" : user.profile.phone,
        }

        Pform = ProfileForm(instance=user.profile, initial=initial)

        context = {
            "user" : user,
            "following" : following,
            "followers" : followers,
            "Pform" : Pform,
            "is_following" : is_following,
            "twittes" : twittes,
        }
            
        return render(request, self.template_name, context)


    def post(self, request, username):
        form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)

        data = {}
        if form.is_valid():
            form.save()
            data["formchange"] = 1

            if not User.objects.filter(username = request.POST["username"]).first():
                this_user = get_object_or_404(User, username=request.user.username)
                this_user.username = request.POST["username"]
                this_user.save()
                data["username"] = request.POST["username"]
                data["isUnique"] = 1
                return JsonResponse(data)
            else:
                data["username"] = request.user.username
                data["isUnique"] = 0
                return JsonResponse(data)
        else:
            data["formchange"] = 0
            return JsonResponse(data)


class Follow(LoginRequiredMixin, View):
    def post(self, request):
        try:
            userID = request.POST["userID"]
            following = get_object_or_404(User, pk=userID)
            
            relation = Relation(from_user = request.user, to_user = following)
            relation.save()
            data = {
                "status" : "ok",
            }

            return JsonResponse(data)

        except :
            data = {
                "status" : "nok",
            }

            return JsonResponse(data)


class Unfollow(LoginRequiredMixin, View):
    def post(self, request):
        try:
            userID = request.POST["userID"]
            following = get_object_or_404(User, pk=userID)
            
            relation = Relation.objects.filter(from_user = request.user, to_user = following)
            if relation.exists():
                relation.delete()
            
                data = {
                    "status" : "ok",
                }
            else:
                data = {
                    "status" : "nok",
                }

            return JsonResponse(data)


        except :
            data = {
                "status" : "nok",
            }

            return JsonResponse(data)


class SearchQuery(LoginRequiredMixin, View):
    def get(self, request):
        if 'query' in request.GET and request.GET['query'] is not "":

            try:
                data = User.objects.filter(username__icontains=request.GET["query"]).order_by("username")[:5]
            except User.DoesNotExist:
                pass
        
            users = []
            for item in data:
                users.append([item.username, json.dumps(str(item.profile.avatar))])

            data = {
                "users" : users,
            }

        else:
            data = {
                "status" : "nok",
            }

        return JsonResponse(data)