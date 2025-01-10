from django.urls import path

from packages import views

# Add some more helpful routes
urlpatterns = [
    path("<str:package_name>", views.PackageView.as_view()),
    path("<str:package_name>/<str:range>", views.PackageView.as_view()),
]
