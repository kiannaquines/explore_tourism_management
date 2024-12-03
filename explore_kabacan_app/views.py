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
    success_url = reverse_lazy("toursit")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        invalid_form = super().form_invalid(form)
        return invalid_form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Create New Tourist"
        context["button"] = "Create Tourist"
        return context


class AddSpotView(CreateView):
    form_class = SpotForm
    template_name = "includes/add.html"
    model = Spot
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        invalid_form = super().form_invalid(form)
        return invalid_form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Create New Spot"
        context["button"] = "Create Spot"
        return context


class AddCategorySpotView(CreateView):
    form_class = CategoryForm
    template_name = "includes/add.html"
    model = SpotCategory
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        invalid_form = super().form_invalid(form)
        return invalid_form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Create New Category"
        context["button"] = "Create Category"
        return context


class UpdateCategorySpotView(UpdateView):
    pk_url_kwarg = "pk"
    form_class = CategoryForm
    template_name = "includes/add.html"
    model = SpotCategory
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        invalid_form = super().form_invalid(form)
        return invalid_form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Category"
        context["button"] = "Save Changes"
        return context


class UpdateSpotView(UpdateView):
    pk_url_kwarg = "pk"
    form_class = SpotForm
    template_name = "includes/add.html"
    model = Spot
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        invalid_form = super().form_invalid(form)
        return invalid_form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Spot"
        context["button"] = "Save Changes"
        return context


class UpdateTouristView(UpdateView):
    pk_url_kwarg = "pk"
    form_class = TouristForm
    template_name = "includes/add.html"
    model = Tourist
    success_url = reverse_lazy("toursit")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        invalid_form = super().form_invalid(form)
        return invalid_form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Tourist"
        context["button"] = "Save Changes"
        return context


class DeleteTouristView(DeleteView):
    pk_url_kwarg = "pk"
    template_name = "includes/delete.html"
    model = Tourist
    success_url = reverse_lazy("toursit")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        invalid_form = super().form_invalid(form)
        return invalid_form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Remove Tourist"
        context["button"] = "Remove"
        return context


class DeleteSpotView(DeleteView):
    pk_url_kwarg = "pk"
    template_name = "includes/delete.html"
    model = Spot
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        invalid_form = super().form_invalid(form)
        return invalid_form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Remove Spot"
        context["button"] = "Remove"
        return context


class DeleteCategorySpotView(DeleteView):
    pk_url_kwarg = "pk"
    template_name = "includes/delete.html"
    model = SpotCategory
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        invalid_form = super().form_invalid(form)
        return invalid_form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Remove Category"
        context["button"] = "Remove"
        return context
