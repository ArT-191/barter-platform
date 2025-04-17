from django.urls import path
from . import views

app_name = "exchange"

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('ad/create/', views.ad_create, name='ad_create'),
    path('ad/<int:ad_id>/edit/', views.ad_edit, name='ad_edit'),
    path('ad/<int:ad_id>/delete/', views.ad_delete, name='ad_delete'),
    path('proposal/create/', views.proposal_create, name='proposal_create'),
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposal/<int:proposal_id>/update/', views.proposal_update, name='proposal_update'),
]
