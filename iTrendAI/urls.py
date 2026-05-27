from django.urls import path
from . import views

app_name = 'iTrendAI'
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product_research/', views.product_research, name='product_research'),
    path('product_research/overview/<int:pk>/', views.product_research_overview, name='product_research_overview'),
    path('product_research/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('product_research/<int:pk>/delete/', views.delete_project, name='delete_project'),
]
