from account import views
from django.urls import path
from .views import user_detail_view,add_subject, view_subjects, add_marks
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.dashboard,name='dashboard'),
    path('home/', views.home,name='home'),
    path('register/', views.register,name='register'),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logoutUser,name='logout'),
    path('profile/', views.profile_view,name='profile'),
    path('faculty_home/', views.faculty_home,name='faculty_home'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('profilev/', views.user_detail_view,name='profilev'),
    path('user/<int:user_id>/', user_detail_view, name='user_detail'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('view-subjects/', view_subjects, name='view_subjects'),
    path('add_marks/', views.add_marks, name='add_marks'),
    path('notice_add', views.notice_create, name='notice_add'),
    path('notice_view/',views.notice_list, name='notice_view'),
    path('admin_home/', views.a_home,name='admin_home'),
    path('about/', views.about,name='about'),
    path('approval/',views.admin_approval, name='approval'),
    path('university_mrk/',views.filter_university_marks, name='university_mrk'),
    path('add_UniversityMarks/',views.add_UniversityMarks, name='add_UniversityMarks'),
    path('attendance/',views.attendance, name='attendance'),
    path('add_attendance/',views.add_attendance, name='add_attendance'),
    path('syllabus/',views.view_syllabi, name='syllabus'),
    path('add_syllabus/',views.upload_syllabus, name='add_syllabus'),
    path('add_exam/',views.add_exam_timetable, name='add_exam'),
    path('examtimetable/',views.view_exam_timetable, name='examtimetable'),
    path('add_classtimetable/',views.add_class_timetable, name='add_classtimetable'),
    path('classtimetable/',views.view_class_timetable, name='classtimetable'),
    path('filter_marks/', views.filter_marks, name='filter_marks'),
    path('view_marks/', views.filter_marks, name='view_marks'),
] 
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  