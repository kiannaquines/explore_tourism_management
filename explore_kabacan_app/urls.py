from django.urls import path
from explore_kabacan_app.views import *

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    # View
    path("spot/list", SpotView.as_view(), name="spot"),
    path("category/list", SpotCategoryView.as_view(), name="category"),
    path("tourist/list", TouristView.as_view(), name="toursit"),
    path("users/list", UsersView.as_view(), name="users"),

    # Add View
    path("users/add", AddUserView.as_view(), name="add_user"),
    path("tourist/add", AddTouristView.as_view(), name="add_tourist"),
    path("spot/add", AddSpotView.as_view(), name="add_spot"),
    path("category/add", AddCategorySpotView.as_view(), name="add_category"),

    # Update View
    path("tourist/update/<int:pk>", UpdateTouristView.as_view(), name="update_tourist"),
    path("spot/update/<int:pk>", UpdateSpotView.as_view(), name="update_spot"),
    path("category/update/<int:pk>",UpdateCategorySpotView.as_view(), name="update_category"),

    # Delete View
    path("tourist/delete/<int:pk>", DeleteTouristView.as_view(), name="delete_tourist"),
    path("spot/delete/<int:pk>", DeleteSpotView.as_view(), name="delete_spot"),
    path("category/delete/<int:pk>", DeleteCategorySpotView.as_view(), name="delete_category"),
]
