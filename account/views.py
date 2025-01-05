from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from .forms import LoginForm, StdProfileForm,RegistrationForm,MarksForm,SubjectForm,NoticeForm,UniversityMarksForm,AttendanceForm,SyllabusForm,ExamTimetableForm,ClassTimetableForm,MarksFilterForm
from .models import StdProfile,Subject,Marks,Notice,UniversityMarks,Attendance,Syllabus,ExamTimetable,ClassTimetable
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
import logging
from django.contrib import messages
from collections import defaultdict

  

def dashboard(request):
    return render(request,'dashboard.html')

logger = logging.getLogger(__name__)

def register(request):
    frm = RegistrationForm()
    if request.method == 'POST':
        frm = RegistrationForm(request.POST)
        if frm.is_valid():
            user = frm.save(commit=False)
            user.is_active = False  # the user is set to be inactive by default
            user.save()
            user.refresh_from_db()  
            messages.success(request, 'Your account has been created and is awaiting approval.')
            try:
                group = Group.objects.get(name='student')
            except Group.DoesNotExist:
                logger.error("Group 'student' does not exist.")
                frm.add_error(None, "Registration failed due to server error. Please try again later.")
                return render(request, 'register.html', {'frm': frm})

            user.groups.add(group)
            login(request, user)
            #return redirect('login')  # Redirect to profile creation page
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






@login_required
def filter_marks(request):
    if request.user.groups.filter(name='faculty').exists() or request.user.is_superuser:
        marks = None
        departments = StdProfile.objects.values_list('department', flat=True).distinct()
        courses = StdProfile.objects.values_list('course', flat=True).distinct()
        semesters = StdProfile.objects.values_list('semester', flat=True).distinct()
        subjects = Subject.objects.values_list('name', flat=True).distinct()

        department_choices = [(department, department) for department in departments]
        course_choices = [(course, course) for course in courses]
        semester_choices = [(semester, semester) for semester in semesters]
        subject_choices = [(subject, subject) for subject in subjects]


        marks = []
        if request.method == "POST":
            form = MarksFilterForm(request.POST, departments=department_choices, courses=course_choices, semesters=semester_choices, subjects=subject_choices)
            if form.is_valid():
                department = form.cleaned_data['department']
                course = form.cleaned_data['course']
                semester = form.cleaned_data['semester']
                subject = form.cleaned_data['subject']
                students = StdProfile.objects.filter(department=department, course=course, semester=semester)
                marks = Marks.objects.filter(student__in=students).order_by('student__user__username', 'subject__name')
                if subject:
                    marks = marks.filter(subject__name=subject)
                marks = marks.order_by('subject__name', 'student__user__username')
        else:
            form = MarksFilterForm(departments=department_choices, courses=course_choices, semesters=semester_choices, subjects=subject_choices)
        return render(request, 'mrk_view.html', {'form': form, 'marks': marks})
     
    elif request.user.groups.filter(name='student').exists():
        std_profile = StdProfile.objects.get(user=request.user)
        marks = Marks.objects.filter(student=std_profile).order_by('subject__name')
        return render(request, 'mrk_view.html', {'marks': marks})
    else:
        return redirect('dashboard')
    




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

@staff_member_required
def admin_approval(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('approve')
        User.objects.filter(id__in=user_ids).update(is_active=True)
        messages.success(request, 'Selected users have been approved.')
        return redirect('approval')
    
    unapproved_users = User.objects.filter(is_active=False)
    return render(request, 'approval.html', {'unapproved_users': unapproved_users})






def filter_university_marks(request):
    if request.user.groups.filter(name='faculty').exists() or request.user.is_superuser:
        departments = StdProfile.objects.values_list('department', flat=True).distinct()
        courses = StdProfile.objects.values_list('course', flat=True).distinct()
        semesters = StdProfile.objects.values_list('semester', flat=True).distinct()
        subjects = Subject.objects.values_list('name', flat=True).distinct()

        department_choices = [(department, department) for department in departments]
        course_choices = [(course, course) for course in courses]
        semester_choices = [(semester, semester) for semester in semesters]
        subject_choices = [(subject, subject) for subject in subjects]

        marks = []
        if request.method == "POST":
            form = MarksFilterForm(request.POST, departments=department_choices, courses=course_choices, semesters=semester_choices, subjects=subject_choices)
            if form.is_valid():
                department = form.cleaned_data['department']
                course = form.cleaned_data['course']
                semester = form.cleaned_data['semester']
                subject = form.cleaned_data['subject']
                students = StdProfile.objects.filter(department=department, course=course, semester=semester)
                marks = UniversityMarks.objects.filter(student__in=students)
                if subject:
                    marks = marks.filter(subject__name=subject)
                marks = marks.order_by('subject__name', 'student__user__username')
        else:
            form = MarksFilterForm(departments=department_choices, courses=course_choices, semesters=semester_choices, subjects=subject_choices)
        
        return render(request, 'university_mrk.html', {'form': form, 'marks': marks})

    elif request.user.groups.filter(name='student').exists():
        std_profile = StdProfile.objects.get(user=request.user)
        marks = UniversityMarks.objects.filter(student=std_profile).order_by('subject__name')
        return render(request, 'university_mrk.html', {'marks': marks})
    else:
        return redirect('dashboard')










@user_passes_test(is_faculty)
@login_required(login_url='login')
def add_UniversityMarks(request):
    if request.method == 'POST':
        form = UniversityMarksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('university_mrk')
    else:
        form = UniversityMarksForm()
    return render(request, 'add_university_mrk.html', {'form': form})


@login_required(login_url='login')
def attendance(request):
    user = request.user
    if user.is_staff or user.is_superuser:
        # Handle faculty or superuser
        if request.method == "POST":
            form = AttendanceForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('attendance')
        else:
            form = AttendanceForm()
        attendance_records = Attendance.objects.all()
        context = {
            'form': form,
            'attendance_records': attendance_records,
            'role': 'staff',
        }
    else:
        # Handle students and other users
        try:
            student = StdProfile.objects.get(user=user)
            attendance_records = Attendance.objects.filter(student=student)
            context = {
                'attendance_records': attendance_records,
                'role': 'student',
            }
        except StdProfile.DoesNotExist:
            # Handle case where the user does not belong to either group
            context = {
                'message': 'You are not assigned to a valid group.',
            }

    return render(request, 'attendance.html', context)

def add_attendance(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance')
    else:
        form = AttendanceForm()
    return render(request, 'attendance.html', {'form': form})


@login_required
def upload_syllabus(request):
    if request.user.groups.filter(name='faculty').exists():
        if request.method == "POST":
            form = SyllabusForm(request.POST, request.FILES)
            if form.is_valid():
                syllabus = form.save(commit=False)
                syllabus.uploaded_by = request.user
                syllabus.save()
                return redirect('syllabus')
        else:
            form = SyllabusForm()
        return render(request, 'add_syllabus.html', {'form': form})
    else:
        return redirect('syllabus')

@login_required
def view_syllabi(request):
    syllabi = Syllabus.objects.all()
    return render(request, 'syllabus.html', {'syllabi': syllabi})


@login_required
def add_exam_timetable(request):
    if request.user.groups.filter(name='faculty').exists():
        if request.method == "POST":
            form = ExamTimetableForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('examtimetable')
        else:
            form = ExamTimetableForm()
        return render(request, 'add_exam.html', {'form': form})
    else:
        return redirect('examtimetable')

@login_required
def view_exam_timetable(request):
    if request.user.groups.filter(name='student').exists():
        std_profile = StdProfile.objects.get(user=request.user)
        timetables = ExamTimetable.objects.filter(semester=std_profile.semester).order_by('exam_date', 'exam_time')
    else:
        timetables = ExamTimetable.objects.all().order_by('semester', 'exam_date', 'exam_time')
    
    return render(request, 'examtimetable.html', {'timetables': timetables})



@login_required
def add_class_timetable(request):
    if request.user.groups.filter(name='faculty').exists():
        if request.method == "POST":
            form = ClassTimetableForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('classtimetable')
        else:
            form = ClassTimetableForm()
        return render(request, 'add_classtimetable.html', {'form': form})
    else:
        return redirect('classtimetable')




@login_required
def view_class_timetable(request):
    if request.user.groups.filter(name='student').exists():
        std_profile = StdProfile.objects.get(user=request.user)
        timetables = ClassTimetable.objects.filter(semester=std_profile.semester, course=std_profile.course).order_by('day', 'start_time')
    elif request.user.groups.filter(name='faculty').exists() or request.user.is_superuser:
        timetables = ClassTimetable.objects.all().order_by('course', 'semester', 'day', 'start_time')
    else:
        timetables = []
    
    timetable_dict = {}
    for timetable in timetables:
        if timetable.day not in timetable_dict:
            timetable_dict[timetable.day] = []
        timetable_dict[timetable.day].append(timetable)

    return render(request, 'classtimetable.html', {'timetable_dict': timetable_dict})

