from django.contrib import admin
from django.urls import path, include
from core.views import base, about, signup, login_view, get_login_status, logout_view

urlpatterns = [
    path('dj-admin/', admin.site.urls),
    path('admin/', include('admin_app.urls')),  # Includes admin app URLs
    path('', base),
    path("base/", base),
    path('about/', about),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('get-login-status/', get_login_status, name='get_login_status'),
    path('logout/', logout_view, name='logout'),
]
