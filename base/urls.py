"""URL Patterns"""

from django.urls import path
from . import views
from .views import TransactionListView, CategoryListView

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("tracker", views.TrackerPageView.as_view(), name="tracker"),
    path("about", views.AboutPageView.as_view(), name="about"),
    path("contact", views.ContactPageView.as_view(), name="contact"),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
]