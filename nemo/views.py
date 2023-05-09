from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.contrib import messages
from nemo.forms import *
from django.contrib.auth.decorators import login_required
from nemo.decorators import unauthenticated_user,admin_only
from nemo.models import *
from nemo.filters import *
import pandas as pd
from django.conf import settings
#from nemo.resources import *
from django.core.files.storage import FileSystemStorage
import csv


#users start here
def registerPage(request):
    form = CreateUserForm()

    if request.method =='POST':
         form = CreateUserForm(request.POST)
         if form.is_valid():
              user = form.save()
              username = form.cleaned_data.get('username')
              permission = request.POST['permission']
              group = Group.objects.get(name=permission)
              user.groups.add(group)
              
              messages.success(request,'User created successfully ' + username) 
    customers = User.objects.all()
    groups = Group.objects.all()
    

    context ={'form':form,'customers':customers,'groups':groups }
    return render(request,"users.html",context)
#users end here

#login start here
@unauthenticated_user
def loginPage(request):        
            if request.method =='POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username,password=password)
                if user is not None:
                        login(request,user)
                        return redirect('/dashboard/')
                else:
                    messages.info(request,'username or password incorrect')

            context = {}
            return render(request,"login.html", context)
#login end here
           
#logout start here
def logoutUser(request):
    logout(request)
    return redirect('login')
#logout end here

#dashboard start here
@login_required(login_url='login')
def dashboard(request):
        return render(request,"dashboard.html")
#dashboard end here

#search start here
@login_required(login_url='login')
def search(request):
        candidate = Candidate.objects.all()
        filter = CandidateFilter(request.GET, queryset=candidate)
        candidate = filter.qs
        context ={ 'filter':filter, 'candidate':candidate }
        return render(request,"advanced-search.html",context)
#search end here

#user start here
@login_required(login_url='login')
def users(request):
        
        customers = User.objects.all()
        context ={'customers':customers}
        return render(request,"allusers.html",context)
#user end here

#candidate start here
@login_required(login_url='login')
@admin_only
def candidate(request):

    form = CreateCandidateForm()
    
    if request.method =='POST':
         form = CreateCandidateForm(request.POST,request.FILES)
         if form.is_valid():
              form.save()              
              messages.success(request,'Candidate created successfully ') 
    rank = Rank.objects.all()
    vessel = Vessel.objects.all()
    experience = Experience.objects.all()
    grade = Grade.objects.all()
    country = CountryName.objects.all()

    context ={'form':form, 'rank':rank,'vessel':vessel,'experience':experience,'grade':grade, 'country':country }
    return render(request,"add-candidate.html",context)
#candidate end here 
# 
#Edit candidate start here
@login_required(login_url='login')
@admin_only
def editcandidate(request ,pk):

    candidate = Candidate.objects.get(id = pk)
    form = CreateCandidateForm( instance = candidate )

    if request.method =='POST':
         form = CreateCandidateForm(request.POST,request.FILES, instance = candidate)
         if form.is_valid():
              form.save()              
              messages.success(request,'Candidate created successfully ') 


    rank = Rank.objects.all()
    vessel = Vessel.objects.all()
    experience = Experience.objects.all()
    grade = Grade.objects.all()
    country = CountryName.objects.all()
    context ={'form':form, 'rank':rank,'vessel':vessel,'experience':experience,'grade':grade, 'country':country }
    return render(request,"add-candidate.html",context)
#Edit candidate end here                     
        
#company profile here
@login_required(login_url='login')
def profile(request):
        user = request.user.profile
        form = CreateProfileForm(instance=user)
        if request.method =='POST':
         form = CreateProfileForm(request.POST,request.FILES, instance= user)
         if form.is_valid():
              form.save()
              messages.success(request,'Profile updated successfully ') 
        context ={
              'form':form
        }
        return render(request,"profile.html", context)
#company profile end here


#company start here
@login_required(login_url='login')
def company(request):
    form = CreateCompanyForm()
    
    if request.method =='POST':
         form = CreateCompanyForm(request.POST)
         if form.is_valid():
              form.save()
              messages.success(request,'Company added successfully ') 
    companys = Company.objects.all()

    context ={'form':form,'companys':companys}
           
    return render(request,"company.html", context)
#company end here

#vessel start here
@login_required(login_url='login')
def vessel(request):
        form = CreateVesselForm()
        if request.method =='POST':
            form = CreateVesselForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Vessel added successfully ')
        vessel = Vessel.objects.all()      
        context ={'form':form, 'vessel':vessel}
        return render(request,"add-vessel.html" ,context)
# vessel end here

#experience end here
@login_required(login_url='login')
def experience(request):
        form = CreateExperienceForm()
        if request.method=='POST':
              form = CreateExperienceForm(request.POST)
              if form.is_valid():
                form.save()
                messages.success(request,'Experience added successfully ')
        experience = Experience.objects.all()       

        context ={'form':form ,'experience':experience}
        return render(request,"add-experience.html",context)
#experience end here

#rank end here
@login_required(login_url='login')
def rank(request):
        form = CreateRankForm()
        if request.method=='POST':
              form = CreateRankForm(request.POST)
              if form.is_valid():
                form.save()
                messages.success(request,'Rank added successfully ')
        rank = Rank.objects.all()       

        context ={'form':form ,'rank':rank}
        return render(request,"add-rank.html",context)
#rank end here


#grade start here
@login_required(login_url='login')
def grade(request):
        form = CreateGradeForm()
        if request.method == 'POST':
              form =CreateGradeForm(request.POST)
              if form.is_valid():
                form.save()
                messages.success(request, 'Grade added successfully')
        grade = Grade.objects.all()                
        context={'form':form,'grade':grade}
        return render(request,"add-grade.html",context)
#grade end here

#grade port here
@login_required(login_url='login')
def port(request):
        form = CreatePortForm()
        if request.method == 'POST':
              form = CreatePortForm(request.POST)
              if form.is_valid():
                    form.save()
                    messages.success(request, "Port Added Successfully")
        port = Port.objects.all()            

        context ={'form':form,'port':port}
        return render(request,"add-port.html", context)
#grade port end

#port agent start here
@login_required(login_url='login')
def portagent(request):
        form = CreatePortAgentForm()
        if request.method == 'POST':
              form = CreatePortAgentForm(request.POST)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'Port Agent Added Successfully')
        portagent = PortAgent.objects.all()

        context ={ 'form':form, 'portagent':portagent }
        return render(request,"add-port-agent.html" ,context)
#port agent end here

#hospital start here
@login_required(login_url='login')
def hospital(request):
        form = CreateHospitalForm()
        if request.method == 'POST':
              form = CreateHospitalForm(request.POST, request.FILES)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'Port Agent Added Successfully')
        hospital = Hospital.objects.all()

        context ={ 'form':form, 'hospital':hospital }
        return render(request,"add-hospital.html" ,context)


#Document start here
@login_required(login_url='login')
def document(request):
        form = CreateDocumentForm()
        if request.method == 'POST':
              form = CreateDocumentForm(request.POST)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'Document Added Successfully')
        document = DocumentType.objects.all()

        context ={ 'form':form,'document':document }
        return render(request,"add-document.html", context)

#Document start here
@login_required(login_url='login')
def vendors(request):
        form = CreateVendorForm()
        if request.method == 'POST':
              form = CreateVendorForm(request.POST)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'Vendor Added Successfully')
        vendor = Vendors.objects.all()

        context ={ 'form':form ,'vendor':vendor }
        return render(request,"add-vendor.html", context)


#Document start here
@login_required(login_url='login')
def vsl(request):
        form = CreateVslForm()
        if request.method == 'POST':
              form = CreateVslForm(request.POST)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'VSL Name Added Successfully')
        vsl = VslType.objects.all()

        context ={ 'form':form ,'vsl':vsl }
        return render(request,"add-vsl.html", context)

#Candidate start here
@login_required(login_url='login')
def viewcandidate(request):
        view = Candidate.objects.all()

        context ={ 'view':view }
        return render(request,"list-candidate.html", context)

#Office Document start here
@login_required(login_url='login')
def viewdocument(request):
        form = CreateOfficeForm()
        if request.method == 'POST':
              form = CreateOfficeForm(request.POST, request.FILES)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'VSL Name Added Successfully')
        view = OfficeDocument.objects.all()
        context ={ 'form':form, 'view':view }
        return render(request,"office-document.html", context)

#Country start here
@login_required(login_url='login')
def country(request):
        form = CreateCountryForm()
        if request.method == 'POST':
              form = CreateCountryForm(request.POST, request.FILES)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'Country Added Successfully')
        country = CountryName.objects.all()
        context ={ 'form':form, 'country':country }
        return render(request,"add-country.html", context)

#Edit candidate start here
@login_required(login_url='login')
@admin_only
def editcountry(request ,pk):

    country = CountryName.objects.get(id = pk)
    form = CreateCountryForm( instance = country )

    if request.method =='POST':
         form = CreateCountryForm(request.POST, instance = country)
         if form.is_valid():
              form.save()              
              messages.success(request,'Country updated successfully ') 

    country = CountryName.objects.all()
    context ={'form':form,'country':country }
    return render(request,"add-country.html",context)
#Edit candidate end here  
# 
# import using django import   
def importcompany(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            print(path)
            for dbframe in dbframe.itertuples():
                  obj = Company.objects.create(   
                        company_name = dbframe.company_name,
                        contact_person = dbframe.contact_person,
                        address = dbframe.address,
                        phone = dbframe.phone,
                        email = dbframe.email,
                        management = dbframe.management
                        )           
            obj.save()
            messages.success(request,"Company Data uploaded")      

    return redirect ("/company/")

def exportcompay(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="CompanyData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Company Name'])  
      writer.writerow(['company_name','contact_person','address','Phone','Email','Management'])     
      users = Company.objects.all().values_list('company_name','contact_person' , 'address' , 'phone','email','management')

      for user in users:
            writer.writerow(user)
      return response
      
                   




                    
                    
            





