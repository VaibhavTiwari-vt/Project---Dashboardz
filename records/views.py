from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

def error404(request,exception):
    return render(request,"errors/error404.html",status=404)

def privacy_policy(request):
    return render(request,"records/privacy-policy.html")
def main(request):
    if request.user.is_authenticated:
        return render(request,'records/records.html')
    return render(request, 'main.html')

class AddTableView(LoginRequiredMixin,View):
    login_url=reverse_lazy("login")
    redirect_field_name = "next"
    def get(self,request):
        return render(request, 'records/add-table.html')
    def post(self,request):
        return redirect("records")

class AddTableDataView(LoginRequiredMixin,View):
    login_url=reverse_lazy("login")
    redirect_field_name = "next"
    def get(self,request):
        return render(request, 'records/add-table-data.html')
    def post(self,request):
        return redirect("records")

class EditTableDataView(LoginRequiredMixin,View):
    login_url=reverse_lazy("login")
    redirect_field_name = "next"
    def get(self,request):
        return render(request, 'records/edit-table-data.html')
    def post(self,request):
        return redirect("records")
