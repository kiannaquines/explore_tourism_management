from django.shortcuts import render
from django.views.generic import View
from explore_kabacan_app.forms import *

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
