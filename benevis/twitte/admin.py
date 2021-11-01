from django.contrib import admin
from .models import Twitte
from .models import Comment
from .models import Vote


@admin.register(Twitte)
class TwitteAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass