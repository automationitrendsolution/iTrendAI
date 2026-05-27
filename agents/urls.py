from django.urls import path
from .views import ProductResearchAgentView

app_name = 'agents'

urlpatterns = [
    path('product-research/', ProductResearchAgentView.as_view(), name='product_research'),
    path('product-research/<int:pk>/', ProductResearchAgentView.as_view(), name='product_research_detail'),
]
