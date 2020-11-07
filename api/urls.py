from django.urls import path
from .views import ItemListView

urlpatterns = [
    path('item', ItemListView.as_view()),
]