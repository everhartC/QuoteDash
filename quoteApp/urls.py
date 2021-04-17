from django.urls import path
from . import views

urlpatterns = [
    path('', views.quotes),
    path('addQuote', views.addQuote),
    path('like/<int:quote_id>', views.addLike),
    path('deleteQuote/<int:quote_id>', views.deleteQuote),
]