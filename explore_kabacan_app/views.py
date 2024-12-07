import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from io import BytesIO
from typing import Any
from django.forms import BaseModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View, CreateView, UpdateView, DeleteView
from explore_kabacan_app.forms import *
from django.urls import reverse_lazy
from explore_kabacan_app.models import *
from django.contrib import messages
from explore_kabacan_app.mixins import CustomLoginRequiredMixin
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import ExtractYear, TruncMonth
import plotly.io as pio
import plotly.graph_objects as go
from reportlab.lib.units import inch
from django.contrib.auth import login, logout, authenticate
from django.db.models.functions import TruncDate

from explore_kabacan_app.pdf_builder import pdf_builder


class CreateTouristView(CreateView):
    form_class = CreateTouristForm
    template_name = "create_tourist.html"
    model = Tourist
    success_url = reverse_lazy("visitor_tourist_create")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request,
            "You have successfully created your tourist information, please come again.",
            extra_tags="success",
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Create My Tourist Information"
        context["button"] = "Continue"
        return context


class LoginView(View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")

        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            try:
                user = CustomUser.objects.get(username=username)
                if not user.is_active:
                    messages.error(
                        request,
                        "Your account is inactive. Please contact support.",
                        extra_tags="danger",
                    )
                    return render(request, self.template_name, {"form": form})
            except CustomUser.DoesNotExist:
                messages.error(
                    request,
                    "No user found with your username, please try again.",
                    extra_tags="danger",
                )
                return render(request, self.template_name, {"form": form})

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(
                    request, "You have successfully logged in.", extra_tags="success"
                )
                return redirect("dashboard")
            else:
                messages.error(
                    request, "Invalid username or password.", extra_tags="danger"
                )
        else:
            messages.error(
                request, "Please correct the errors below.", extra_tags="danger"
            )

        return render(request, self.template_name, {"form": form})


class RegisterView(View):
    template_name = "register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")

        register_form = RegisterForm()
        return render(request, self.template_name, {"form": register_form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(
                request,
                "Account created successfully! Please wait for activation.",
                extra_tags="success",
            )
            return redirect("login")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags="danger")

        return render(request, self.template_name, {"form": form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy("login"))


def create_pie_chart(data, label, title):
    fig = go.Figure(data=[go.Pie(labels=label, values=data, hole=0.7)])
    fig.update_layout(title=title)

    buf = BytesIO()
    pio.write_image(fig, buf, format="png")
    buf.seek(0)
    return buf


def create_bar_chart(
    data,
    label=[
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ],
    title="Monthly Visitors",
    xaxis="Month",
    yaxis="Visitor Count",
):

    fig = go.Figure(data=[go.Bar(x=label, y=data)])

    fig.update_layout(
        title=title,
        xaxis_title=xaxis,
        yaxis_title=yaxis,
    )

    buf = BytesIO()
    pio.write_image(fig, buf, format="png")
    buf.seek(0)
    return buf


def generate_pdf_report(request):
    if request.method == "GET":
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        gender_counts = (
            Tourist.objects.filter(visit_date__range=(start_date, end_date))
            .values("gender")
            .annotate(count=Count("gender"))
        )
        gender_data = [gender["count"] for gender in gender_counts]
        gender_labels = [gender["gender"] for gender in gender_counts]
        gender_chart_buf = create_pie_chart(
            gender_data, gender_labels, "Gender Distribution"
        )

        today = datetime.today()
        age_data = {"0-18": 0, "19-30": 0, "31-40": 0, "41-50": 0, "51+": 0}
        for tourist in Tourist.objects.filter(
            visit_date__range=(start_date, end_date)
        ).all():
            age = today.year - tourist.dob.year
            if age <= 18:
                age_data["0-18"] += 1
            elif age <= 30:
                age_data["19-30"] += 1
            elif age <= 40:
                age_data["31-40"] += 1
            elif age <= 50:
                age_data["41-50"] += 1
            else:
                age_data["51+"] += 1

        age_chart_buf = create_pie_chart(
            list(age_data.values()), list(age_data.keys()), "Age Distribution"
        )

        monthly_visitors = (
            Tourist.objects.filter(visit_date__range=(start_date, end_date))
            .values("visit_date__month")
            .annotate(count=Count("id"))
            .order_by("visit_date__month")
        )

        monthly_data = [0] * 12
        for visitor in monthly_visitors:
            month = visitor["visit_date__month"] - 1
            monthly_data[month] = visitor["count"]

        monthly_chart_buf = create_bar_chart(monthly_data)

        spot_counts = (
            Tourist.objects.filter(visit_date__range=(start_date, end_date))
            .values("destination__spot")
            .annotate(count=Count("id"))
        )
        spot_data = [spot["count"] for spot in spot_counts]
        spot_labels = [spot["destination__spot"] for spot in spot_counts]
        spot_chart_buf = create_pie_chart(
            spot_data, spot_labels, "Most Visitors Distribution per Spot"
        )

        chart_buffers = [
            (gender_chart_buf),
            (age_chart_buf),
            (monthly_chart_buf),
            (spot_chart_buf),
        ]

        return pdf_builder(chart_buffers)


def monthly_visitors_count(request):
    monthly_visitors = (
        Tourist.objects.annotate(month=TruncMonth("visit_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    months = []
    counts = []

    for entry in monthly_visitors:
        months.append(entry["month"].strftime("%Y-%m"))
        counts.append(entry["count"])

    return JsonResponse({"months": months, "counts": counts})


def gender_distribution(request):
    gender_counts = (
        Tourist.objects.values("gender")
        .annotate(count=Count("gender"))
        .order_by("gender")
    )

    data = {entry["gender"]: entry["count"] for entry in gender_counts}
    return JsonResponse({"gender_distribution": data})


def age_distribution(request):
    current_year = timezone.now().year
    age_ranges = {
        "0-17": 0,
        "18-35": 0,
        "36-50": 0,
        "51+": 0,
    }

    tourists = Tourist.objects.annotate(age=current_year - ExtractYear("dob"))

    for tourist in tourists:
        if tourist.age <= 17:
            age_ranges["0-17"] += 1
        elif 18 <= tourist.age <= 35:
            age_ranges["18-35"] += 1
        elif 36 <= tourist.age <= 50:
            age_ranges["36-50"] += 1
        else:
            age_ranges["51+"] += 1

    return JsonResponse({"age_ranges": age_ranges})


class DashboardView(CustomLoginRequiredMixin, View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        context = {}
        current_time = timezone.now().date()
        context["count_total_visitors"] = Tourist.objects.count()
        context["count_total_spots"] = Spot.objects.count()
        context["count_total_category"] = SpotCategory.objects.count()
        context["count_total_visitors_today"] = Tourist.objects.filter(
            visit_date__date=current_time
        ).count()

        if request.user.assigned_to:
            context["visitors_history"] = Tourist.objects.filter(
                destination=request.user.assigned_to
            ).order_by("-visit_date")[:20]
        else:
            context["visitors_history"] = Tourist.objects.all().order_by("-visit_date")[
                :20
            ]

        context["most_visited_spot"] = Spot.objects.annotate(
            visit_count=Count("tourist")
        ).order_by("-visit_count")[:10]

        most_visited_spots = Spot.objects.annotate(
            visit_count=Count("tourist")
        ).order_by("-visit_count")[:10]

        chart_data = [
            {"name": spot.spot, "y": spot.visit_count} for spot in most_visited_spots
        ]

        context["chart_data"] = chart_data

        return render(request, self.template_name, context)


class MostVisitedByTouristPerSpotReportView(CustomLoginRequiredMixin, View):
    template_name = "report_tourist_per_spot.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["items"] = Spot.objects.all()
        return render(request, self.template_name, context)
    
    def post(self, request):
        destination_id = request.POST.get("spot_name")
        destination = Spot.objects.get(pk=destination_id)
        daily_visits = (
            Tourist.objects.filter(destination_id=destination_id)
            .annotate(visit_day=TruncDate("visit_date"))
            .values("visit_day")
            .annotate(total_visits=Count("id"))
            .order_by("visit_day")
        )

        spot_data = [visit["total_visits"] for visit in daily_visits]
        spot_labels = [visit["visit_day"].strftime("%Y-%m-%d") for visit in daily_visits]


        per_spot_pie_chart = create_pie_chart(
            data=spot_data,
            label=spot_labels,
            title=f"Pie Chart of Visitors in {destination.spot}",
        )

        per_spot_bar_chart = create_bar_chart(
            data=spot_data,
            label=spot_labels,
            title=f"Bar Chart of Visitors in {destination.spot}",
        )

        chart_bufs = [(per_spot_pie_chart),(per_spot_bar_chart)]

        return pdf_builder(chart_bufs, pdf_title="Per Tourist Spot Report", output_filename="per_tourist_spot_report.pdf")


class AnnuallyTouristReportView(CustomLoginRequiredMixin, View):
    template_name = "annually_report.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["tourists"] = Tourist.objects.all().order_by("-visit_date")
        return render(request, self.template_name, context)


class MonthlyTouristReportView(CustomLoginRequiredMixin, View):
    template_name = "monthly_report.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["tourists"] = Tourist.objects.all().order_by("-visit_date")
        return render(request, self.template_name, context)


class TouristWeeklyReportView(CustomLoginRequiredMixin, View):
    template_name = "report_weekly.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["tourists"] = Tourist.objects.all().order_by("-visit_date")
        return render(request, self.template_name, context)


class SpotView(CustomLoginRequiredMixin, View):
    template_name = "spots.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["tourist_spot"] = Spot.objects.all().order_by("-date_added")
        return render(request, self.template_name, context)

    def post(self, request):
        get_all_most_visited_spot = (
            Tourist.objects.values("destination__spot")
            .annotate(visit_count=Count("id"))
            .order_by("-visit_count")[:15]
        )

        spot_data = [spot["visit_count"] for spot in get_all_most_visited_spot]
        spot_labels = [spot["destination__spot"] for spot in get_all_most_visited_spot]

        most_visited_spot_bar_chart = create_bar_chart(
            data=spot_data,
            label=spot_labels,
            title="Most Visited Spots",
            yaxis="Visitor Count",
            xaxis="Tourist Spot",
        )


        most_visited_spot_pie_chart = create_pie_chart(
            data=spot_data,
            label=spot_labels,
            title="Most Visited Spots",
        )



        chart_bufs = [(most_visited_spot_bar_chart), (most_visited_spot_pie_chart)]

        return pdf_builder(chart_bufs, pdf_title="Tourist Spot Report", output_filename="most_visited_spots.pdf")


class SpotCategoryView(CustomLoginRequiredMixin, View):
    template_name = "category.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["categories"] = SpotCategory.objects.all().order_by("-date_added")
        return render(request, self.template_name, context)


class UsersView(CustomLoginRequiredMixin, View):
    template_name = "users.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["users"] = CustomUser.objects.all().order_by("-date_joined")
        return render(request, self.template_name, context)


class TouristView(CustomLoginRequiredMixin, View):
    template_name = "tourist.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["tourists"] = Tourist.objects.all().order_by("-visit_date")
        return render(request, self.template_name, context)


class AddTouristView(CustomLoginRequiredMixin, CreateView):
    form_class = TouristForm
    template_name = "includes/add.html"
    model = Tourist
    success_url = reverse_lazy("toursit")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Tourist added successfully.", extra_tags="success"
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Create New Tourist"
        context["button"] = "Create Tourist"
        return context


class PersonelAddTouristView(CustomLoginRequiredMixin, CreateView):
    form_class = PersonelTouristForm
    template_name = "includes/add.html"
    model = Tourist
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.destination = self.request.user.assigned_to
        messages.success(
            self.request, "Tourist added successfully.", extra_tags="success"
        )
        valid_form = super().form_valid(form)
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
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
            self.request, "Tourist Spot added successfully.", extra_tags="success"
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
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
        messages.success(self.request, "User added successfully.", extra_tags="success")
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
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
    success_url = reverse_lazy("category")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Category added successfully.", extra_tags="success"
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
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
    success_url = reverse_lazy("category")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "Category updated successfully.", extra_tags="success"
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
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
            self.request, "Tourist Spot updated successfully.", extra_tags="success"
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
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
            self.request,
            "Tourist information updated successfully.",
            extra_tags="success",
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
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
            self.request,
            "Tourist information removed successfully.",
            extra_tags="success",
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
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
            self.request,
            "Tourist spot information removed successfully.",
            extra_tags="success",
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
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
            self.request,
            "Category information removed successfully.",
            extra_tags="success",
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Remove Category"
        context["button"] = "Yes, Remove"
        return context


class UpdateUserView(CustomLoginRequiredMixin, UpdateView):
    pk_url_kwarg = "pk"
    form_class = UpdateUserForm
    template_name = "includes/add.html"
    model = CustomUser
    success_url = reverse_lazy("users")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "User updated successfully.", extra_tags="success"
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Update User"
        context["button"] = "Save Changes"
        return context


class DeleteUserView(CustomLoginRequiredMixin, DeleteView):
    pk_url_kwarg = "pk"
    template_name = "includes/delete.html"
    model = CustomUser
    success_url = reverse_lazy("users")

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        messages.success(
            self.request, "User removed successfully.", extra_tags="success"
        )
        return valid_form

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}", extra_tags="danger")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["name"] = "Remove User"
        context["button"] = "Yes, Remove"
        return context
