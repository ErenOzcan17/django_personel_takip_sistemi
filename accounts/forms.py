from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="username")
    password = forms.CharField(max_length=100, label="password", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=100, label="email")
    username = forms.CharField(max_length=100, label="username")
    password = forms.CharField(max_length=100, label="password", widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=100, label="username")
