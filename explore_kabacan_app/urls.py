from django.urls import path
from explore_kabacan_app.views import *

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),


    path('spot/list', SpotView.as_view(), name="spot"),
    path('category/list', SpotCategoryView.as_view(), name="category"),
    path('tourist/list', TouristView.as_view(), name="toursit"),

    path('tourist/add', AddTouristView.as_view(), name="add_tourist"),

]