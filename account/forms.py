from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import StdProfile,Marks,Subject,Notice,Attendance,UniversityMarks,Syllabus,ExamTimetable,ClassTimetable


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'email','username','password1','password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    error_messages={
            'required': 'Please enter your username.',
            'max_length': 'Username cannot exceed 150 characters.'
    }
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    error_messages={
            'required': 'Please enter your password.'
        }

class StdProfileForm(forms.ModelForm):
    class Meta:
        model = StdProfile
        fields = ['department', 'semester','course', 'gender','roll_number']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'department','semester','course']

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'subject', 'marks']


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        
class UniversityMarksForm(forms.ModelForm):
    class Meta:
        model = UniversityMarks
        fields = ['student', 'subject', 'unimarks']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'month', 'year', 'attendance_percentage']


class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['course', 'syllabus_file']


class ExamTimetableForm(forms.ModelForm):
    exam_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = ExamTimetable
        fields = ['subject', 'exam_date', 'exam_time', 'semester']


class ClassTimetableForm(forms.ModelForm):
    class Meta:
        model = ClassTimetable
        fields = ['course', 'semester', 'day', 'start_time', 'end_time', 'subject']






class MarksFilterForm(forms.Form):
    department = forms.ChoiceField(choices=[])
    course = forms.ChoiceField(choices=[])
    semester = forms.ChoiceField(choices=[])
    subject = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        departments = kwargs.pop('departments', [])
        courses = kwargs.pop('courses', [])
        semesters = kwargs.pop('semesters', [])
        subjects = kwargs.pop('subjects', [])
        super().__init__(*args, **kwargs)
        self.fields['department'].choices = departments
        self.fields['course'].choices = courses
        self.fields['semester'].choices = semesters
        self.fields['subject'].choices = [('', 'All Subjects')] + subjects