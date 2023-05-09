from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    user_image = models.ImageField(upload_to='userprofile', null=True)

    def __str__(self):
        return self.name
    


class Candidate(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200 , null=True)
    rank = models.CharField(max_length=200 , null=True)
    availibity = models.CharField(max_length=200 , null=True)
    nationality = models.CharField(max_length=200 , null=True)
    marital_status = models.CharField(max_length=200 , null=True)
    date_birth = models.CharField(max_length=200 , null=True)
    birth_place = models.CharField(max_length=200 , null=True)
    worked_with_us = models.CharField(max_length=200 , null=True)
    vessel_type = models.CharField(max_length=200 , null=True)
    experience = models.CharField(max_length=200 , null=True)
    zone = models.CharField(max_length=200 , null=True)
    grade = models.CharField(max_length=200 , null=True)
    boiler_suit_size = models.CharField(max_length=200 , null=True)
    safety_shoe_size = models.CharField(max_length=200 , null=True)
    height = models.CharField(max_length=200 , null=True)
    weight = models.CharField(max_length=200 , null=True)
    license_country = models.CharField(max_length=200 , null=True)
    INDoS_Number = models.CharField(max_length=200 , null=True)
    profile = models.ImageField(null=True, blank=True ,upload_to='profile')
    resume = models.FileField(null=True, upload_to='resume')

    permanent_address=models.CharField(max_length=200 , null=True)
    permanent_city=models.CharField(max_length=200 , null=True)
    permanent_state=models.CharField(max_length=200 , null=True)
    permanent_pincode=models.CharField(max_length=200 , null=True)

    temp_address=models.CharField(max_length=200 , null=True)
    temp_city=models.CharField(max_length=200 , null=True)
    temp_state=models.CharField(max_length=200 , null=True)
    temp_pincode=models.CharField(max_length=200 , null=True)

    mobile1 = models.CharField(max_length=200 , null=True)
    mobile2 = models.CharField(max_length=200 , null=True)
    landline = models.CharField(max_length=200 , null=True)
    email1 = models.CharField(max_length=200 , null=True) 
    email2 = models.CharField(max_length=200 , null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.first_name
    

class Company(models.Model):
    CATEGORY =(
        ("Owner" ,"Owner"),
        ("Managers" ,"Managers")
    )
    company_name= models.CharField(max_length=200, null=True, unique=True)
    contact_person= models.CharField(max_length=200, null=True)
    address= models.CharField(max_length=200, null=True)
    phone= models.CharField(max_length=200, null=True)
    email= models.CharField(max_length=200, null=True)
    management= models.CharField(max_length=200, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.company_name
    

class Vessel(models.Model):
    vessel_name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    
    def __str__(self):
        return self.vessel_name
    

class Experience(models.Model):
    experience = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    
    def __str__(self):
        return self.experience

class Rank(models.Model):
    RANK=(
        ("Officer","Officer" ),
        ("Rating","Rating" ),
        ("IV Crew","IV Crew" )
    )
    #user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    rank_name= models.CharField(max_length=200, null=True)       
    rank_order= models.CharField(max_length=200, null=True)
    rank_category = models.CharField(max_length=200, choices=RANK)
    date_created = models.DateTimeField(auto_now_add=True , null=True)   

    def __str__(self):
        return self.rank_name
    
class Grade(models.Model):
    grade_name =models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.grade_name
    
class Port(models.Model):
    port_name= models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.port_name
    

class PortAgent(models.Model):
    port_agent = models.CharField(max_length=200 ,null=True)
    port_contact_person = models.CharField(max_length=200 , null=True)
    port_agent_address= models.CharField(max_length=200, null=True)
    port_agent_phone =models.CharField(max_length=200, null=True)
    port_agent_email = models.CharField(max_length=200, null=True)
    port_agent_city = models.CharField(max_length=200, null=True)
    port_agent_state = models.CharField(max_length=200, null=True)
    port_agent_country = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.port_agent    
    
class Hospital(models.Model):
    hospital_name = models.CharField(max_length=200, null=True)
    doctor_name = models.CharField(max_length=200, null=True)
    hospital_address = models.CharField(max_length=200, null=True)
    hospital_city = models.CharField(max_length=200, null=True)
    hospital_state = models.CharField(max_length=200, null=True)
    hospital_phone = models.CharField(max_length=200, null=True)
    hospital_email = models.CharField(max_length=200, null=True)
    hospital_image = models.ImageField(null=True ,blank=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.hospital_name 

class DocumentType(models.Model):
    EXPIRY_DATE =(
        ('Yes','Yes'),
        ('No','No')
    )
    document_type = models.CharField(max_length=200, null=True)
    hide_expiry_date = models.CharField(max_length=200, choices=EXPIRY_DATE)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.document_type 
    

class Vendors(models.Model):
    vendor_name = models.CharField(max_length=200, null=True)
    vendor_address = models.CharField(max_length=200, null=True)  
    date_created = models.DateTimeField(auto_now_add=True , null=True) 

    def __str__(self):
        return self.vendor_name 



class VslType(models.Model):
    vsl_name = models.CharField(max_length=200, null=True)
    vsl_type = models.CharField(max_length=200, null=True)  
    vsl_company = models.CharField(max_length=200, null=True)
    IMO_Number  = models.CharField(max_length=200, null=True)
    vsl_flag = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)


    def __str__(self):
        return self.vsl_name   



class OfficeDocument(models.Model):
    document_name = models.CharField( max_length=200, null=True)
    document_file = models.FileField( null=True, upload_to='officedoc')
    date_created = models.DateTimeField(auto_now_add=True , null=True) 

    def __str__(self):
        return self.document_name      
 
class CountryName(models.Model):
    country_name = models.CharField( max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

# files handling modles
class ExcelFiles(models.Model):
    file = models.FileField(upload_to='import_files')  
   
    
    
        
        
      

