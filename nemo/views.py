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
        rank = Rank.objects.all()
        vessel = Vessel.objects.all()
        exp = Experience.objects.all()
        context ={ 'filter':filter, 'candidate':candidate,'rank':rank ,'vessel':vessel,'exp':exp }
        return render(request,"advanced-search.html",context)
#search end here

#user start here
@login_required(login_url='login')
def users(request):
        
        customers = User.objects.all()
        context ={'customers':customers}
        return render(request,"allusers.html",context)
#user end here

                    
        
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










#grade port here







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



########Candidate start here
@login_required(login_url='login')
def viewcandidate(request):
        view = Candidate.objects.all()
        context ={ 'view':view }
        return render(request,"viewTemplates/view-candidate.html", context)
#candidate start here
@login_required(login_url='login')
@admin_only
def addcandidate(request):
    form = CreateCandidateForm()
    if request.method =='POST':
         form = CreateCandidateForm(request.POST,request.FILES)
         if form.is_valid():
              form.save()              
              messages.success(request,'Candidate created successfully ') 
              return redirect('/view-candidate')
    rank = Rank.objects.all()
    vessel = Vessel.objects.all()
    experience = Experience.objects.all()
    grade = Grade.objects.all()
    country = CountryName.objects.all()
    context ={'form':form, 'rank':rank,'vessel':vessel,'experience':experience,'grade':grade, 'country':country }
    
    return render(request,"addTemplates/add-candidate.html",context)
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
              messages.success(request,'Candidate Updated successfully ') 
              return redirect('/view-candidate')

    rank = Rank.objects.all()
    vessel = Vessel.objects.all()
    experience = Experience.objects.all()
    grade = Grade.objects.all()
    country = CountryName.objects.all()
    context ={'form':form, 'rank':rank,'vessel':vessel,'experience':experience,'grade':grade, 'country':country }
    return render(request,"editTemplates/edit-candidate.html",context)
###########
@login_required(login_url='login')
@admin_only
def deletecandidate(request ,pk):
    delete = Candidate.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-candidate')
    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-candidate.html",context)

##### candidate end here 



########### Country start here
@login_required(login_url='login')
def country(request):
        country = CountryName.objects.all()
        context ={ 'country':country }
        return render(request,"viewTemplates/view-country.html", context)

#############
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
              return redirect ("/view-country/")
    context ={'form':form}
    return render(request,"editTemplates/edit-country.html",context)

#################
def addcountry(request):
        form = CreateCountryForm()
        if request.method == 'POST':
              form = CreateCountryForm(request.POST)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'Country Added Successfully')
                    return redirect ("/view-country/")
        context ={ 'form':form}
        return render(request,"addTemplates/add-country.html", context)

###########
@login_required(login_url='login')
@admin_only
def deletecountry(request ,pk):
    delete = CountryName.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-country')
    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-country.html",context)

################
def importcountry(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = CountryName.objects.create(   
                        country_name = dbframe.country_name,
                        country_code = dbframe.country_code,
                        country_phone_code = dbframe.country_phone_code
                        )                
            obj.save()
            messages.success(request,"Country Data uploaded")      
            return redirect ("/view-country/")
    return render(request,"exportsTemplates/exportCountry.html")

##################
def exportcountry(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="Country.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['country_name'])     
      users = CountryName.objects.all().values_list('country_name')
      for user in users:
            writer.writerow(user)
      return response
#### Country End Here


####### Vendor Start here
#Vendor start here
@login_required(login_url='login')
def vendors(request):
        vendors = Vendors.objects.all()
        context ={ 'vendors':vendors}
        return render(request,"viewTemplates/view-vendor.html", context)

#################
def addvendors(request):
        form = CreateVendorForm()
        if request.method == 'POST':
              form = CreateVendorForm(request.POST)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'Vendor Added Successfully')
                    return redirect ("/view-vendor/")
        context ={ 'form':form}
        return render(request,"addTemplates/add-vendor.html", context)

###############
@login_required(login_url='login')
@admin_only
def editvendors(request ,pk):
    vendor = Vendors.objects.get(id = pk)
    form = CreateVendorForm( instance = vendor )
    if request.method =='POST':
         form = CreateVendorForm(request.POST, instance = vendor)
         if form.is_valid():
              form.save()              
              messages.success(request,'Vendor updated successfully ') 
              return redirect('/view-vendor')
    context ={'form':form}
    return render(request,"editTemplates/edit-vendor.html",context)

##############
@login_required(login_url='login')
@admin_only
def deletevendors(request ,pk):
    delete = Vendors.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-vendor')
    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-vendor.html",context)

################
def importvendors(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Vendors.objects.create(   
                        vendor_name = dbframe.vendor_name,
                        vendor_address = dbframe.vendor_address
                        )                
            obj.save()
            messages.success(request,"Vendors Data uploaded")      
            return redirect ("/view-vendor/")
    return render(request,"exportsTemplates/exportVendors.html")

##################
def exportvendors(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="Vendors.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['vendor_name','vendor_address'])     
      users = Vendors.objects.all().values_list('vendor_name','vendor_address')
      for user in users:
            writer.writerow(user)
      return response



######## Office Document Start Here
#Office Document start here
@login_required(login_url='login')
def adddocument(request):
        form = CreateDocumentForm()
        if request.method == 'POST':
              form = CreateDocumentForm(request.POST, request.FILES)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'VSL Name Added Successfully')
                    return redirect('/view-document')
        context ={ 'form':form}
        return render(request,"addTemplates/add-document.html", context)
###############
@login_required(login_url='login')
@admin_only
def editdocument(request ,pk):
    document = DocumentType.objects.get(id = pk)
    form = CreateDocumentForm( instance = document )
    if request.method =='POST':
         form = CreateDocumentForm(request.POST, instance = document)
         if form.is_valid():
              form.save()              
              messages.success(request,'Document updated successfully ') 
              return redirect('/view-document')
    context ={'form':form}
    return render(request,"editTemplates/edit-document.html",context)

################
@login_required(login_url='login')
def viewdocument(request):
        view = DocumentType.objects.all()
        context ={ 'view':view }
        return render(request,"viewTemplates/view-document.html", context)

###########
@login_required(login_url='login')
@admin_only
def deletedocument(request ,pk):
    delete = DocumentType.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-document')
    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-document.html",context)
################
def importdocument(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = DocumentType.objects.create(   
                        DocumentType = dbframe.DocumentType,
                        hide_expiry_date = dbframe.hide_expiry_date
                        )                
            obj.save()
            messages.success(request,"Document Data uploaded")      
            return redirect ("/view-document/")
    return render(request,"exportsTemplates/exportdocument.html")
##################
def exportdocument(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="DocumentType.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['DocumentType','hide_expiry_date'])     
      users = DocumentType.objects.all().values_list('DocumentType','hide_expiry_date')
      for user in users:
            writer.writerow(user)
      return response
### Document End Here


####### Hospital Start Here
#hospital start here
@login_required(login_url='login')
def hospital(request):
        hospital = Hospital.objects.all()
        context ={ 'hospital':hospital }
        return render(request,"viewTemplates/view-hospital.html" ,context)
## Hospital Add Here
@login_required(login_url='login')
@admin_only
def edithospital(request ,pk):

    hospital = Hospital.objects.get(id = pk)
    form = CreateHospitalForm( instance = hospital )
    if request.method =='POST':
         form = CreateHospitalForm(request.POST, instance = hospital)
         if form.is_valid():
              form.save()              
              messages.success(request,'Hospital updated successfully ') 
              return redirect('/view-hospital')
    context ={'form':form}
    return render(request,"editTemplates/edit-hospital.html",context)
#hospital start here
@login_required(login_url='login')
def addhospital(request):
        form = CreateHospitalForm()
        if request.method == 'POST':
              form = CreateHospitalForm(request.POST, request.FILES)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'Hospital Added Successfully')
                    return redirect('/view-hospital')
        context ={ 'form':form}
        return render(request,"addTemplates/add-hospital.html" ,context)
###########
@login_required(login_url='login')
@admin_only
def deletehospital(request ,pk):

    delete = Hospital.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-hospital')
    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-hospital.html",context)
################
def importhospital(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Hospital.objects.create(   
                        hospital_name = dbframe.hospital_name,
                        doctor_name = dbframe.doctor_name,
                        hospital_address = dbframe.hospital_address,
                        hospital_city = dbframe.hospital_city,
                        hospital_state = dbframe.hospital_state,
                        hospital_phone = dbframe.hospital_phone,
                        hospital_email = dbframe.hospital_email
                        
                        )
                            
            obj.save()
            messages.success(request,"Port Agent Data uploaded")      
            return redirect ("/view-hospital/")
    return render(request,"exportsTemplates/exportHospital.html")
##################
def exporthospital(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="Hospital.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['hospital_name','doctor_name','hospital_address','hospital_city','hospital_state','hospital_phone','hospital_email','hospital_image'])     
      users = Hospital.objects.all().values_list('hospital_name','doctor_name','hospital_address','hospital_city','hospital_state','hospital_phone','hospital_email','hospital_image')
      for user in users:
            writer.writerow(user)
      return response
##### Hospital End Here



##### Port agent start here
@login_required(login_url='login')
def portagent(request):
        portagent = PortAgent.objects.all()
        context ={ 'portagent':portagent }
        return render(request,"viewTemplates/view-portagent.html" ,context)
#######
@login_required(login_url='login')
def addportagent(request):
        form = CreatePortAgentForm()
        if request.method == 'POST':
              form = CreatePortAgentForm(request.POST)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'Port Agent Added Successfully')
        context ={ 'form':form}
        return render(request,"addTemplates/add-portagent.html" ,context)
########
@login_required(login_url='login')
@admin_only
def editportagent(request ,pk):

    country = PortAgent.objects.get(id = pk)
    form = CreatePortAgentForm( instance = country )

    if request.method =='POST':
         form = CreatePortAgentForm(request.POST, instance = country)
         if form.is_valid():
              form.save()              
              messages.success(request,'Port Agent updated successfully ')
              return redirect('/view-agentport') 
    context ={'form':form}
    return render(request,"editTemplates/edit-portagent.html" ,context)

@login_required(login_url='login')
@admin_only
def deleteportagent(request ,pk):

    delete = PortAgent.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-agentport')

    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-portagent.html",context)
################
def importportagent(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = PortAgent.objects.create(   
                        port_agent = dbframe.port_agent,
                        port_contact_person = dbframe.port_contact_person,
                        port_agent_address = dbframe.port_agent_address,
                        port_agent_phone = dbframe.port_agent_phone,
                        port_agent_email = dbframe.port_agent_email,
                        port_agent_city = dbframe.port_agent_city,
                        port_agent_state = dbframe.port_agent_state,
                        port_agent_country = dbframe.port_agent_country
                        )           
            obj.save()
            messages.success(request,"Port Agent Data uploaded")      
            return redirect ("/view-agentport/")
    return render(request,"exportsTemplates/exportPortagent.html")
##################
def exportportagent(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="PortAgentData.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['port_agent','port_contact_person','port_agent_address','port_agent_phone','port_agent_email','port_agent_city','port_agent_state','port_agent_country'])     
      users = PortAgent.objects.all().values_list('port_agent','port_contact_person','port_agent_address','port_agent_phone','port_agent_email','port_agent_city','port_agent_state','port_agent_country')
      for user in users:
            writer.writerow(user)
      return response

######Port agent end here


#### port start here
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
        return render(request,"viewTemplates/view-port.html", context)
#grade port end
@login_required(login_url='login')
def addport(request):
        form = CreatePortForm()
        if request.method == 'POST':
              form = CreatePortForm(request.POST)
              if form.is_valid():
                    form.save()
                    messages.success(request, "Port Added Successfully")          

        context ={'form':form}
        return render(request,"addTemplates/add-port.html", context)

@login_required(login_url='login')
@admin_only
def editport(request ,pk):

    edit = Port.objects.get(id = pk)
    form = CreatePortForm( instance = edit )

    if request.method =='POST':
         form = CreatePortForm(request.POST, instance = edit)
         if form.is_valid():
              form.save()              
              messages.success(request,'Port updated successfully ') 
              return redirect('/view-port/')

    context ={'form':form}
    return render(request,"editTemplates/edit-port.html",context)
##########
@login_required(login_url='login')
@admin_only
def deleteport(request ,pk):

    delete = Port.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-port')

    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-port.html",context)
##############
def importport(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Port.objects.create(   
                        port_name = dbframe.port_name
                        )           
            obj.save()
            messages.success(request,"Port Data uploaded")      
            return redirect ("/view-port/")
    return render(request,"exportsTemplates/exportPort.html")
#############
def exportport(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="PortData.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['port_name'])     
      users = Port.objects.all().values_list('port_name')

      for user in users:
            writer.writerow(user)
      return response





#### Grade star here

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
        return render(request,"viewTemplates/view-grade.html",context)
## Grade Add here
@login_required(login_url='login')
def addgrade(request):
        form = CreateGradeForm()
        if request.method=='POST':
              form = CreateGradeForm(request.POST)
              if form.is_valid():
                form.save()
                messages.success(request,'Grade added successfully ')
                return redirect('/view-grade/')

        context ={'form':form }
        return render(request,"addTemplates/add-grade.html",context)

@login_required(login_url='login')
@admin_only
def editgrade(request ,pk):

    edit = Grade.objects.get(id = pk)
    form = CreateGradeForm( instance = edit )

    if request.method =='POST':
         form = CreateGradeForm(request.POST, instance = edit)
         if form.is_valid():
              form.save()              
              messages.success(request,'Grade updated successfully ') 
              return redirect('/view-grade/')

    context ={'form':form}
    return render(request,"editTemplates/edit-grade.html",context)

@login_required(login_url='login')
@admin_only
def deletegrade(request ,pk):

    delete = Grade.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-grade')

    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-grade.html",context)


def importgrade(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Grade.objects.create(   
                        grade_name = dbframe.grade_name
                        )           
            obj.save()
            messages.success(request,"Grade Data uploaded")      
            return redirect ("/view-grade/")
    return render(request,"exportsTemplates/exportGrade.html")

def exportgrade(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="GradeData.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['grade_name'])     
      users = Grade.objects.all().values_list('grade_name')

      for user in users:
            writer.writerow(user)
      return response

##### Grade end here


##### Rank start here
#rank view here
@login_required(login_url='login')
def rank(request):
        rank = Rank.objects.all()
        context ={'rank':rank}
        return render(request,"viewTemplates/view-rank.html",context)

### rank edit here
@login_required(login_url='login')
@admin_only
def editrank(request ,pk):

    edit = Rank.objects.get(id = pk)
    form = CreateRankForm( instance = edit )

    if request.method =='POST':
         form = CreateRankForm(request.POST, instance = edit)
         if form.is_valid():
              form.save()              
              messages.success(request,'Rank updated successfully ') 
              return redirect('/view-rank/')

    context ={'form':form}
    return render(request,"editTemplates/edit-rank.html",context)

#Rank add here
@login_required(login_url='login')
def addrank(request):
        form = CreateRankForm()
        if request.method=='POST':
              form = CreateRankForm(request.POST)
              if form.is_valid():
                form.save()
                messages.success(request,'Rank added successfully ')
                return redirect('/view-rank/')

        context ={'form':form }
        return render(request,"addTemplates/add-rank.html",context)

## Rank delete Here
@login_required(login_url='login')
@admin_only
def deleterank(request ,pk):

    delete = Rank.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-rank')

    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-rank.html",context)


def importrank(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Rank.objects.create(   
                        rank_name = dbframe.rank_name,
                        rank_order = dbframe.rank_order,
                        rank_category = dbframe.rank_category
                        )           
            obj.save()
            messages.success(request,"Rank Data uploaded")      
            return redirect ("/view-rank/")
    return render(request,"exportsTemplates/exportRank.html")

def exportrank(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="RankData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Rank Name'])  
      writer.writerow(['rank_name','rank_order','rank_category'])     
      users = Rank.objects.all().values_list('rank_name','rank_order','rank_category')

      for user in users:
            writer.writerow(user)
      return response

######Rank end here

###### Experience start here

#experience end here
@login_required(login_url='login')
def experience(request):
        experience = Experience.objects.all()       

        context ={'experience':experience}
        return render(request,"viewTemplates/view-experience.html",context)
#experience end here

@login_required(login_url='login')
@admin_only
def editexperience(request ,pk):

    edit = Experience.objects.get(id = pk)
    form = CreateExperienceForm( instance = edit )

    if request.method =='POST':
         form = CreateExperienceForm(request.POST, instance = edit)
         if form.is_valid():
              form.save()              
              messages.success(request,'Experience updated successfully ') 

              return redirect('/view-experience/')

    context ={'form':form}
    return render(request,"editTemplates/edit-experience.html",context)

#experience end here
@login_required(login_url='login')
def addexperience(request):
        form = CreateExperienceForm()
        if request.method=='POST':
              form = CreateExperienceForm(request.POST)
              if form.is_valid():
                form.save()
                messages.success(request,'Experience added successfully ')
                return redirect('/view-experience')

        context ={'form':form }
        return render(request,"addTemplates/add-experience.html",context)

## delete experience
@login_required(login_url='login')
@admin_only
def deleteexperience(request ,pk):

    delete = Experience.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-experience')

    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-experience.html",context)

#experience end here
def importexperience(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Experience.objects.create(   
                        experience = dbframe.experience
                        )           
            obj.save()
            messages.success(request,"Experience Data uploaded")      

            return redirect ("/view-experience/")
    return render(request,"exportsTemplates/exportExperience.html")

def exportexperience(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="ExperienceData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Experience Name'])  
      writer.writerow(['experience'])     
      users = Experience.objects.all().values_list('experience')

      for user in users:
            writer.writerow(user)
      return response



##### VSL starts here
#Edit VSL start here
@login_required(login_url='login')
@admin_only
def editvsl(request ,pk):

    editvessel = Vessel.objects.get(id = pk)
    form = CreateVesselForm( instance = editvessel )

    if request.method =='POST':
         form = CreateVesselForm(request.POST, instance = editvessel)
         if form.is_valid():
              form.save()              
              messages.success(request,'Vessel updated successfully ') 

              return redirect('/view-vessel/')

    vessel = Vessel.objects.all()
    context ={'form':form,'vessel':vessel }
    return render(request,"editTemplates/edit-vessel.html",context)


@login_required(login_url='login')
def addvsl(request):
        form = CreateVslForm()
        if request.method == 'POST':
              form = CreateVslForm(request.POST)
              if form.is_valid():
                    form.save()
                    messages.success(request, 'VSL Name Added Successfully')

        context ={ 'form':form}
        return render(request,"addTemplates/add-vsl.html", context)


@login_required(login_url='login')
def vsl(request):
        vsl = VslType.objects.all()

        context ={ 'vsl':vsl }
        return render(request,"viewTemplates/view-vsl.html", context)

def importvsl(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(file)
            for dbframe in dbframe.itertuples():
                  obj = Vessel.objects.create(   
                        vsl_name = dbframe.vsl_name,
                        vsl_type = dbframe.vsl_type,
                        vsl_company = dbframe.vsl_company,
                        IMO_Number = dbframe.IMO_Number,
                        vsl_flag = dbframe.vsl_flag
                        )           
            obj.save()
            messages.success(request,"VSL Data uploaded")      

            return redirect ("/view-vsl/")
    return render(request,"exportsTemplates/exportVsl.html")

def exportvsl(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="VslData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Vsl Name'])  
      writer.writerow(['vsl_name','vsl_type','vsl_company','IMO_Number','vsl_flag'])     
      users = VslType.objects.all().values_list('vsl_name','vsl_type','vsl_company','IMO_Number','vsl_flag')

      for user in users:
            writer.writerow(user)
      return response

#####vessel start here
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
        return render(request,"viewTemplates/view-vessel.html" ,context)
# vessel end here

#vessel start here
@login_required(login_url='login')
def addvessel(request):
        form = CreateVesselForm()
        if request.method =='POST':
            form = CreateVesselForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Vessel added successfully ')
                return redirect('/view-vessel/')
        
        context ={'form':form}
        return render(request,"addTemplates/add-vessel.html" ,context)
# vessel end here
#Edit company start here
@login_required(login_url='login')
@admin_only
def editvessel(request ,pk):

    editvessel = Vessel.objects.get(id = pk)
    form = CreateVesselForm( instance = editvessel )

    if request.method =='POST':
         form = CreateVesselForm(request.POST, instance = editvessel)
         if form.is_valid():
              form.save()              
              messages.success(request,'Vessel updated successfully ') 

              return redirect('/view-vessel/')

    vessel = Vessel.objects.all()
    context ={'form':form,'vessel':vessel }
    return render(request,"editTemplates/edit-vessel.html",context)

#vessel end here
@login_required(login_url='login')
@admin_only
def deletevessel(request ,pk):

    delete = Vessel.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-vessel')

    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-vessel.html",context)


# import using django import   
def importvessel(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(file)
            for dbframe in dbframe.itertuples():
                  obj = Vessel.objects.create(   
                        vessel_name = dbframe.vessel_name
                        )           
            obj.save()
            messages.success(request,"Vessel Data uploaded")      

            return redirect ("/view-vessel/")
    return render(request,"exportsTemplates/exportVessel.html")

def exportvessel(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="VesselData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Vessel Name'])  
      writer.writerow(['vessel_name'])     
      users = Vessel.objects.all().values_list('vessel_name')

      for user in users:
            writer.writerow(user)
      return response



######Edit company start here
@login_required(login_url='login')
@admin_only
def editcompany(request ,pk):

    editcompany = Company.objects.get(id = pk)
    form = CreateCompanyForm( instance = editcompany )

    if request.method =='POST':
         form = CreateCompanyForm(request.POST, instance = editcompany)
         if form.is_valid():
              form.save()              
              messages.success(request,'Country updated successfully ') 

    company = Company.objects.all()
    context ={'form':form,'companys':company }
    return render(request,"editTemplates/edit-company.html",context)


##company start here
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
           
    return render(request,"viewTemplates/view-company.html", context)
#company end here

#company start here
@login_required(login_url='login')
def addcompany(request):
    form = CreateCompanyForm()
    
    if request.method =='POST':
         form = CreateCompanyForm(request.POST)
         if form.is_valid():
              form.save()
              messages.success(request,'Company added successfully ') 
    companys = Company.objects.all()

    context ={'form':form,'companys':companys}
           
    return render(request,"addtemplates/add-company.html", context)
#company end here
@login_required(login_url='login')
@admin_only
def deletecompany(request ,pk):

    delete = Company.objects.get(id = pk)
    if request.method == 'POST':
          delete.delete()
          messages.success(request, "Deleted successfully")
          return redirect('/view-company')

    context ={'delete':delete}
    return render(request,"deleteTemplates/delete-company.html",context)

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
            #print(path)
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

            return redirect ("/view-company/")
    return render(request,"exportsTemplates/exportCompany.html")

def exportcompany(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="CompanyData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Company Name'])  
      writer.writerow(['company_name','contact_person','address','Phone','Email','Management'])     
      users = Company.objects.all().values_list('company_name','contact_person' , 'address' , 'phone','email','management')

      for user in users:
            writer.writerow(user)
      return response
      
                   




                    
                    
            





