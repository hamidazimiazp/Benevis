from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from twitte.models import Twitte 


class Home(ListView):
    model = Twitte
    template_name = "core/index.html"
    context_object_name ="twittes"
    paginate_by = 4 

    def post(self, request, *args, **kwargs):
        return redirect("accounts:login")

    def get_queryset(self):
        queryset = Twitte.objects.all().order_by("-created")
        if self.request.user.is_authenticated:
            for item in queryset:
                item.can_like = item.user_can_vote(self.request.user)

        if self.request.method == 'POST':
            return redirect("accounts:login")

        return queryset