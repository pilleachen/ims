from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    

class StdProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    DEPT_CHOICES = [
        ('CS', 'Computer Science'),
        ('CM', 'Commerce and Management'),
        ('EL', 'Electronics'),
    ]
    SEM_CHOICES = [
        ('S1', 'Semester 1'),
        ('S2', 'Semester 2'),
        ('S3', 'Semester 3'),
        ('S4', 'Semester 4'),
        ('S5', 'Semester 5'),
        ('S6', 'Semester 6'),
    ]
    COURSE_CHOICES = [
        ('BCA', 'Bachelor of Computer Application'),
        ('CS', 'B.Sc. Computer Science'),
        ('ELC', 'B.Sc. Electronics'),
        ('TAX', 'B.COM. Taxation'),
        ('FIN', 'B.COM. Finance'),
        ('BBA', ' Bachelor of Business Administration'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    department = models.CharField(max_length=2, choices=DEPT_CHOICES, default='CS')
    semester = models.CharField(max_length=2, choices=SEM_CHOICES, default='S4')
    course = models.CharField(max_length=3, choices=COURSE_CHOICES, default='BCA')
    
    roll_number = models.CharField(max_length=2)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    def __str__(self):
        return self.user.username
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Subject(models.Model):
    DEPT_CHOICES = [
        ('CS', 'Computer Science'),
        ('CM', 'Commerce and Management'),
        ('EL', 'Electronics'),
    ]
    SEM_CHOICES = [
        ('S1', 'Semester 1'),
        ('S2', 'Semester 2'),
        ('S3', 'Semester 3'),
        ('S4', 'Semester 4'),
        ('S5', 'Semester 5'),
        ('S6', 'Semester 6'),
    ]
    COURSE_CHOICES = [
        ('BCA', 'Bachelor of Computer Application'),
        ('CS', 'B.Sc. Computer Science'),
        ('ELC', 'B.Sc. Electronics'),
        ('TAX', 'B.COM. Taxation'),
        ('FIN', 'B.COM. Finance'),
        ('BBA', ' Bachelor of Business Administration'),
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=2, choices=DEPT_CHOICES, default='CS')
    semester = models.CharField(max_length=2, choices=SEM_CHOICES, default='S4')
    course = models.CharField(max_length=3, choices=COURSE_CHOICES, default='BCA')
    def __str__(self):
        return self.name
    
class Marks(models.Model):
    student = models.ForeignKey(StdProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField()

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} - {self.marks}"

class UniversityMarks(models.Model):
    student = models.ForeignKey(StdProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    unimarks = models.FloatField()

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} - {self.unimarks}"

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attendance(models.Model):
    student = models.ForeignKey(StdProfile, on_delete=models.CASCADE)
    month = models.CharField(max_length=10)
    year = models.IntegerField()
    attendance_percentage = models.FloatField()

    def __str__(self):
        return f"{self.student.full_name} - {self.month}/{self.year}"
    

class Course(models.Model):
    COURSE_CHOICES = [
        ('BCA', 'Bachelor of Computer Application'),
        ('CS', 'B.Sc. Computer Science'),
        ('ELC', 'B.Sc. Electronics'),
        ('TAX', 'B.COM. Taxation'),
        ('FIN', 'B.COM. Finance'),
        ('BBA', ' Bachelor of Business Administration'),
    ]
    name = models.CharField(max_length=3, choices=COURSE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Syllabus(models.Model):
    COURSE_CHOICES = [
        ('BCA', 'Bachelor of Computer Application'),
        ('CS', 'B.Sc. Computer Science'),
        ('ELC', 'B.Sc. Electronics'),
        ('TAX', 'B.COM. Taxation'),
        ('FIN', 'B.COM. Finance'),
        ('BBA', ' Bachelor of Business Administration'),
    ]
    course = models.CharField(max_length=3, choices=COURSE_CHOICES, unique=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    syllabus_file = models.FileField(upload_to='syllabi/')

    def __str__(self):
        return f"{self.course} - {self.uploaded_by.username}"
    

class ExamTimetable(models.Model):
    SEM_CHOICES = [
        ('S1', 'Semester 1'),
        ('S2', 'Semester 2'),
        ('S3', 'Semester 3'),
        ('S4', 'Semester 4'),
        ('S5', 'Semester 5'),
        ('S6', 'Semester 6'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date = models.DateField()
    exam_time = models.TimeField()
    semester = models.CharField(max_length=2, choices=SEM_CHOICES,)

    def __str__(self):
        return f"{self.subject.name} - {self.exam_date} - {self.exam_time}"



class ClassTimetable(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    SEM_CHOICES = [
        ('S1', 'Semester 1'),
        ('S2', 'Semester 2'),
        ('S3', 'Semester 3'),
        ('S4', 'Semester 4'),
        ('S5', 'Semester 5'),
        ('S6', 'Semester 6'),
    ]
    COURSE_CHOICES = [
        ('BCA', 'Bachelor of Computer Application'),
        ('CS', 'B.Sc. Computer Science'),
        ('ELC', 'B.Sc. Electronics'),
        ('TAX', 'B.COM. Taxation'),
        ('FIN', 'B.COM. Finance'),
        ('BBA', ' Bachelor of Business Administration'),
    ]
    
    course = models.CharField(max_length=3, choices=COURSE_CHOICES)
    semester = models.CharField(max_length=2, choices=SEM_CHOICES)
    day = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course} - {self.semester} - {self.day} - {self.subject.name}"