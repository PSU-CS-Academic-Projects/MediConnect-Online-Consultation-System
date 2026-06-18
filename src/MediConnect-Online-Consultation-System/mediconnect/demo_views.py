import random
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth import get_user_model
from accounts.models import DoctorProfile, PatientProfile
from django.conf import settings
from django.contrib.auth import authenticate, login

User = get_user_model()

def setup_demo_view(request):
    if not settings.DEBUG:
        return HttpResponseForbidden("This feature is only available in debug mode.")

    try:
        from faker import Faker
    except ImportError:
        return HttpResponse(
            "<h3>Faker is not installed.</h3>"
            "<p>Please install it by running <code>pip install faker</code> in your terminal.</p>"
        )

    fake = Faker()
    
    generated_accounts = {
        'doctors': [],
        'patients': [],
        'admins': []
    }

    # Generate or get 1 Demo Patient
    patient_username = "demo_patient"
    patient_password = "demo_password_123"
    
    patient_user, created = User.objects.get_or_create(
        username=patient_username,
        defaults={
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'role': 'patient'
        }
    )
    
    if created:
        patient_user.set_password(patient_password)
        patient_user.save()
        PatientProfile.objects.filter(user=patient_user).update(
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
            gender=random.choice(['male', 'female']),
            blood_type=random.choice(['A+', 'O+', 'B+', 'AB+', 'O-']),
            allergies="None",
            medical_history="No significant history."
        )
        
    generated_accounts['patients'].append({
        'username': patient_username,
        'password': patient_password,
        'name': patient_user.get_full_name()
    })

    # Generate or get 2 Demo Doctors (One online, one offline/busy)
    specialties = ['general', 'cardiology', 'dermatology', 'neurology']
    statuses = ['online', 'busy']
    
    for i in range(2):
        doctor_username = f"demo_doctor_{i+1}"
        doctor_password = "demo_password_123"
        
        doctor_user, created = User.objects.get_or_create(
            username=doctor_username,
            defaults={
                'email': fake.email(),
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'role': 'doctor'
            }
        )
        
        if created:
            doctor_user.set_password(doctor_password)
            doctor_user.save()
            DoctorProfile.objects.filter(user=doctor_user).update(
                specialty=random.choice(specialties),
                license_number=f"MD-{random.randint(100000, 999999)}",
                bio=fake.paragraph(nb_sentences=3),
                years_of_experience=random.randint(3, 25),
                availability_status=statuses[i],
                is_verified=True,  # Automatically verified for demo
                rating=round(random.uniform(4.0, 5.0), 1)
            )
            
        generated_accounts['doctors'].append({
            'username': doctor_username,
            'password': doctor_password,
            'name': f"Dr. {doctor_user.get_full_name()}",
            'specialty': doctor_user.doctorprofile.get_specialty_display(),
            'status': doctor_user.doctorprofile.get_availability_status_display()
        })

    # Generate or get 1 Demo Admin
    admin_username = "demo_admin"
    admin_password = "demo_password_123"
    
    admin_user, created = User.objects.get_or_create(
        username=admin_username,
        defaults={
            'email': fake.email(),
            'first_name': 'Admin',
            'last_name': 'Demo',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin_user.set_password(admin_password)
        admin_user.save()
        
    generated_accounts['admins'].append({
        'username': admin_username,
        'password': admin_password,
        'name': admin_user.get_full_name()
    })

    return render(request, 'demo_accounts.html', {'accounts': generated_accounts})

def login_demo_view(request, username):
    if not settings.DEBUG:
        return HttpResponseForbidden("This feature is only available in debug mode.")
    
    user = authenticate(request, username=username, password="demo_password_123")
    if user is not None:
        login(request, user)
        return redirect('/dashboard/home/')
    else:
        return HttpResponse("Failed to authenticate demo user.")
