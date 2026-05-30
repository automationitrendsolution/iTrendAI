from django.urls import path
from . import views

app_name = 'iTrendAI'
urlpatterns = [
    path('agents/',                      views.agents,                    name='agents'),
    path('newproductresearch/',          views.newproductresearch,        name='newproductresearch'),
    path('newproductresearchreport/',    views.newproductresearchreport,  name='newproductresearchreport'),
    path('report/<int:pk>/',             views.view_report,               name='view_report'),
    path('report/<int:pk>/delete/',      views.delete_report,             name='delete_report'),
]
