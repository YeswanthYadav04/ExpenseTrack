from django.urls import path, include
from . import views

urlpatterns = [

    # Home page
    path('', views.home, name='home'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Transactions
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),

    # Registration
    path('register/', views.register, name='register'),

    # Django authentication (login/logout/password)
    path('accounts/', include('django.contrib.auth.urls')),
]