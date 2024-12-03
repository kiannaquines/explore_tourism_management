from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, DeleteView
from explore_kabacan_app.forms import *
from django.urls import reverse_lazy
from explore_kabacan_app.models import *
from django.contrib import messages


class LoginView(View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pass


class RegisterView(View):
    template_name = "register.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pass


class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class SpotView(View):
    template_name = "spots.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class SpotCategoryView(View):
    template_name = "category.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
    

class TouristView(View):
    template_name = "tourist.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
    



class AddTouristView(CreateView):
    form_class = TouristForm
    template_name = "includes/add.html"
    model = Tourist
    success_url = reverse_lazy('toursit')

    def form_valid(self, form):
        context = super().form_valid(form)
        return context
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
