from django.urls import path
from .views import *


app_name = 'website'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('shop/', ProductListView.as_view(), name='shop'),
]