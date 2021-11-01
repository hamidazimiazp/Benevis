from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Comment, Twitte
from .models import Vote
from django.http import JsonResponse
from accounts.models import User
from django.db.models import Q


class CreateTwitte(LoginRequiredMixin, View):
    def post(self, request, user_id):
        if request.user.id == user_id:
            try:
                Twitte.objects.create(user=request.user, body=request.POST["body"])
                messages.success(request, "توییت با موفقیت پست شد", "info")
                return redirect("accounts:dashboard", request.user.username)
            except :
                messages.success(request, "خطا رخ داد! دوباره تلاش کنید", "warning")
                return redirect("accounts:dashboard", request.user.username)    
        else:
            messages.success(request, "خطا رخ داد! دوباره تلاش کنید", "warning")

        return redirect("accounts:dashboard", request.user.username)


class DeleteTwitte(LoginRequiredMixin, View):
    def get(self, request, user_id, twt_id):
        if request.user.id == user_id:
            try:
                twt = Twitte.objects.filter(pk=twt_id)
                if twt.exists():
                    twt.delete()
                    messages.success(request, "توییت با موفقیت حذف شد", "info")
                    return redirect("accounts:dashboard", request.user.username)
            except :
                messages.success(request, "خطا رخ داد! دوباره تلاش کنید", "warning")
                return redirect("accounts:dashboard", request.user.username)    
        else:
            messages.success(request, "خطا رخ داد! دوباره تلاش کنید", "warning")

        return redirect("accounts:dashboard", request.user.username)


class MakeVote(LoginRequiredMixin, View):
    def post(self, request, twitte_id):
        this_user_votes = request.user.uVote.all()
        this_twitte = Twitte.objects.get(pk = twitte_id)
        
        new_one = this_user_votes.filter(twitte = this_twitte)

        if not new_one.exists():
            Vote.objects.create(user=request.user, twitte = this_twitte)
            data = {
                "status" : "ok"
            }
            return JsonResponse(data)
        else:
            data = {
                "status" : "nok"
            }
            return JsonResponse(data)


class DeleteVote(LoginRequiredMixin, View):
    def post(self, request, twitte_id):
        this_user_votes = request.user.uVote.all()
        this_twitte = Twitte.objects.get(pk = twitte_id)
        
        new_one = this_user_votes.filter(twitte = this_twitte)

        if new_one.exists():
            new_one.delete()
            data = {
                "status" : "ok"
            }
            return JsonResponse(data)
        else:
            data = {
                "status" : "nok"
            }
            return JsonResponse(data)


class TwitteDetail(LoginRequiredMixin, View):
    def get(self, request, id, year, month, day):
        twitte = get_object_or_404(Twitte,
                                   id=id,
                                   created__year=year,
                                   created__month = month,
                                   created__day = day)
        
        twitte.can_like = twitte.user_can_vote(request.user)

        comments = twitte.tTwitte.all().order_by('-created')

        context = {
            "twitte" : twitte,
            "comments" : comments,
        }

        return render(request, "twitte/twitteDetail.html", context)  


class CreateComment(LoginRequiredMixin, View):
    def post(self, request, twitte_id):
        try:
            twitte = Twitte.objects.get(pk=twitte_id)

            Comment.objects.create(user=request.user,
                                   twitte = twitte,
                                   body=request.POST["body"])

            messages.success(request, "کامنت با موفقیت ارسال شد", "info")
            return redirect("twitte:twitteDetail", twitte.id,
                                                   twitte.created.year,
                                                   twitte.created.month,
                                                   twitte.created.day)
        except :
            messages.success(request, "خطا رخ داد! دوباره تلاش کنید", "warning")
            return redirect("twitte:twitteDetail", twitte.id,
                                                   twitte.created.year,
                                                   twitte.created.month,
                                                   twitte.created.day)


class FriendsTwittes(LoginRequiredMixin, ListView):
    model = Twitte
    template_name = "twitte/friendsTwittes.html"
    context_object_name ="twittes"
    paginate_by = 4 

    def get_queryset(self):
        this_user = get_object_or_404(User, pk=self.request.user.id)

        if this_user is not None:
            followings = this_user.following.all()
            users = []
            for following in followings:
                users.append(following.to_user)

            queryset = Twitte.objects.filter(Q(user__in=users)).order_by('-created')

            for item in queryset:
                item.can_like = item.user_can_vote(self.request.user)

        return queryset