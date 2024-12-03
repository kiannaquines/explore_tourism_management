from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, DeleteView
from explore_kabacan_app.forms import *
from django.urls import reverse_lazy
from explore_kabacan_app.models import *
from django.contrib import messages
from explore_kabacan_app.mixins import CustomLoginRequiredMixin
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import ExtractYear, TruncMonth

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

def monthly_visitors_count(request):
    monthly_visitors = (
        Tourist.objects.annotate(month=TruncMonth('visit_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    months = []
    counts = []

    for entry in monthly_visitors:
        months.append(entry['month'].strftime("%Y-%m")) 
        counts.append(entry['count'])

    return JsonResponse({'months': months, 'counts': counts})


def gender_distribution(request):
    gender_counts = (
        Tourist.objects.values('gender')
        .annotate(count=Count('gender'))
        .order_by('gender')
    )

    data = {entry['gender']: entry['count'] for entry in gender_counts}
    return JsonResponse({'gender_distribution': data})


def age_distribution(request):
    current_year = timezone.now().year
    age_ranges = {
        '0-17': 0,
        '18-35': 0,
        '36-50': 0,
        '51+': 0,
    }

    tourists = Tourist.objects.annotate(
        age=current_year - ExtractYear('dob')
    )

    for tourist in tourists:
        if tourist.age <= 17:
            age_ranges['0-17'] += 1
        elif 18 <= tourist.age <= 35:
            age_ranges['18-35'] += 1
        elif 36 <= tourist.age <= 50:
            age_ranges['36-50'] += 1
        else:
            age_ranges['51+'] += 1

    return JsonResponse({'age_ranges': age_ranges})

class DashboardView(CustomLoginRequiredMixin, View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        context = {}
        current_time = timezone.now().date()
        context['count_total_visitors'] = Tourist.objects.count()
        context['count_total_spots'] = Spot.objects.count()
        context['count_total_category'] = SpotCategory.objects.count()
        context['count_total_visitors_today'] = Tourist.objects.filter(visit_date__date=current_time).count()
        context['visitors_history'] = Tourist.objects.all().order_by('visit_date')[:5]
        context['most_visited_spot'] =  Spot.objects.annotate(visit_count=Count('tourist')).order_by('-visit_count')[:6]
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
