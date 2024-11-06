from django.urls import path

from . import views

urlpatterns = [
    path('call/get/<str:source>/', views.get_call_record),
    path('call/get/<str:source>/<str:month>/', views.get_call_record),
    path('call/get/<str:source>/<str:month>/<str:year>',
         views.get_call_record
         ),

    path('call/post', views.post_call_record),
]
