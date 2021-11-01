from django import  forms
from .models import User
from .models import Profile
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "username")
        widgets = {
            "email" : forms.EmailInput(attrs={'class' : "form-control"}),
        }


    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password1'] and cd['password2']:
            if cd['password1'] != cd['password2']:
                raise forms.ValidationError('passwords must match')
            return cd['password2']
    
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "username")


    def clean_pass(self):
        return self.initial["password"]


class UserRegisterForm(forms.Form):
    #TODO: check user must be unique
            
    email = forms.CharField(required=False, label="ایمیل", max_length=32, widget=forms.EmailInput(attrs={
        "class" : "form-control",
        "placeholder" : "ایمیل خود را وارد کنید",
    }))

    username = forms.CharField(required=False, label="نام کاربری", max_length=32, widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "نام کاربری خود را وارد کنید",
    }))

    password1 = forms.CharField(required=False, label="پسورد", max_length=40, widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "پسورد خود را وارد کنید",
    }))

    password2 = forms.CharField(required=False, label="پسورد(مجددا)", max_length=40, widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "پسورد خود را مجددا وارد کنید",
    }))


    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password1'] and cd['password2']:
            if cd['password1'] != cd['password2']:
                raise forms.ValidationError('passwords must match')
            return cd['password2']
    

class UserLoginForm(forms.Form):
    email = forms.CharField(label="ایمیل", max_length=32, widget=forms.EmailInput(attrs={
        "class" : "form-control",
        "placeholder" : "ایمیل خود را وارد کنید",
    }))

    password = forms.CharField(label="پسورد", max_length=40, widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "پسورد خود را وارد کنید",
    }))


class ProfileForm(forms.ModelForm):
    username = forms.CharField(label="نام کاربری", widget=forms.TextInput(attrs={"class" : "form-control"}))
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "bio", "age", "phone", "avatar")
        widgets = {
            "first_name" : forms.TextInput(attrs={"class" : "form-control"}),
            "last_name" : forms.TextInput(attrs={"class" : "form-control"}),
            "bio" : forms.Textarea(attrs={"class" : "form-control"}),
            "age" : forms.TextInput(attrs={"class" : "form-control"}),
            "phone" : forms.TextInput(attrs={"class" : "form-control",}),
            "avatar" : forms.FileInput(attrs={"class" : "form-control",}),
        }