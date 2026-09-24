from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
import re,random
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from datetime import *
from django.utils import timezone
from django.core.validators import RegexValidator

def home(request):
    return render(request,'home.html')

@login_required
def admin_dashboard(request):
    user = request.user
    if user.is_superuser:   
        return render(request,'admin/Admin_dashboard.html')
    else:
        return HttpResponse('You have no access!!')

@login_required
def agent_dashboard(request):
    user = request.user
    if user.is_superuser:
        return HttpResponse('You have no access!!')
    else:
        return render(request,'Agent/agent_dashboard.html')

def login_page(request):
    return render(request,'login_page.html')

def login_fun(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pword")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)

            if user.is_superuser:
                return redirect('admin_dashboard')
            
            else:
                return redirect('agent_dashboard')
            
        else:
            messages.error(request,'Invalid Username or Password!!')
            return redirect('login_page')
        
    return render(request,'login_page.html')


def logout_view(request):
    logout(request)
    return redirect('login_page')

@login_required
def add_Agent(request):
    user = request.user
    if user.is_superuser:   

        special = User.SPECIALISATION_CHOICES

        return render(request,'admin/add_agent.html',{'specialisation':special})
    return HttpResponse("You have no access!!")

@login_required
def add_agent_fun(request):
    user = request.user
    if user.is_superuser:
        special = User.SPECIALISATION_CHOICES

        if request.method=='POST':
            fname = request.POST.get('firstname')
            lname = request.POST.get('lastname')
            address = request.POST.get('address')
            contact = request.POST.get('contact')
            email = request.POST.get('email')
            uname = request.POST.get('username')
            dob = request.POST.get('dob')
            specialisation = request.POST.get('specialisation')
            profile_img = request.FILES.get('profile')

            if User.objects.filter(contact=contact).exists():
                messages.error(request,'Contact Number already exists')
                return redirect('add_Agent')
        
            if len(contact) != 10:
                messages.error(request,'Contact Number must be exactly 10 digits')
                return redirect('add_Agent')
        
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$'
            if not re.match(email_pattern,email):
                messages.error(request,"Enter email in a valid format")
                return redirect('add_Agent')

            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
                return redirect('add_Agent')
        
            if User.objects.filter(username=uname).exists():
                messages.error(request,'Username already exists')
                return redirect('add_Agent')
        
            date_of_birth = datetime.strptime(dob, "%Y-%m-%d").date()

            user = User.objects.create_user(
                username = uname,
                email = email,
                first_name = fname,
                last_name = lname,

                Address = address,
                contact = contact,
                dob = date_of_birth,
                specialisation = specialisation,
                profile_image = profile_img,
                is_staff = "1"            
            )


            print(user)

            password = str(random.randint(100000,999999))
            user.set_password(password)
            user.save()

            print(user)
            subject = "Account Created"
            message = (
            f" Hello {user.first_name} \n\n"
            f" You has been registered Successfully!!\n\n"
            f' Your Username : {user.username} \n'
            f' Your password : {password}\n\n'
            f" You can change your password after Login. Have a nice Day!! "

           )   

            send_mail(subject,message,settings.EMAIL_HOST_USER,[user.email],fail_silently=False)

            messages.success(request,"Client registered Successfully!!")
            return redirect('add_Agent')
    
        return render(request,'admin/add_agent.html',{'specialisation':special})
    return HttpResponse("You have no access!!")

def check_username(request):
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    print(exists)
    return JsonResponse({'exists':exists})

def check_mail(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists':exists})

def check_contact(request):
    contact = request.GET.get('contact')
    print(contact)
    exists = User.objects.filter(contact=contact).exists()
    print(exists)
    return JsonResponse({"exists":exists})

@login_required
def view_agents(request):
    user =request.user
    if user.is_superuser:
        agents = User.objects.filter(is_superuser=False)
        return render(request,'admin/view_clients.html',{'agents':agents})
    else:
        return HttpResponse("You have no access!!")

@login_required
def view_agent_profile(request,id):
    user =request.user
    if user.is_superuser:
        agent = User.objects.get(id=id)
        return render(request,'admin/view_agent_profile.html',{"agent":agent})
    else:
        return HttpResponse("You have no access!!")

@login_required
def edit_agent_profile(request,id):
    user =request.user
    if user.is_superuser:
        agent = User.objects.get(id=id)

        special = User.SPECIALISATION_CHOICES

        user = request.user

        if request.method == "POST":
            fname = request.POST.get('firstname')
            lname = request.POST.get('lastname')
            address = request.POST.get('address')
            contact = request.POST.get('contact')
            email = request.POST.get('email')
            uname = request.POST.get('username')
            dob = request.POST.get('dob')
            specialisation = request.POST.get('specialisation')
            profile_img = request.FILES.get('profile')

            if User.objects.filter(contact=contact).exclude(id=agent.id).exists():
                messages.error(request,'Contact Number already exists')
                return redirect('edit_agent_profile',id=id)
        
            if not contact.isdigit() or len(contact) != 10:
                messages.error(request,'Contact Number must be exactly 10 digits')
                return redirect('edit_agent_profile',id=id)
        
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$'
            if not re.match(email_pattern,email):
                messages.error(request,"Enter email in a valid format")
                return redirect('edit_agent_profile',id=id)

            if User.objects.filter(email=email).exclude(id=agent.id).exists():
                messages.error(request,'Email already exists')
                return redirect('edit_agent_profile',id=id)
        
            if User.objects.filter(username=uname).exclude(id=agent.id).exists():
                messages.error(request,'Username already exists')
                return redirect('edit_agent_profile',id=id)
        
            agent.first_name = fname
            agent.last_name = lname
            agent.Address = address
            agent.contact = contact
            agent.email = email
            agent.username = uname
            agent.specialisation = specialisation
        
            if profile_img:
                agent.profile_image = profile_img

            agent.save()

            messages.success(request,'Profile updated successfully!!')
            return redirect('view_agent_profile',id=id)

        return render(request,'admin/edit_agent_profile.html',{"agent":agent,"specialisation":special})
    return HttpResponse("You have no access!!")

@login_required
def delete_agent(request,id):
    user=request.user
    if user.is_superuser:
        user = User.objects.get(id=id)
        user.delete()
        messages.success(request,'Agent deleted successfully!!')
        return redirect('view_agents')
    return HttpResponse("You have no access!!")

@login_required
def add_campaign(request):
    user = request.user
    if user.is_superuser:
        agents = User.objects.filter(is_superuser=False)

        if request.method == 'POST':
            title = request.POST.get('title')
            location = request.POST.get('location')
            assign_agent_id = request.POST.get('agent')
            poster = request.FILES.get('poster')
            ag_date = request.POST.get('camp_date')
            time = request.POST.get('camp_time')
            latitude = request.POST.get('lat')
            longitude = request.POST.get('long')

            add_date = datetime.strptime(ag_date, "%Y-%m-%d").date()

            today = timezone.now().date()

            agent = User.objects.get(id=assign_agent_id)

            if add_date < today:
                messages.error(request,"Select a Different date")
                return redirect('add_campaign')

            campaign = Campaign.objects.create(
                title = title,
                location = location,
                assign_agents = agent,
                poster = poster,
                date = add_date,
                time = time,
                latitude = latitude,
                longitude = longitude
            )
        
            campaign.save()
        
            messages.success(request,'Added Successfully!!')
            return redirect("add_campaign")

        return render(request,'admin/add_campaign.html',{"agents":agents})
    return HttpResponse("You have no access!!")

@login_required
def view_campaign(request):
    user = request.user
    if user.is_superuser:
        campaign = Campaign.objects.all()
        return render(request,'admin/view_campaign.html',{"campaign":campaign})
    return HttpResponse("You have no access!!")

@login_required
def edit_campaign(request,id):
    user = request.user
    if user.is_superuser:
        agents = User.objects.filter(is_superuser=False)

        campaign = Campaign.objects.get(id=id)

        if request.method == 'POST':
            title = request.POST.get('title')
            location = request.POST.get('location')
            latitude = request.POST.get('lat')
            longitude = request.POST.get('long')
            assign_agent_id = request.POST.get('agent')
            poster = request.FILES.get('poster')
            ag_date = request.POST.get('camp_date')
            time = request.POST.get('camp_time')

            add_date = datetime.strptime(ag_date, "%Y-%m-%d").date()

            agent = User.objects.get(id=assign_agent_id)


            campaign.title = title
            campaign.location = location
            campaign.latitude = latitude
            campaign.longitude = longitude
            campaign.assign_agents = agent
            campaign.date = add_date
            campaign.time = time

            if poster:
                campaign.poster = poster


            campaign.save()

            messages.success(request,"Updated Successfully!!")
            return redirect('view_campaign')

        return render(request,"admin/edit_campaign.html",{"campaign":campaign,"agent":agents})
    return HttpResponse('You have no access!!')

@login_required
def delete_campaign(request,id):
    user = request.user
    if user.is_superuser:
        campaign = Campaign.objects.get(id=id)
        campaign.delete()

        return redirect('view_campaign')
    return HttpResponse('You have no access!!')
 
@login_required
def view_my_campaigns(request):
    user = request.user
    if user.is_superuser:
        return HttpResponse('You have no access!!')   
    else:
        campaign = Campaign.objects.filter(assign_agents = user.id)
        return render(request,'Agent/view_my_campaigns.html',{"campaign":campaign})


@login_required
def add_client(request):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no access!!")
    else:
        qualification = Client.QUALIFICATION_CHOICES
        return render(request,'Agent/add_client.html',{'qualification':qualification})


@login_required
def add_client_fun(request):
    user=request.user
    if user.is_superuser:
        return HttpResponse("You have no access!!")
    else:
        if request.method == 'POST':
            fname = request.POST.get('fullname')
            address = request.POST.get('address')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            aadhar = request.POST.get('aadhar')
            pan = request.POST.get('pan')
            occ = request.POST.get('job')
            salary = request.POST.get('salary')
            qualification = request.POST.get('qualification')
            status = request.POST.get('status')
            interest = request.POST.get('interest')
            agent_feedback = request.POST.get('feedback_agent')
            feedback = request.POST.get('feedback')

            if Client.objects.filter(contact=contact).exists():
                messages.error(request,'Contact Number already exists')
                return redirect('add_client')
        
            if not contact.isdigit() or len(contact) != 10:
                messages.error(request,'Contact Number must be exactly 10 digits')
                return redirect('add_client')
        
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$'
            if not re.match(email_pattern,email):
                messages.error(request,"Enter email in a valid format")
                return redirect('add_client')

            if Client.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
                return redirect('add_client')
        
            if not aadhar.isdigit() or len(aadhar) != 12:
                messages.error(request,'Aadhaar must contain only 12 digits')
                return redirect('add_client')

            if not len(pan) == 10 :
                messages.error(request,"Pan Should contain only 10 charcters")
                return redirect("add_client")
        
            client = Client.objects.create(
            full_name = fname,
            address = address,
            email = email,
            contact = contact,
            aadhar = aadhar,
            pan = pan,
            job = occ,
            salary = salary,
            qualification = qualification,
            status = status,
            interest = interest,
            agent_feedback =agent_feedback,
            feedback = feedback,
            agent = request.user
            )

            client.save()
            return redirect('view_clients')
        return render(request,'Agent/add_client.html')


def check_aadhar(request):
    aadhar = request.GET.get("aadhar")
    exists = Client.objects.filter(aadhar=aadhar).exists()
    print(exists)
    return JsonResponse({'exists':exists})

def check_client_email(request):
    print("REQUEST:", request.GET)

    email = request.GET.get('email')
    exists = Client.objects.filter(email=email).exists()
    print("EXISTS:", exists)

    return JsonResponse({'exists':exists})


def check_client_contact(request):
    contact = request.GET.get('contact')
    print(contact)
    exists = Client.objects.filter(contact=contact).exists()
    print(exists)
    return JsonResponse({"exists":exists})

def check_pan(request):
    pan = request.GET.get('pan')
    exists = Client.objects.filter(pan=pan).exists()
    print(exists)
    return JsonResponse({"exists":exists}) 

@login_required
def reset_pass(request):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no access!!")
    else:
        return render(request,'Agent/reset_password.html')

@login_required
def reset_pass_fun(request):
    user =request.user
    if user.is_superuser:
        return HttpResponse("You have no access!!")
    else:
        if request.method == 'POST':
            current_password = request.POST.get('cpass')
            new_password = request.POST.get('npass')
            confirm_password = request.POST.get('copass')
        
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'

            if current_password == '':
                messages.error(request,'Password cannot be empty')
                return redirect('reset_pass')        

            if not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('reset_pass')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('reset_pass')
        
            if not re.match(regex,new_password):
                messages.error(request,'Password must contain 8+ characters including all characters')
                return redirect('reset_pass')


            user.set_password(new_password)
            user.save()
            messages.success(request,"Password Reset Successful!!")
            return redirect('login_page')

        return render(request,'Agent/reset_password.html')

@login_required
def view_clients(request):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no Access!!")
    else:
        clients = Client.objects.filter(agent=user.id)
    
        return render(request,"Agent/view_clients.html",{"clients":clients})

@login_required
def view_client_profile(request,id):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no Access!!")
    else:
        client = Client.objects.get(id=id)

        return render(request,"Agent/view_client_profile.html",{"client":client})

@login_required
def view_profile(request):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no Access!!")
    else:
        return render(request,'Agent/view_profile.html',{"agent":user})

@login_required
def edit_profile(request,id):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no Access!!")
    else:
        special = User.SPECIALISATION_CHOICES
        if request.method == "POST":
            fname = request.POST.get('firstname')
            lname = request.POST.get('lastname')
            address = request.POST.get('address')
            contact = request.POST.get('contact')
            email = request.POST.get('email')
            uname = request.POST.get('username')
            dob = request.POST.get('dob')
            specialisation = request.POST.get('specialisation')
            profile_img = request.FILES.get('profile')

            if User.objects.filter(contact=contact).exclude(id=user.id).exists():
                messages.error(request,'Contact Number already exists')
                return redirect('edit_profile',id=id)
        
            if not contact.isdigit() or len(contact) != 10:
                messages.error(request,'Contact Number must be exactly 10 digits')
                return redirect('edit_profile',id=id)
        
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$'
            if not re.match(email_pattern,email):
                messages.error(request,"Enter email in a valid format")
                return redirect('edit_profile',id=id)

            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request,'Email already exists')
                return redirect('edit_profile',id=id)
        
            if User.objects.filter(username=uname).exclude(id=user.id).exists():
                messages.error(request,'Username already exists')
                return redirect('edit_profile',id=id)
        

            user.first_name = fname
            user.last_name = lname
            user.Address = address
            user.contact = contact
            user.email = email
            user.username = uname
            user.specialisation = specialisation
        
            if profile_img:
                user.profile_image = profile_img

            user.save()

            messages.success(request,'Profile updated successfully!!')
            return redirect('view_profile')
 
        return render(request,'Agent/edit_profile.html',{"agent":user,"specialisation":special})
    
@login_required
def add_client_camppage(request,id):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no Access!!")
    else:
        qualification = Client.QUALIFICATION_CHOICES
        campaign = Campaign.objects.get(id=id)
        return render(request,'Agent/add_client_campaign.html',{'campaign':campaign,'qualification':qualification})

@login_required
def add_client_campaign(request,id):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no Access!!")
    else:
        qualification_choices = Client.QUALIFICATION_CHOICES
        campaign = Campaign.objects.get(id=id)
        if request.method == 'POST':
            fname = request.POST.get('fullname')
            address = request.POST.get('address')
            email = request.POST.get('email')
            contact = request.POST.get('phone')
            aadhar = request.POST.get('aadhar')
            pan = request.POST.get('pan')
            occ = request.POST.get('job')
            salary = request.POST.get('salary')
            qualification = request.POST.get('qualification')
            status = request.POST.get('status')
            interest = request.POST.get('interest')
            agent_feedback = request.POST.get('feedback_agent')
            feedback = request.POST.get('feedback')

            if Client.objects.filter(contact=contact).exists():
                messages.error(request,'Contact Number already exists')
                return redirect('add_client_campaign',id=id)
        
            if not contact.isdigit() or len(contact) != 10:
                messages.error(request,'Contact Number must be exactly 10 digits')
                return redirect('add_client_campaign',id=id)
        
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$'
            if not re.match(email_pattern,email):
                messages.error(request,"Enter email in a valid format")
                return redirect('add_client_campaign',id=id)

            if Client.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
                return redirect('add_client_campaign',id=id)
        
            if not aadhar.isdigit() or len(aadhar) != 12:
                messages.error(request,'Aadhaar must contain only 12 digits')
                return redirect('add_client_campaign',id=id)

            if not len(pan) == 10 :
                messages.error(request,"Pan Should contain only 10 charcters")
                return redirect("add_client_campaign",id=id)
        
            client = Client.objects.create(
                full_name = fname,
                address = address,
                email = email,
                contact = contact,
                aadhar = aadhar,
                pan = pan,
                job = occ,
                salary = salary,
                qualification = qualification,
                status = status,
                interest = interest, 
                agent_feedback =agent_feedback,
                feedback = feedback,
                agent = request.user,
                campaign = campaign
            )

            client.save()
            messages.success(request,"Client added successfully!")
        return render(request,'Agent/add_client_campaign.html',{'campaign':campaign,'qualification':qualification_choices})

@login_required
def view_clients_campaign(request,id):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no Access!!")
    else:
        campaign = Campaign.objects.get(id=id)

        clients = Client.objects.filter(campaign=campaign,agent = request.user)
    # print(clients)
        return render(request,'Agent/view_client_camp.html',{'clients':clients,"campaign":campaign})

@login_required
def edit_client_profile(request,id):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no Access!!")
    else:
        qualification_choices = Client.QUALIFICATION_CHOICES
        campaign = Campaign.objects.filter(assign_agents=request.user)
        client = Client.objects.get(id=id)
        # campaign = Campaign.objects.all()
        if request.method == 'POST':
            fname = request.POST.get('fullname')
            address = request.POST.get('address')
            email = request.POST.get('email')
            contact = request.POST.get('phone')
            occ = request.POST.get('job')
            salary = request.POST.get('salary')
            aadhar = request.POST.get('aadhar')
            pan = request.POST.get('pan')
            qualification = request.POST.get('qualification')
            status = request.POST.get('status')
            interest = request.POST.get('interest')
            agent_feedback = request.POST.get('feedback_agent')
            feedback = request.POST.get('feedback')
            campaign_id = request.POST.get('campaign')

            if Client.objects.filter(contact=contact).exclude(id=client.id).exists():
                messages.error(request,'Contact Number already exists')
                return redirect('edit_client_profile',id=id)
        
            if not contact.isdigit() or len(contact) != 10:
                messages.error(request,'Contact Number must be exactly 10 digits')
                return redirect('edit_client_profile',id=id)
        
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$'
            if not re.match(email_pattern,email):
                messages.error(request,"Enter email in a valid format")
                return redirect('edit_client_profile',id=id)

            if Client.objects.filter(email=email).exclude(email = client.email).exists():
                messages.error(request,'Email already exists')
                return redirect('edit_client_profile',id=id)
            
            if Client.objects.filter(aadhar=aadhar).exclude(aadhar = client.aadhar).exists():
                messages.error(request,'Aadhar number already exists')
                return redirect('edit_client_profile',id=id)
            
            if not aadhar.isdigit() or len(aadhar) != 12:
                messages.error(request,'Aadhaar Number must be exactly 12 digits')
                return redirect('edit_client_profile',id=id)
            
            if Client.objects.filter(pan=pan).exclude(pan=client.pan).exists():
                messages.error(request,"PAN already exists")
                return redirect("edit_client_profile",id=id)
        
            if campaign_id:
                try:
                    client_campaign = Campaign.objects.get(id=campaign_id)
                    client.campaign = client_campaign
                except(ValueError,Campaign.DoesNotExist):
                    client.campaign = client_campaign
            # else:
            #     client.campaign = None

            user=User.objects.get(id=request.user.id)
            print(user)

            client.full_name = fname
            client.address = address
            client.email = email
            client.contact = contact
            client.job = occ
            client.salary = salary
            client.aadhar = aadhar
            client.pan = pan
            client.qualification = qualification
            client.status = status
            client.interest = interest 
            client.agent_feedback =agent_feedback
            client.feedback = feedback
            client.agent = user


            client.save()
            messages.success(request,"Client updated successfully!")
            return redirect('view_clients')
        return render(request,'Agent/edit_client.html',{'campaign':campaign,'qualification':qualification_choices,"client":client})

@login_required
def delete_client_profile(request,id):
    user = request.user
    if user.is_superuser:
        return HttpResponse("You have no Access!!")
    else:
        client = Client.objects.get(id=id)
        client.delete()
        messages.success(request,"Client deleted successfully!!")
        return redirect('view_clients')

@login_required
def view_camp_clients(request,id):
    user = request.user
    if user.is_superuser:
        campaign = Campaign.objects.get(id=id)

        clients = Client.objects.filter(campaign=id)
        return render(request,'admin/view_camp_clients.html',{'campaign':campaign,'clients':clients})
    else:
        return HttpResponse("You have no Access!!")

@login_required
def view_client_admin_profile(request,id):
    user = request.user
    if user.is_superuser:
        client = Client.objects.get(id=id)

        return render(request,"admin/view_clients_profile.html",{"client":client})
    else:
        return HttpResponse("You have no Access!!")

@login_required
def view_clients_by_admin(request,id):
    user = request.user
    if user.is_superuser:
        clients = Client.objects.filter(agent=id)
        return render(request,'admin/view_camp_clients.html',{'clients':clients})
    else:
        return HttpResponse("You have no Access!!")


