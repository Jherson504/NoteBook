from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('user-authenticate/', views.authenticate_user, name='user-authenticate'),
    path('login/', views.login_page, name='login'),
    path('book/create/', views.book_create, name='book-create'),
    path('section/create/<str:pk>/',
         views.section_create, name='section-create'),

    path('book/view/<str:pk>/', views.book_view, name='book-view'),
    path('book/edit/<str:pk>/', views.book_edit, name='book-edit'),

    path('sign-in/', views.login_page, name='sign-in'),
    path('data/reset/', views.data_reset, name='data-reset'),

    path('logout/', views.logout_page, name='logout'),


]
