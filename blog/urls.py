from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.category, name='category'),
    path('category/view/<category_id>/<int:page_id>/', views.category_view, name='category_view'),
    path('post/<post_id>/', views.post, name='post'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('email/register/', views.email_register, name='email_register'),
]
