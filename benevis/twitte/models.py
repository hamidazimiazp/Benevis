from django.db import models
from accounts.models import User
from django.utils.text import slugify
from django.shortcuts import reverse


class Twitte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userTwitte")
    body = models.TextField(max_length=300)
    slug = models.SlugField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    can_this_like = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user} | {self.body[:30]}"

    
    
    def user_can_vote(self, user):
        user_votes = user.uVote.all()
        qs = user_votes.filter(twitte = self)
        if qs.exists():
            return False
        else:
            return True


    def like_count(self):
        return self.tVote.count()


    def get_absolute_url(self):
        return reverse("twitte:twitteDetail", args=[self.id,
                                                    self.created.year,
                                                    self.created.month,
                                                    self.created.day])
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.body[:20])
        super().save(*args, **kwargs)
        


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uTwitte")
    twitte = models.ForeignKey(Twitte, on_delete=models.CASCADE, related_name="tTwitte")
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="rTwitte")
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user} | {self.body[:30]}"


class Vote(models.Model):
    twitte = models.ForeignKey(Twitte, on_delete=models.CASCADE, related_name="tVote")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uVote")


    def __str__(self):
        return f"{self.user} | {self.twitte}"