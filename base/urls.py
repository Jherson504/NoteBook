from django.urls import path
from . import views


urlpatterns = [
    # home
    path('', views.home, name='home'),
    # [+] AUTH [+]
    path('auth/', views.authenticate_user, name='auth'),
    # sign-in
    path('auth/sign-in/', views.sign_in_page, name='sign-in'),
    # login
    path('auth/login/', views.login_page, name='login'),
    # logout
    path('logout/', views.logout_page, name='logout'),
    # [-] AUTH [-]
    # [+] BOOK [+]
    # view
    path('book/view/<str:pk>/', views.book_view, name='book-view'),
    # edit
    path('book/edit/<str:pk>/', views.book_edit, name='book-edit'),
    # create
    path('book/create/', views.book_edit, name='book-create'),
    # [-] BOOK [-]
    # [+] ARTICLE [+]
    # view
    path('article/view/<str:pk>/', views.book_view, name='article-view'),
    # edit
    path('article/edit/<str:pk>/', views.book_edit, name='article-edit'),
    # create
    path('article/create/', views.book_edit, name='article-create'),
    # [-] ARTICLE [-]
    # [+] SECTION [+]
    # view
    path('section/view/<str:pk>/', views.book_view, name='section-view'),
    # edit
    path('section/edit/<str:pk>/', views.book_edit, name='section-edit'),
    # create
    path('section/create/', views.book_edit, name='section-create'),
    # [-] SECTION [-]
    # [!]RESET-DATA[!]
    path('data/reset/', views.data_reset, name='data-reset'),



]
