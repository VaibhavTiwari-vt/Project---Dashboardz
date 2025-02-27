from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

class MyAccountAdapter(DefaultAccountAdapter):
    def login(self, request, *args, **kwargs):
        return redirect("/accounts/google/login/?process=login")
