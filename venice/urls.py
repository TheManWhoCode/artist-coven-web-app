from django.urls import path
from . import views
urlpatterns= [

    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/signup/',views.signup,name='signup'),
    path('dashboard/contribute/',views.upload_art,name='contribute'),
    path('dashboard/exhibition/',views.see_art,name='exhibition'),
]