"""
URL configuration for nsnemo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # new
from django.conf.urls.static import static #new
from nemo import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginPage),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('users/', views.registerPage , name="users"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('candidate/', views.candidate, name="candidate"),
    path('edit-candidate/<str:pk>/', views.editcandidate, name="edit-candidate"),
    path('search/', views.search, name="search"),
    path('allusers/', views.users, name="allusers"),
    path('profile/', views.profile, name="profile"),
    path('company/', views.company, name="company"),
    path('vessel/', views.vessel, name="vessel"),
    path('experience/', views.experience, name="experience"),
    path('rank/', views.rank, name="rank"),
    path('grade/', views.grade, name="grade"),
    path('port/', views.port, name="port"),
    path('port-agent/', views.portagent, name="port-agent"),
    path('hospital/', views.hospital, name="hospital"),
    path('document/', views.document, name="document"),
    path('vendor/', views.vendors, name="vendor"),
    path('vsl/', views.vsl, name="vsl"),
    path('view-candidate/', views.viewcandidate, name="view-candidate"),
    path('office-document/', views.viewdocument, name="office-document"),
    path('country/', views.country, name="country"),
    path('edit-country/<str:pk>/', views.editcountry, name="edit-country"),
    path('delete-country/<str:pk>/', views.editcountry, name="delete-country"),
    path('company-import/', views.importcompany, name="company-import"),
    path('company-export/', views.exportcompay, name="company-export"),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    
