from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, DeleteView
from explore_kabacan_app.forms import *
from django.urls import reverse_lazy
from explore_kabacan_app.models import *
from django.contrib import messages
from explore_kabacan_app.mixins import CustomLoginRequiredMixin


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


class DashboardView(CustomLoginRequiredMixin, View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class SpotView(CustomLoginRequiredMixin, View):
    template_name = "spots.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["tourist_spot"] = Spot.objects.all()
        return render(request, self.template_name, context)


class SpotCategoryView(CustomLoginRequiredMixin, View):
    template_name = "category.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["categories"] = SpotCategory.objects.all()
        return render(request, self.template_name, context)


class UsersView(CustomLoginRequiredMixin, View):
    template_name = "users.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["users"] = CustomUser.objects.all()
        return render(request, self.template_name, context)


class TouristView(CustomLoginRequiredMixin, View):
    template_name = "tourist.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["tourists"] = Tourist.objects.all()
        return render(request, self.template_name, context)


class AddTouristView(CustomLoginRequiredMixin, CreateView):
    form_class = TouristForm
    template_name = "includes/add.html"
    model = Tourist
    success_url = reverse_lazy("toursit")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Tourist added successfully.",
            extra_tags='success'
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags='danger')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Create New Tourist"
        context["button"] = "Create Tourist"
        return context


class AddSpotView(CustomLoginRequiredMixin, CreateView):
    form_class = SpotForm
    template_name = "includes/add.html"
    model = Spot
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Tourist Spot added successfully.",
            extra_tags='success'
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags='danger')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Create New Spot"
        context["button"] = "Create Spot"
        return context


class AddUserView(CustomLoginRequiredMixin, CreateView):
    form_class = UserForm
    template_name = "includes/add.html"
    model = CustomUser
    success_url = reverse_lazy("users")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "User added successfully.",
            extra_tags='success'
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags='danger')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Create New User"
        context["button"] = "Create User"
        return context


class AddCategorySpotView(CustomLoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = "includes/add.html"
    model = SpotCategory
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Category added successfully.",
            extra_tags='success'
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags='danger')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Create New Category"
        context["button"] = "Create Category"
        return context


class UpdateCategorySpotView(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    form_class = CategoryForm
    template_name = "includes/add.html"
    model = SpotCategory
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Category updated successfully.",
            extra_tags='success'
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags='danger')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Category"
        context["button"] = "Save Changes"
        return context


class UpdateSpotView(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    form_class = SpotForm
    template_name = "includes/add.html"
    model = Spot
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Tourist Spot updated successfully.",
            extra_tags='success'
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags='danger')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Spot"
        context["button"] = "Save Changes"
        return context


class UpdateTouristView(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    form_class = TouristForm
    template_name = "includes/add.html"
    model = Tourist
    success_url = reverse_lazy("toursit")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Tourist information updated successfully.",
            extra_tags='success'
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags='danger')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Update Tourist"
        context["button"] = "Save Changes"
        return context


class DeleteTouristView(CustomLoginRequiredMixin, DeleteView):
    pk_url_kwarg = "pk"
    template_name = "includes/delete.html"
    model = Tourist
    success_url = reverse_lazy("toursit")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Tourist information removed successfully.",
            extra_tags='success'
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags='danger')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Remove Tourist"
        context["button"] = "Yes, Remove"
        return context


class DeleteSpotView(CustomLoginRequiredMixin, DeleteView):
    pk_url_kwarg = "pk"
    template_name = "includes/delete.html"
    model = Spot
    success_url = reverse_lazy("spot")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Tourist spot information removed successfully.",
            extra_tags='success'
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags='danger')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Remove Spot"
        context["button"] = "Yes, Remove"
        return context


class DeleteCategorySpotView(CustomLoginRequiredMixin, DeleteView):
    pk_url_kwarg = "pk"
    template_name = "includes/delete.html"
    model = SpotCategory
    success_url = reverse_lazy("category")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Category information removed successfully.",
            extra_tags='success'
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags='danger')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Remove Category"
        context["button"] = "Yes, Remove"
        return context
