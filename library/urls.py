from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('zvirata/', views.seznam_zvirat, name='seznam_zvirat'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('zvire/<int:zvire_id>/', views.detail_zvirete, name='detail_zvirete'),
    path('zvire/<int:zvire_id>/edit/', views.upravit_zvire, name='upravit_zvire'),
    path('zvire/<int:zvire_id>/delete/', views.smazat_zvire, name='smazat_zvire'),
    path('utulky/', views.seznam_utulku, name='seznam_utulku'),
    path('archiv/', views.archiv_zvirat, name='archiv_zvirat'),
]
