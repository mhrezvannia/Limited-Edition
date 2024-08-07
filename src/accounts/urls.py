from django.urls import path
from .views import logoutview, CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logoutview, name='logout')
]