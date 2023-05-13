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

    
    path('search/', views.search, name="search"),
    path('allusers/', views.users, name="allusers"),
    path('profile/', views.profile, name="profile"),
    
    
    
    
    
    
    
    
    
    
    
    
    path('office-document/', views.viewdocument, name="office-document"),
    # view paths
    path('view-country/', views.country, name="view-country"),
    path('view-company/', views.company, name="view-company"),
    path('view-vessel/', views.vessel, name="view-vessel"),
    path('view-vsl/', views.vsl, name="view-vsl"),
    path('view-experience/', views.experience, name="view-experience"),
    path('view-rank/', views.rank, name="view-rank"),
    path('view-grade/', views.grade, name="view-grade"),
    path('view-port/', views.port, name="view-port"),
    path('view-agentport/', views.portagent, name="view-agentport"),
    path('view-hospital/', views.hospital, name="view-hospital"),
    path('view-document/', views.viewdocument, name="view-document"),
    path('view-vendor/', views.vendors, name="view-vendor"),
    path('view-candidate/', views.viewcandidate, name="view-candidate"),
    #add paths
    path('add-candidate/', views.addcandidate, name="add-candidate"),
    path('add-company/', views.addcompany, name="add-company"),
    path('add-vessel/', views.addvessel, name="add-vessel"),
    path('add-vsl/', views.addvsl, name="add-vsl"),
    path('add-experience/', views.addexperience, name="add-experience"),
    path('add-rank/', views.addrank, name="add-rank"),
    path('add-grade/', views.addgrade, name="add-grade"),
    path('add-port/', views.addport, name="add-port"),
    path('add-agentport/', views.addportagent, name="add-agentport"),
    path('add-hospital/', views.addhospital, name="add-hospital"),
    path('add-document/', views.adddocument, name="add-document"),
    path('add-vendor/', views.addvendors, name="add-vendor"),
    path('add-country/', views.addcountry, name="add-country"),
    # edit paths
    path('edit-country/<str:pk>/', views.editcountry, name="edit-country"),
    path('edit-company/<str:pk>/', views.editcompany, name="edit-company"),
    path('edit-vessel/<str:pk>/', views.editvessel, name="edit-vessel"),
    path('edit-experience/<str:pk>/', views.editexperience, name="edit-experience"),
    path('edit-rank/<str:pk>/', views.editrank, name="edit-rank"),
    path('edit-grade/<str:pk>/', views.editgrade, name="edit-grade"),
    path('edit-port/<str:pk>/', views.editport, name="edit-port"),
    path('edit-agentport/<str:pk>/', views.editportagent, name="edit-agentport"),
    path('edit-hospital/<str:pk>/', views.edithospital, name="edit-hospital"),
    path('edit-document/<str:pk>/', views.editdocument, name="edit-document"),
    path('edit-vendor/<str:pk>/', views.editvendors, name="edit-vendor"),
    path('edit-country/<str:pk>/', views.editcountry, name="edit-country"),
    path('edit-candidate/<str:pk>/', views.editcandidate, name="edit-candidate"),
    #delete paths
    path('delete-company/<str:pk>/', views.deletecompany, name="delete-company"),
    path('delete-vessel/<str:pk>/', views.deletevessel, name="delete-vessel"),
    path('delete-experience/<str:pk>/', views.deleteexperience, name="delete-experience"),
    path('delete-rank/<str:pk>/', views.deleterank, name="delete-rank"),
    path('delete-grade/<str:pk>/', views.deletegrade, name="delete-grade"),
    path('delete-port/<str:pk>/', views.deleteport, name="delete-port"),
    path('delete-agentport/<str:pk>/', views.deleteportagent, name="delete-agentport"),
    path('delete-hospital/<str:pk>/', views.deletehospital, name="delete-hospital"),
    path('delete-document/<str:pk>/', views.deletedocument, name="delete-document"),
    path('delete-vendor/<str:pk>/', views.deletevendors, name="delete-vendor"),
    path('delete-country/<str:pk>/', views.deletecountry, name="delete-country"),
    path('delete-candidate/<str:pk>/', views.deletecandidate, name="delete-candidate"),
    #export paths
    path('company-import/', views.importcompany, name="company-import"),
    path('company-export/', views.exportcompany, name="company-export"),
    path('vessel-import/', views.importvessel, name="vessel-import"),
    path('vessel-export/', views.exportvessel, name="vessel-export"),
    path('vsl-import/', views.importvsl, name="vsl-import"),
    path('vsl-export/', views.exportvsl, name="vsl-export"),
    path('experience-import/', views.importexperience, name="experience-import"),
    path('experience-export/', views.exportexperience, name="experience-export"),
    path('rank-import/', views.importrank, name="rank-import"),
    path('rank-export/', views.exportrank, name="rank-export"),
    path('grade-import/', views.importgrade, name="grade-import"),
    path('grade-export/', views.exportgrade, name="grade-export"),
    path('port-import/', views.importport, name="port-import"),
    path('port-export/', views.exportport, name="port-export"),
    path('agentport-import/', views.importportagent, name="agentport-import"),
    path('agentport-export/', views.exportportagent, name="agentport-export"),
    path('hospital-import/', views.importhospital, name="hospital-import"),
    path('hospital-export/', views.exporthospital, name="hospital-export"),
    path('document-import/', views.importdocument, name="document-import"),
    path('document-export/', views.exportdocument, name="document-export"),
    path('vendor-import/', views.importvendors, name="vendor-import"),
    path('vendor-export/', views.exportvendors, name="vendor-export"),
    path('country-import/', views.importcountry, name="country-import"),
    path('country-export/', views.exportcountry, name="country-export"),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    
