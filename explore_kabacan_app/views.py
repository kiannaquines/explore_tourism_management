import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
import plotly.io as pio
import plotly.graph_objects as go
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.units import inch
from django.contrib.auth import login, logout, authenticate

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))

def create_pie_chart(data, labels, title):
    fig = go.Figure(data=[go.Pie(labels=labels, values=data, hole=0.3)])
    fig.update_layout(title=title)

    buf = BytesIO()
    pio.write_image(fig, buf, format="png")
    buf.seek(0)
    return buf


def create_bar_chart(monthly_data):
    month_names = [
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
    ]

    fig = go.Figure(data=[go.Bar(x=month_names, y=monthly_data)])

    fig.update_layout(
        title="Monthly Visitors",
        xaxis_title="Month",
        yaxis_title="Visitor Count",
    )

    buf = BytesIO()
    pio.write_image(fig, buf, format="png")
    buf.seek(0)
    return buf


def generate_pdf_report(request):
    gender_counts = Tourist.objects.values("gender").annotate(count=Count("gender"))
    gender_data = [gender["count"] for gender in gender_counts]
    gender_labels = [gender["gender"] for gender in gender_counts]
    gender_chart_buf = create_pie_chart(
        gender_data, gender_labels, "Gender Distribution"
    )

    today = datetime.today()
    age_data = {"0-18": 0, "19-30": 0, "31-40": 0, "41-50": 0, "51+": 0}
    for tourist in Tourist.objects.all():
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
        Tourist.objects.values("visit_date__month")
        .annotate(count=Count("id"))
        .order_by("visit_date__month")
    )

    monthly_data = [0] * 12
    for visitor in monthly_visitors:
        month = visitor["visit_date__month"] - 1
        monthly_data[month] = visitor["count"]

    monthly_chart_buf = create_bar_chart(monthly_data)

    spot_counts = Tourist.objects.values("destination__spot").annotate(
        count=Count("id")
    )
    spot_data = [spot["count"] for spot in spot_counts]
    spot_labels = [spot["destination__spot"] for spot in spot_counts]
    spot_chart_buf = create_pie_chart(spot_data, spot_labels, "Most Visitors Distribution per Spot")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="tourist_report.pdf"'

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=40,
        leftMargin=40,
        topMargin=10,
        bottomMargin=72,
        pagesize=letter,
    )

    doc.title = "Statiscal Document for Explore Kabacan"
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    header_style = ParagraphStyle(
        "Header",
        parent=styles["Heading1"],
        fontSize=13,
        spaceAfter=0,
        alignment=1,
        textColor=colors.black,
    )

    title = Paragraph("Explore Kabacan Management System", header_style)
    third_title = Paragraph(f"Date Generated: {today.strftime('%Y-%m-%d')}", header_style)
    second_title = Paragraph("Tourist Report", header_style)
    elements.append(title)
    elements.append(third_title)
    elements.append(second_title)

    elements.append(Paragraph("<br />", normal_style))

    gender_image = ImageReader(gender_chart_buf)
    gender_width, gender_height = gender_image.getSize()
    aspect_ratio = gender_height / gender_width
    new_width = 440
    new_height = new_width * aspect_ratio
    gender_chart = Image(gender_chart_buf, width=new_width, height=new_height)
    elements.append(gender_chart)

    age_image = ImageReader(age_chart_buf)
    age_width, age_height = age_image.getSize()
    aspect_ratio = age_height / age_width
    new_width = 440
    new_height = new_width * aspect_ratio
    age_chart = Image(age_chart_buf, width=new_width, height=new_height)
    elements.append(age_chart)

    monthly_image = ImageReader(monthly_chart_buf)
    monthly_width, monthly_height = monthly_image.getSize()
    aspect_ratio = monthly_height / monthly_width
    new_width = 440
    new_height = new_width * aspect_ratio
    monthly_chart = Image(monthly_chart_buf, width=new_width, height=new_height)
    elements.append(monthly_chart)

    spot_image = ImageReader(spot_chart_buf)
    spot_width, spot_height = spot_image.getSize()
    aspect_ratio = spot_height / spot_width
    new_width = 440
    new_height = new_width * aspect_ratio
    spot_chart = Image(spot_chart_buf, width=new_width, height=new_height)
    elements.append(spot_chart)

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response


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
        context["visitors_history"] = Tourist.objects.all().order_by("visit_date")[:5]
        context["most_visited_spot"] = Spot.objects.annotate(
            visit_count=Count("tourist")
        ).order_by("-visit_count")[:6]
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
    success_url = reverse_lazy("spot")

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
    success_url = reverse_lazy("spot")

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
