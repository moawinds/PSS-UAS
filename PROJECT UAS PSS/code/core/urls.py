from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # JALUR UTAMA: Jika belum login, paksa ke login Google. Jika sudah login, tampilkan daftar kursus.
    path('', lambda request: redirect('account_login') if not request.user.is_authenticated else redirect('course_list'), name='root_redirect'),
    
    path('content/<int:content_id>/complete/', views.mark_complete, name='mark_complete'),
    path('course/<int:course_id>/certificate/', views.download_certificate, name='download_certificate'),
    
    # KUNCIAN: Tambahkan 2 baris ini di paling bawah sebelum kurung siku tutup
    path('profile/', views.user_profile, name='user_profile'),
    path('achievements/', views.user_achievements, name='user_achievements'),
    
    # Memindahkan daftar kursus asli ke path /courses/ agar tidak bentrok dengan jalur utama
    path('courses/', views.course_list, name='course_list'),
    
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('testing/', views.testing, name='testing'),
    path('all-course/', views.allCourse, name='all_course'),
    path('user-courses/', views.userCourses, name='user_courses'),
    path('course-stat/', views.courseStat, name='course_stat'),
    path('course-member-stat/', views.courseMemberStat, name='course_member_stat'),
    path('course-detail-stat/<int:course_id>/', views.courseDetail, name='course_detail_stat'),
    path('user-stat/', views.userStat, name='user_stat'),
    path('user-detail-stat/<int:user_id>/', views.userDetailStat, name='user_detail_stat'),
    path('enroll/<int:pk>/', views.enroll_course, name='enroll_course'),
    path('course/<int:pk>/payment/', views.payment_page, name='payment_page'),
    path('course/<int:pk>/process-payment/', views.process_payment, name='process_payment'),
    path('login/', views.login_view, name='login'),
    path('google-login-mock/', views.google_login_mock, name='google_login_mock'),
    path('logout/', views.logout_view, name='logout'),
    
    # =====================================================================
    # TAMBAHAN FITUR: URL ROUTING UNTUK PROGRESS & SERTIFIKAT
    # =====================================================================
    path('content/<int:content_id>/complete/', views.mark_complete, name='mark_complete'),
    path('course/<int:course_id>/certificate/', views.download_certificate, name='download_certificate'),
]