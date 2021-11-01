from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.html import mark_safe
from django.contrib.staticfiles import finders


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=32, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]
    def __str__(self):
        return self.username


    def has_perm(self, perm, obj=None):
        return True

    
    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    bio = models.TextField(max_length=70, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True)
    avatar = models.ImageField(default=finders.find('images/customer.png'), null=True, blank=True)


    def __str__(self):
        return self.user.username


    def image_tag(self):
        return mark_safe("<img src='{}' height='150px' width='150px;border-radius:50% !important'>".format(self.avatar.url))
    
    image_tag.short_description = "Image"


    def get_absolute_url(self):
        return reverse("accounts:dashboard", kwargs={"pk": self.user.id})
    

def save_profile(sender, **kwargs):
    if kwargs["created"]:
        new_profile = Profile(user = kwargs["instance"])
        new_profile.save()



post_save.connect(save_profile, sender=User)


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "followers")


    def __str__(self):
        return f"{self.from_user} followed {self.to_user}"