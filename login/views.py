from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Count
from django.utils import timezone
from .models import User,Citizen,Panchayat,Asset,Cultivationrecord, Vaccinationrecord, Welfareprogram, Land, Household,Servicerequest
from datetime import datetime

text = {
    "admin":"You can modify or add the data to the biggest and the important database, We are hoping you the best experience",
    "citizen": "You can watch the data of your panchayat virtually from the home, We are hoping you the best experience",
    "government": "You can get all your data within seconds, We are hoping you the best experience",
    "employee":"You can mofidy or add data of your panchayat, We are hoping you the best experience"
}

data = "null"
# Create your views here.

def index(request):
    return render(request, "login/layout.html")

def display_page(request):
    if(request.method == 'POST'):
        data = request.POST["userType"]
        
    return render(request, "login/display.html",{
        "person":data,
        "text":text[data]
    })

def auth(request,data):
    if(request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]

        user = User.objects.get(username=username)


        if(user.password == password and user.role == data):
            
            if(data == "citizen"):
                citizen = user.citizenid
                print(citizen.fullname)
                panchayat = citizen.panchayatid
                assets = Asset.objects.filter(panchayatid=panchayat)
                citizens_in_panchayat = Citizen.objects.filter(panchayatid=panchayat)
                cultivation = Cultivationrecord.objects.filter(panchayatid=panchayat).values('year', 'season', 'croptype').annotate(total_cultivated_area=Sum('cultivatedarea')).order_by('year', 'season', 'croptype')    
                vaccinationrecords = Vaccinationrecord.objects.filter(panchayatid=panchayat)
                welfareschemes = Welfareprogram.objects.all()
            
                return render(request, "login/citizens.html",{
                    "citizen":citizen,
                    "panchayat":panchayat,
                    "assets":assets,
                    "citizens_in_panchayat":citizens_in_panchayat,
                    "cultivation":cultivation,
                    "vaccinationrecords":vaccinationrecords,
                    "welfareschemes":welfareschemes
                })
            
            elif(data == "employee"):
                citizen = user.citizenid
                print(citizen.fullname)
                panchayat = citizen.panchayatid
                assets = Asset.objects.filter(panchayatid=panchayat)
                citizens_in_panchayat = Citizen.objects.filter(panchayatid=panchayat)
                cultivation = Cultivationrecord.objects.filter(panchayatid=panchayat).values('year', 'season', 'croptype').annotate(total_cultivated_area=Sum('cultivatedarea')).order_by('year', 'season', 'croptype')    
                vaccinationrecords = Vaccinationrecord.objects.filter(panchayatid=panchayat)
                welfareschemes = Welfareprogram.objects.all()
                service_request = Servicerequest.objects.all()

                return render(request, "login/employees.html",{
                    "citizen":citizen,
                    "panchayat":panchayat,
                    "assets":assets,
                    "citizens_in_panchayat":citizens_in_panchayat,
                    "cultivation":cultivation,
                    "vaccinationrecords":vaccinationrecords,
                    "welfareschemes":welfareschemes,
                    "service_request":service_request,
                })
        
            elif(data == "admin"):
                return redirect('/admin/')
            
            elif(data == "government"):
                citizens = Citizen.objects.all()
                panchayats = Panchayat.objects.all()
                assets = Asset.objects.all()
                cultivation = Cultivationrecord.objects.all()    
                vaccinationrecords = Vaccinationrecord.objects.all()
                welfareschemes = Welfareprogram.objects.all()
                service_request = Servicerequest.objects.all()

                return render(request, "login/government.html",{
                    "citizens":citizens,
                    "panchayats":panchayats,
                    "assets":assets,
                    "cultivation":cultivation,
                    "vaccinationrecords":vaccinationrecords,
                    "welfareschemes":welfareschemes,
                    "service_request":service_request,
                })

        else:
            print("Unsucsessful Login")

def service_request(request):
    """
    Handle service request form submission and save data to Servicerequest model
    """
    if request.method == 'POST':
        try:
            # Get form data
            request_type = request.POST.get('request_type')
            citizen_id = request.POST.get('citizenid')
            
            # Validate citizen exists
            try:
                citizen = Citizen.objects.get(citizenid=citizen_id)
            except Citizen.DoesNotExist:
                messages.error(request, "Invalid citizen ID")
                return redirect('login:citizen_dashboard')
            
            # Create new service request
            service_request = Servicerequest(
                requesttype=request_type,
                requestdate=timezone.now().date(),
                status='Pending',  # Initial status
                citizenid=citizen  # ForeignKey relation
            )
            
            # Save to database
            service_request.save()
            
            # Store additional data in a related model if needed
            # For example, you could store the subject, description, etc. in another model
            
            messages.success(request, "Service request submitted successfully! Request ID: {}".format(service_request.requestid))
            return redirect('login:citizen_dashboard', citizen_id)
            
        except Exception as e:
            messages.error(request, f"Error submitting service request: {str(e)}")
            return redirect('login:citizen_dashboard', citizen_id)
    
    # If not POST method, redirect to dashboard
    return redirect('login:citizen_dashboard', citizen)

@login_required
def gov_citizens(request):
    citizens = Citizen.objects.all()

    return render(request, "login/government_citizens.html", {
        "citizens":citizens
    })

@login_required
def gov_assets(request):
    assets = Asset.objects.all()

    return render(request, "login/government_assets.html", {
        "assets":assets,
    })


@login_required
def update_assets(request):
    """
    Function to handle asset data updates from the employee dashboard
    """
    if request.method == 'POST':
        try:
            # Extract form data
            asset_type = request.POST.get('asset_type')
            asset_location = request.POST.get('asset_location')
            asset_condition = request.POST.get('asset_condition')
            asset_maintenance_date = request.POST.get('asset_maintenance')
            asset_installation_date = request.POST.get('asset_installation')
            
            # Get current panchayat from user session or context
            panchayat_id = request.session.get('panchayat_id')
            panchayat = Panchayat.objects.get(pk=1)
            
            # Create new asset record
            new_asset = Asset(
                assettype=asset_type,
                location=asset_location,
                condition=asset_condition,
                lastmaintenancedate=asset_maintenance_date,
                installationdate=asset_installation_date,
                panchayatid=panchayat
            )
            new_asset.save()
            
            messages.success(request, 'Asset information updated successfully')
            return redirect('login:employee_dashboard')
        
        except Exception as e:
            messages.error(request, f'Error updating asset information: {str(e)}')
            return redirect('login:employee_dashboard')
    
    # If GET request, redirect to dashboard
    return redirect('login:employee_dashboard')

@login_required
def employee_dashboard(request):
    """
    View function for the employee dashboard
    Displays forms for managing panchayat data
    """
    # Get panchayat ID from session or user profile
    panchayat_id = request.session.get('panchayat_id')
    
    # Get panchayat data
    panchayat = Panchayat.objects.get(pk=1)
    
    # Get data for dropdowns and lookups if needed
    assets = Asset.objects.filter(panchayatid=panchayat_id)
    citizens = Citizen.objects.filter(panchayatid=panchayat_id)
    cultivation_records = Cultivationrecord.objects.filter(panchayatid=panchayat_id)
    welfare_programs = Welfareprogram.objects.all()
    vaccination_records = Vaccinationrecord.objects.filter(panchayatid=panchayat_id)
    service_request = Servicerequest.objects.all()
    
    context = {
        'panchayat': panchayat,
        'assets': assets,
        'citizens': citizens,
        'cultivation_records': cultivation_records,
        'welfare_programs': welfare_programs,
        'vaccination_records': vaccination_records,
        "service_request":service_request,

    }
    
    return render(request, 'login/employees.html', context)

@login_required
def citizen_dashboard(request, citizen):
    # Get the citizen object from the string ID
    try:
        citizen = Citizen.objects.get(pk=citizen)
    except Citizen.DoesNotExist:
        # Handle the case where citizen doesn't exist
        messages.error(request, "Citizen not found.")
        return redirect('home')  # or wherever appropriate
        
    # Rest of function remains same
    panchayat = citizen.panchayatid
    assets = Asset.objects.filter(panchayatid=panchayat)
    citizens_in_panchayat = Citizen.objects.filter(panchayatid=panchayat)
    cultivation = Cultivationrecord.objects.filter(panchayatid=panchayat).values('year', 'season', 'croptype').annotate(total_cultivated_area=Sum('cultivatedarea')).order_by('year', 'season', 'croptype')
    vaccinationrecords = Vaccinationrecord.objects.filter(panchayatid=panchayat)
    welfareschemes = Welfareprogram.objects.all()
    
    return render(request, "login/citizens.html",{
        "citizen": citizen,
        "panchayat": panchayat,
        "assets": assets,
        "citizens_in_panchayat": citizens_in_panchayat,
        "cultivation": cultivation,
        "vaccinationrecords": vaccinationrecords,
        "welfareschemes": welfareschemes
    })


@login_required
def update_citizens(request):
    """
    Function to handle citizen data updates from the employee dashboard
    """
    if request.method == 'POST':
        try:
            # Extract form data
            citizen_id = request.POST.get('citizen_id')
            citizen_name = request.POST.get('citizen_name')
            citizen_dob = request.POST.get('citizen_dob')
            citizen_gender = request.POST.get('citizen_gender')
            household_id = request.POST.get('citizen_household')
            education_level = request.POST.get('citizen_education')
            
            # Get current panchayat from user session or context
            panchayat_id = request.session.get('panchayat_id')
            panchayat = Panchayat.objects.get(panchayatid=1)
            
            # Get household
            household = Household.objects.get(householdid=household_id)
            
            if citizen_id:  # Update existing citizen
                citizen = Citizen.objects.get(citizenid=citizen_id)
                citizen.fullname = citizen_name
                citizen.dateofbirth = citizen_dob
                citizen.gender = citizen_gender
                citizen.householdid = household
                citizen.educationlevel = education_level
                citizen.panchayatid = panchayat
                citizen.save()
                messages.success(request, 'Citizen information updated successfully')
            else:  # Create new citizen
                new_citizen = Citizen(
                    fullname=citizen_name,
                    dateofbirth=citizen_dob,
                    gender=citizen_gender,
                    householdid=household,
                    educationlevel=education_level,
                    panchayatid=panchayat
                )
                new_citizen.save()
                messages.success(request, 'New citizen added successfully')
            
            return redirect('login:employee_dashboard')
        
        except Exception as e:
            messages.error(request, f'Error updating citizen information: {str(e)}')
            return redirect('login:employee_dashboard')
    
    # If GET request, redirect to dashboard
    return redirect('login:employee_dashboard')

@login_required
def update_cultivation(request):
    """
    Function to handle cultivation data updates from the employee dashboard
    """
    if request.method == 'POST':
        try:
            # Extract form data
            cultivation_year = request.POST.get('cultivation_year')
            cultivation_crop = request.POST.get('cultivation_crop')
            cultivation_season = request.POST.get('cultivation_season')
            cultivation_area = request.POST.get('cultivation_area')
            
            # Get current panchayat from user session or context
            panchayat_id = request.session.get('panchayat_id')
            panchayat = Panchayat.objects.get(panchayatid=1)
            
            # Create new cultivation record
            new_record = Cultivationrecord(
                year=cultivation_year,
                croptype=cultivation_crop,
                season=cultivation_season,
                cultivatedarea=cultivation_area,
                panchayatid=panchayat
            )
            new_record.save()
            
            messages.success(request, 'Cultivation record added successfully')
            return redirect('login:employee_dashboard')
        
        except Exception as e:
            messages.error(request, f'Error updating cultivation information: {str(e)}')
            return redirect('login:employee_dashboard')
    
    # If GET request, redirect to dashboard
    return redirect('login:employee_dashboard')

@login_required
def update_welfare(request):
    """
    Function to handle welfare program updates from the employee dashboard
    """
    if request.method == 'POST':
        try:
            # Extract form data
            program_id = request.POST.get('program_id')
            program_name = request.POST.get('program_name')
            program_description = request.POST.get('program_description')
            program_eligibility = request.POST.get('program_eligibility')
            program_benefits = request.POST.get('program_benefits')
            program_start = request.POST.get('program_start')
            program_expiry = request.POST.get('program_expiry')
            program_department = request.POST.get('program_department')
            
            if program_id:  # Update existing program
                program = Welfareprogram.objects.get(programid=program_id)
                program.programname = program_name
                program.description = program_description
                program.eligibilitycriteria = program_eligibility
                program.benefits = program_benefits
                program.startdate = program_start
                program.expirydate = program_expiry
                program.managingdepartment = program_department
                program.save()
                messages.success(request, 'Welfare program updated successfully')
            else:  # Create new program
                new_program = Welfareprogram(
                    programname=program_name,
                    description=program_description,
                    eligibilitycriteria=program_eligibility,
                    benefits=program_benefits,
                    startdate=program_start,
                    expirydate=program_expiry,
                    managingdepartment=program_department
                )
                new_program.save()
                messages.success(request, 'New welfare program added successfully')
            
            return redirect('login:employee_dashboard')
        
        except Exception as e:
            messages.error(request, f'Error updating welfare program: {str(e)}')
            return redirect('login:employee_dashboard')
    
    # If GET request, redirect to dashboard
    return redirect('login:employee_dashboard')

@login_required
def update_vaccination(request):
    """
    Function to handle vaccination record updates from the employee dashboard
    """
    if request.method == 'POST':
        try:
            # Extract form data
            citizen_id = request.POST.get('vaccination_citizen')
            vaccine_name = request.POST.get('vaccination_name')
            vaccination_date = request.POST.get('vaccination_date')
            
            # These fields aren't in the model but they're in the form
            # You might want to extend the model to include them
            # dose_number = request.POST.get('vaccination_dose')
            # health_worker = request.POST.get('vaccination_worker')
            # location = request.POST.get('vaccination_location')
            
            # Get current panchayat from user session or context
            panchayat_id = request.session.get('panchayat_id')
            panchayat = Panchayat.objects.get(panchayatid=1)
            
            # Get citizen
            citizen = Citizen.objects.get(citizenid=citizen_id)
            
            # Create new vaccination record
            new_vaccination = Vaccinationrecord(
                vaccinename=vaccine_name,
                dateadministered=vaccination_date,
                citizenid=citizen,
                panchayatid=panchayat
            )
            new_vaccination.save()
            
            messages.success(request, 'Vaccination record added successfully')
            return redirect('login:employee_dashboard')
        
        except Exception as e:
            messages.error(request, f'Error updating vaccination record: {str(e)}')
            return redirect('login:employee_dashboard')
    
    # If GET request, redirect to dashboard
    return redirect('login:employee_dashboard')

def update_service_request(request):
    if request.method == 'POST':
        # Get request parameters
        request_id = request.POST.get('request_id')
        status = request.POST.get('request_status')
        notes = request.POST.get('request_notes', '')
        
        try:
            # Retrieve the service request object
            service_request = Servicerequest.objects.get(requestid=request_id)
            
            # Update the status
            service_request.status = status
            
            # Save the changes
            service_request.save()
            
            # Optional: Log the update with notes
            # You could create a ServiceRequestLog model to track changes
            # ServiceRequestLog.objects.create(
            #     requestid=service_request,
            #     status_change=status,
            #     notes=notes,
            #     updated_by=request.user,
            #     update_date=timezone.now()
            # )
            
            messages.success(request, f'Service Request #{request_id} has been updated successfully.')
            
        except Servicerequest.DoesNotExist:
            messages.error(request, f'Service Request #{request_id} does not exist.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    # Redirect back to the service requests page
    return redirect('login:employee_dashboard')

