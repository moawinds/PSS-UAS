from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required # Tambahan Baru
from .models import Course, CourseContent, Comment, CourseMember, Completion, Certificate # Diperbarui
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def course_list(request):
    # Pertemuan 10: Search, Sorting, dan Pagination
    from django.core.paginator import Paginator

    # 1. Ambil parameter dari URL query string
    search  = request.GET.get('search', '').strip()
    sort    = request.GET.get('sort', 'id')
    page    = request.GET.get('page', 1)

    # 2. Query dasar — ambil semua kursus beserta data teacher
    courses = Course.objects.select_related('teacher').all()

    # 3. FILTERING — cari berdasarkan nama kursus
    if search:
        courses = courses.filter(name__icontains=search)

    # 4. SORTING — urut berdasarkan kolom yang diizinkan
    allowed_sort = ['id', 'name', 'price', '-price', '-name']
    if sort in allowed_sort:
        courses = courses.order_by(sort)
    else:
        courses = courses.order_by('id')

    # 5. PAGINATION — 5 data per halaman (sesuai ketentuan Pertemuan 10)
    paginator    = Paginator(courses, 5)
    page_obj     = paginator.get_page(page)

    return render(request, 'core/course_list.html', {
        'page_obj' : page_obj,
        'courses'  : page_obj,          # alias agar template lama tetap kompatibel
        'search'   : search,
        'sort'     : sort,
        'title'    : 'Daftar Kursus LMS',
    })

def course_detail(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Silakan login terlebih dahulu untuk mengakses kursus.')
        return redirect('login')

    # Gunakan fungsi bawaan yang benar agar tidak error
    course = get_object_or_404(
        Course.objects.prefetch_related(
            'coursecontent_set__comment_set__member_id__user_id',
            'coursecontent_set__coursecontent_set'
        ),
        pk=pk
    )
    
    # Cek apakah user adalah pembuat kursus (teacher) atau superuser
    is_teacher_or_admin = (request.user == course.teacher) or request.user.is_superuser
    
    member = CourseMember.objects.filter(course_id=course, user_id=request.user).first()
    
    # Jika bukan member dan bukan teacher/admin, harus bayar dulu
    if not member and not is_teacher_or_admin:
        return redirect('payment_page', pk=pk)

    # 2. Siapkan variabel default untuk progress & sertifikat
    certificate = None
    completed_content_ids = []
    progress_percent = 0
    is_member = True

    # 3. Hitung progress & status sertifikatnya jika dia member
    if member:
        # Cek sertifikat lulus
        certificate = Certificate.objects.filter(member=member).first()
        
        # Ambil ID konten yang sudah diklik 'Mark as Complete'
        completed_content_ids = Completion.objects.filter(member_id=member)\
            .values_list('content_id_id', flat=True)
        
        # KOREKSI: Hanya hitung MATERI UTAMA (yang tidak punya parent_id) sebagai pembagi
        total_main_content = course.coursecontent_set.filter(parent_id__isnull=True).count()
        
        if total_main_content > 0:
            # Hitung berapa banyak materi utama yang sudah diselesaikan
            completed_main_count = course.coursecontent_set.filter(
                parent_id__isnull=True, 
                id__in=completed_content_ids
            ).count()
            
            # Gunakan fungsi round() agar menghasilkan angka bulat (misal: 33%, 25%)
            progress_percent = round((completed_main_count / total_main_content) * 100)

    # 4. Kirimkan seluruh data krusial ini ke template HTML Anda
    return render(request, 'core/course_detail.html', {
        'course': course,
        'certificate': certificate,
        'completed_content_ids': completed_content_ids,
        'progress_percent': progress_percent,
        'is_member': is_member
    })
    
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User

def testing(request):
    # Logika dari panduan dosen: Cek, Buat, Ambil, Hapus, dan Serialize
    user_test = User.objects.filter(username="usertesting")
    
    if not user_test.exists():
        user_test = User.objects.create_user(
            username="usertesting",
            email="usertest@email.com",
            password="sanditesting"
        )
    else:
        user_test = user_test.first()
        
    all_users = serializers.serialize('python', User.objects.all())
    
    admin = User.objects.get(pk=1)
    # user_test.delete() # Kita comment agar user-nya tetap ada untuk dilihat
    
    after_delete = serializers.serialize('python', User.objects.all())
    
    response = {
        "admin_user": serializers.serialize('python', [admin])[0],
        "all_users": all_users,
        "after_del": after_delete,
    }
    return JsonResponse(response)

def allCourse(request):
    # Logika Query Relasional dari panduan dosen
    allCourse = Course.objects.all()
    result = []
    for course in allCourse:
        record = {
            'id': course.id, 
            'name': course.name,
            'description': course.description,
            'price': course.price,
            'teacher': {
                'id': course.teacher.id,
                'username': course.teacher.username,
                'email': course.teacher.email,
                'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
            }
        }
        result.append(record)
from django.db.models import Max, Min, Avg, Count

def userCourses(request):
    # Select user data & his courses (as teacher)
    user = User.objects.get(pk=3)
    courses = Course.objects.filter(teacher=user.id)
    
    course_data = []
    for course in courses:
        record = {'id': course.id, 'name': course.name, 'description': course.description, 'price': course.price}
        course_data.append(record)
        
    result = {
        'id': user.id, 
        'username': user.username, 
        'email': user.email,
        'fullname': f"{user.first_name} {user.last_name}",
        'courses': course_data
    }
    return JsonResponse(result, safe=False)

def courseStat(request):
    # Select course data with aggregate (Sesuai Gambar N+1 Problems)
    courses = Course.objects.all()
    stats = courses.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    
    cheapest = Course.objects.filter(price=stats['min_price'])
    expensive = Course.objects.filter(price=stats['max_price'])
    
    popular = Course.objects.annotate(member_count=Count('coursemember'))\
        .order_by('-member_count')[:5]
        
    unpopular = Course.objects.annotate(member_count=Count('coursemember'))\
        .order_by('member_count')[:5]
        
    result = {
        'course_count': len(courses),
        'courses': stats,
        'cheapest': serializers.serialize('python', cheapest),
        'expensive': serializers.serialize('python', expensive),
        'popular': serializers.serialize('python', popular),
        'unpopular': serializers.serialize('python', unpopular)
    }
    return JsonResponse(result, safe=False)

def courseMemberStat(request):
    # Select filter course data with aggregate/annotate
    courses = Course.objects.filter(description__contains='python').annotate(member_num=Count('coursemember'))
    
    course_data = []
    for course in courses:
        record = {
            'id': course.id,
            'name': course.name,
            'price': course.price,
            'member_count': course.member_num
        }
        course_data.append(record)
        
    result = {
        'data_count': len(course_data),
        'data': course_data
    }
    return JsonResponse(result, safe=False)

def courseDetail(request, course_id):
    # Detail Statistik Course (Sesuai Gambar)
    course = Course.objects.annotate(
        member_count=Count('coursemember', distinct=True),
        content_count=Count('coursecontent', distinct=True),
        comment_count=Count('coursecontent__comment', distinct=True)
    ).get(pk=course_id)
    
    contents = CourseContent.objects.filter(course_id=course.id)\
        .annotate(count_comment=Count('comment'))\
        .order_by('-count_comment')[:3]
        
    result = {
        "name": course.name, 
        'description': course.description, 
        'price': course.price,
        'member_count': course.member_count, 
        'content_count': course.content_count,
        'teacher': {
            'username': course.teacher.username, 
            'email': course.teacher.email, 
            'fullname': course.teacher.first_name
        },
        'comment_stat': {
            'comment_count': course.comment_count,
            'most_comment': [
                {
                    'name': content.name,
                    'comment_count': content.count_comment
                } for content in contents
            ],
        }
    }
    return JsonResponse(result)

def userStat(request):
    # Statistik Semua User (Sesuai Gambar)
    non_admin = User.objects.filter(is_superuser=False)
    user_with_course = User.objects.annotate(num_course=Count('course')).filter(num_course__gt=0)
    user_no_course = User.objects.annotate(num_course=Count('course')).filter(num_course=0)
    
    # Rata-rata course yang diikuti per user
    avg_enroll = User.objects.annotate(num_enroll=Count('coursemember')).aggregate(Avg('num_enroll'))
    
    # User yang mengikuti course terbanyak
    most_enroll = User.objects.annotate(num_enroll=Count('coursemember')).order_by('-num_enroll').first()
    
    # List user yang tidak mengikuti course sama sekali
    zero_enroll = User.objects.annotate(num_enroll=Count('coursemember')).filter(num_enroll=0)
    
    result = {
        'total_non_admin': non_admin.count(),
        'users_creating_courses': user_with_course.count(),
        'users_no_courses_created': user_no_course.count(),
        'avg_courses_followed': avg_enroll['num_enroll__avg'],
        'top_student': {
            'username': most_enroll.username,
            'count': most_enroll.num_enroll
        } if most_enroll else None,
        'zero_enroll_users': serializers.serialize('python', zero_enroll)
    }
    return JsonResponse(result, safe=False)

def userDetailStat(request, user_id):
    # Detail Statistik User (Sesuai Gambar)
    user = User.objects.annotate(
        followed_count=Count('coursemember', distinct=True),
        created_count=Count('course', distinct=True),
        total_comments=Count('comment', distinct=True)
    ).get(pk=user_id)
    
    # Jumlah member dari semua course yang dibuat
    total_members = CourseMember.objects.filter(course_id__teacher=user).count()
    
    result = {
        'username': user.username,
        'email': user.email,
        'full_name': f"{user.first_name} {user.last_name}",
        'stats': {
            'courses_followed': user.followed_count,
            'courses_created': user.created_count,
            'total_students_in_his_courses': total_members,
            'total_comments_posted': user.total_comments
        }
    }
    return JsonResponse(result)

def enroll_course(request, pk):
    """Redirect ke halaman pembayaran sebelum mendaftar kursus."""
    if not request.user.is_authenticated:
        messages.warning(request, 'Silakan login terlebih dahulu untuk mendaftar kursus.')
        return redirect('login')

    course = get_object_or_404(Course, pk=pk)
    user = request.user

    # Jika sudah terdaftar, langsung ke halaman kursus
    if CourseMember.objects.filter(course_id=course, user_id=user).exists():
        messages.info(request, f'Anda sudah terdaftar di kursus ini.')
        return redirect('course_detail', pk=pk)

    # Arahkan ke halaman pembayaran
    return redirect('payment_page', pk=pk)


def payment_page(request, pk):
    """Tampilkan halaman pembayaran untuk kursus."""
    if not request.user.is_authenticated:
        return redirect('login')

    course = get_object_or_404(Course, pk=pk)
    user = request.user

    # Jika sudah terdaftar, tidak perlu bayar lagi
    if CourseMember.objects.filter(course_id=course, user_id=user).exists():
        return redirect('course_detail', pk=pk)

    return render(request, 'core/payment.html', {'course': course})


def process_payment(request, pk):
    """Proses konfirmasi pembayaran dan daftarkan user ke kursus."""
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method != 'POST':
        return redirect('payment_page', pk=pk)

    course = get_object_or_404(Course, pk=pk)
    user = request.user

    # Daftarkan user ke kursus setelah pembayaran dikonfirmasi
    if not CourseMember.objects.filter(course_id=course, user_id=user).exists():
        CourseMember.objects.create(
            course_id=course,
            user_id=user,
            roles='std'
        )
        messages.success(request, f'🎉 Pembayaran berhasil! Selamat bergabung di kursus {course.name}!')
    else:
        messages.info(request, 'Anda sudah terdaftar di kursus ini.')

    return redirect('course_detail', pk=pk)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('course_list')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Selamat datang kembali, {user.username}!')
                return redirect('course_list')
            else:
                messages.error(request, 'Username atau password salah.')
        else:
            messages.error(request, 'Username atau password salah.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Anda telah berhasil logout.')
    return redirect('course_list')

@login_required
def mark_complete(request, content_id):
    # 1. Ambil data materi/konten yang dituju
    content = get_object_or_404(CourseContent, pk=content_id)
    
    # 2. Ambil keanggotaan user (CourseMember) di kelas materi tersebut
    member = get_object_or_404(
        CourseMember, 
        course_id=content.course_id, 
        user_id=request.user
    )
    
    # 3. Masukkan ke tabel Completion jika belum ada (ditandai selesai)
    Completion.objects.get_or_create(
        member_id=member,
        content_id=content
    )
    
    # 4. Jalankan fungsi pengecekan otomatis apakah kelas sudah lulus semua
    check_course_completion(member)
    
    # 5. Kembalikan ke halaman detail kursus menggunakan pk kursusnya
    return redirect('course_detail', pk=content.course_id.id)


def check_course_completion(member):
    # 1. Hitung total materi UTAMA yang ada di kursus tersebut (tanpa sub-materi)
    total_main_content = CourseContent.objects.filter(course_id=member.course_id, parent_id__isnull=True).count()
    
    # 2. Ambil semua ID materi yang sudah diselesaikan oleh member
    completed_content_ids = Completion.objects.filter(member_id=member).values_list('content_id_id', flat=True)
    
    # 3. Hitung berapa banyak materi utama yang sukses diselesaikan
    completed_main_content = CourseContent.objects.filter(
        course_id=member.course_id,
        parent_id__isnull=True,
        id__in=completed_content_ids
    ).count()
    
    # 4. Jika jumlah materi utama yang selesai cocok dengan totalnya, buat sertifikat otomatis
    if total_main_content == completed_main_content and total_main_content > 0:
        Certificate.objects.get_or_create(
            member=member,
            defaults={
                "certificate_number": f"CERT-{member.user_id.id}-{member.course_id.id}"
            }
        )

@login_required
def download_certificate(request, course_id):
    import os
    from reportlab.lib.pagesizes import A4, landscape

    # 1. Cari data member yang bersangkutan di kelas ini
    member = get_object_or_404(
        CourseMember, 
        course_id=course_id, 
        user_id=request.user
    )
    
    # 2. Ambil data sertifikatnya dari database
    certificate = get_object_or_404(
        Certificate, 
        member=member
    )
    
    # 3. Siapkan response dengan content type PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Sertifikat_{request.user.username}_{course_id}.pdf"'
    
    # 4. Ukuran halaman: A4 Landscape (841.89 x 595.28 pt)
    page_w, page_h = landscape(A4)
    center_x = page_w / 2

    # 5. Buat canvas PDF
    p = canvas.Canvas(response, pagesize=landscape(A4))
    
    # 6. Gambar background template sertifikat kustom (full page)
    bg_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'static', 'images', 'certificate_background.png'
    )
    if os.path.exists(bg_path):
        p.drawImage(bg_path, 0, 0, width=page_w, height=page_h, preserveAspectRatio=False)
    
    # 7. ── OVERLAY TEKS DINAMIS SAJA ──
    # (Template sudah punya: CERTIFICATE, OF APPRECIATION, garis, medali, SIMPLE LMS)
    # Kita hanya tambahkan: Nama Mahasiswa, Nama Kursus, Nomor Sertifikat & Tanggal

    # ── Nama Mahasiswa ── (di area kosong tengah, gaya italic besar)
    full_name = request.user.get_full_name() or request.user.username
    p.setFont("Helvetica-BoldOblique", 34)
    p.setFillColorRGB(0.08, 0.18, 0.52)
    p.drawCentredString(center_x, page_h * 0.54, full_name.upper())

    # ── Nama Kursus ── (di bawah nama, area setelah garis template)
    course_name = member.course_id.name
    p.setFont("Helvetica", 10)
    p.setFillColorRGB(0.25, 0.25, 0.25)
    p.drawCentredString(center_x, page_h * 0.44,
        "Telah berhasil menyelesaikan seluruh materi dan dinyatakan lulus pada kursus:")
    p.setFont("Helvetica-Bold", 12)
    p.setFillColorRGB(0.08, 0.18, 0.52)
    p.drawCentredString(center_x, page_h * 0.415, f"\u00ab {course_name} \u00bb")

    # ── Nomor Sertifikat & Tanggal ── (di area bawah, di atas "SIMPLE LMS")
    p.setFont("Helvetica", 8)
    p.setFillColorRGB(0.4, 0.4, 0.4)
    p.drawCentredString(center_x, page_h * 0.195,
        f"No. Sertifikat: {certificate.certificate_number}   \u2022   "
        f"Diterbitkan: {certificate.issued_at.strftime('%d %B %Y')}")

    # 8. Selesaikan
    p.showPage()
    p.save()
    
    return response

    from django.shortcuts import redirect

def smart_login_redirect(request):
    # Cek apakah user yang login adalah Superuser (Admin)
    if request.user.is_superuser:
        return redirect('/admin/') # Lempar ke panel admin default
    else:
        return redirect('course_list') # Lempar user biasa ke daftar kursus

@login_required
def user_profile(request):
    return render(request, 'core/profile.html', {
        'user': request.user
    })

@login_required
def user_achievements(request):
    from .models import Certificate, CourseMember
    
    # 1. Cari list keanggotaan menggunakan field user_id
    user_memberships = CourseMember.objects.filter(user_id=request.user)
    
    # 2. Cari sertifikat yang terhubung dengan list keanggotaan tersebut
    certificates = Certificate.objects.filter(member__in=user_memberships)
    
    return render(request, 'core/achievements.html', {
        'certificates': certificates
    })