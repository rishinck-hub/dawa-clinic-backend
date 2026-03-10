from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import LoginView
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('clinic.urls')),
    path('api/login/', LoginView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
