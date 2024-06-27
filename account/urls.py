from account import views
from django.urls import path
from .views import user_detail_view,add_subject, view_subjects, add_marks, view_marks


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
    path('add-marks/', views.add_marks, name='add_marks'),
    path('view-marks/', views.view_marks, name='view_marks'),
    path('notice_add', views.notice_create, name='notice_add'),
    path('notice_view/',views.notice_list, name='notice_view'),
    path('admin_home/', views.a_home,name='admin_home'),
    path('about/', views.about,name='about'),
] 
 