from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from .forms import LoginForm, StdProfileForm,CreateUserForm,MarksForm,SubjectForm,NoticeForm
from .models import StdProfile,Subject,Marks,Notice
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
import logging


def dashboard(request):
    return render(request,'dashboard.html')

logger = logging.getLogger(__name__)

def register(request):
    frm = CreateUserForm()
    if request.method == 'POST':
        frm = CreateUserForm(request.POST)
        if frm.is_valid():
            user = frm.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            try:
                group = Group.objects.get(name='student')
            except Group.DoesNotExist:
                logger.error("Group 'student' does not exist.")
                frm.add_error(None, "Registration failed due to server error. Please try again later.")
                return render(request, 'register.html', {'frm': frm})

            user.groups.add(group)
            login(request, user)
            return redirect('home')  # Redirect to profile creation page
        else:
            logger.info("Form is not valid: %s", frm.errors)
            print(frm.errors)  # For debugging purposes

    return render(request, 'register.html', {'frm': frm})



def login_view(request):

        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                   login(request,user)
                   if user.groups.filter(name='faculty').exists():
                       return redirect ('faculty_home')
                   elif user.groups.filter(name='student').exists():
                       return redirect ('home')
                   elif request.user.is_superuser:
                       return redirect ('admin_home')
                   else:
                       return redirect ("register")
                
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    if request.user.groups.filter(name='student').exists():
        return render(request, 'home.html')
    else:
        return redirect('login')

@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html')

@login_required(login_url='login')
def faculty_home(request):
    if request.user.groups.filter(name='faculty').exists():
        return render(request, 'f_home.html')
    else:
        return redirect('login')

@login_required(login_url='login')
def profile_view(request):
    user_profile, created = StdProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        frmp = StdProfileForm(request.POST, instance=user_profile)
        if frmp.is_valid():
            frmp.save()
            return redirect('home')  # Redirect to the profile page after saving
    else:
        frmp = StdProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'frmp': frmp})

@login_required(login_url='login')
def user_detail_view(request, user_id):#in this the address bar shows the user/userid which is actually rendering
    user = get_object_or_404(User, pk=user_id)#the profilev html document the page have to be reconstructed
    std_profile = get_object_or_404(StdProfile, user=user)
    context = {
        'user': user,
        'StdProfile': std_profile
    }
    return render(request, 'profilev.html', context)

def is_faculty(user):
    return user.is_staff

@user_passes_test(is_faculty)
@login_required(login_url='login')
def add_marks(request):
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_marks')
    else:
        form = MarksForm()
    return render(request, 'mrk_add.html', {'form': form})

@login_required(login_url='login')
def view_marks(request):
    if request.user.is_staff:
        marks = Marks.objects.all()
        
        # Filtering logic for staff
        student_id = request.GET.get('student_id')
        subject_id = request.GET.get('subject_id')
        min_marks = request.GET.get('min_marks')
        max_marks = request.GET.get('max_marks')
        semester = request.GET.get('semester')
        department = request.GET.get('department')

        if student_id:
            marks = marks.filter(student_id=student_id)
        if subject_id:
            marks = marks.filter(subject_id=subject_id)
        if min_marks:
            marks = marks.filter(marks__gte=min_marks)
        if max_marks:
            marks = marks.filter(marks__lte=max_marks)
        if semester:
            marks = marks.filter(student__semester=semester)
        if department:
            marks = marks.filter(student__department=department)
        # Get unique subjects
        unique_subjects = set(marks.values_list('subject', flat=True))
    else:
        student = get_object_or_404(StdProfile, user=request.user)
        marks = Marks.objects.filter(student=student)
        unique_subjects = set(marks.values_list('subject', flat=True))

    return render(request, 'mrk_view.html', {'marks': marks, 'unique_subjects': unique_subjects})


@user_passes_test(is_faculty)
@login_required(login_url='login')
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_subjects')
    else:
        form = SubjectForm()
    return render(request, 'sub_add.html', {'form': form})

@login_required(login_url='login')
def view_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'sub_view.html', {'subjects': subjects})

@login_required(login_url='login')
def notice(request):
    return render(request,'notice')

@login_required
def notice_create(request):
    if not request.user.is_superuser:  # Check if the user is an admin
        return HttpResponseForbidden("You are not allowed to create notices.")
    
    if request.method == 'POST':
        formn = NoticeForm(request.POST)
        if formn.is_valid():
            notice = formn.save(commit=False)
            notice.created_by = request.user
            notice.save()
            return redirect('notice_view')
    else:
        formn = NoticeForm()
    return render(request, 'notice_add.html', {'formn': formn})


@login_required
def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'notice_view.html', {'notices': notices})

@login_required(login_url='login')
def a_home(request):
    return render(request,'a_home.html')

@login_required(login_url='login')
def about(request):
    return render(request,'about.html')