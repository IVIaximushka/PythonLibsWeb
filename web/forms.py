import re

from django import forms

from web.models import User


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Электропочта:")
    username = forms.CharField(label="Имя пользователя:")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль:")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Повторите пароль:")

    def clean(self):
        cleaned_data = super().clean()
        if not re.search(
            r"^(?=.*\W)(?=.*\D)(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$",
            cleaned_data["password"],
        ):
            self.add_error(
                "password",
                "Пароль слишком простой! "
                "Он должен включать в себя "
                "как минимум одну заглавную латинскую букву, "
                "одну строчную, одну цифру и один небуквенный "
                "и нецифровой символ. "
                "Количество символов в пароле "
                "должно быть от 8 до 15.",
            )
        elif cleaned_data["password"] != cleaned_data["password2"]:
            self.add_error("password2", "Пароли не совпадают!")
        elif User.objects.filter(username=cleaned_data["username"]).exists():
            self.add_error("username", "Пользователь с таким именем уже существует!")
        elif User.objects.filter(email=cleaned_data["email"]).exists():
            self.add_error("email", "Пользователь с такой почтой уже существует!")
        return cleaned_data


class AuthenticationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
