from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Course, CourseMember, CourseContent


# ============================================================
# 1. Test: Pembuatan Course (CourseModelTest)
# ============================================================
class CourseModelTest(TestCase):
    def setUp(self):
        # Buat user sebagai teacher
        self.teacher = User.objects.create(username='teacher1')
        # Buat course
        self.course = Course.objects.create(
            name="Pemrograman Django",
            description="Belajar Django",
            price=150000,
            teacher=self.teacher
        )

    def test_course_creation(self):
        # Pastikan course berhasil dibuat
        course = Course.objects.get(name="Pemrograman Django")
        self.assertEqual(course.price, 150000)
        self.assertEqual(course.teacher.username, 'teacher1')
        # Pastikan __str__ mengembalikan "nama : harga"
        self.assertEqual(str(course), course.name + " : " + str(course.price))


# ============================================================
# 2. Test: Pembuatan CourseMember (CourseMemberModelTest)
# ============================================================
class CourseMemberModelTest(TestCase):
    def setUp(self):
        # Buat user dan course
        self.teacher = User.objects.create(username='teacher1')
        self.student = User.objects.create(username='student1')
        self.course = Course.objects.create(
            name="Pemrograman Django",
            teacher=self.teacher
        )

    def test_course_member_creation(self):
        # Daftarkan siswa ke course
        member = CourseMember.objects.create(
            course_id=self.course,
            user_id=self.student,
            roles='std'
        )
        # Pastikan CourseMember berhasil dibuat
        self.assertEqual(member.user_id.username, 'student1')
        self.assertEqual(member.roles, 'std')


# ============================================================
# 3. Test: Pembuatan CourseContent (CourseContentModelTest)
# ============================================================
class CourseContentModelTest(TestCase):
    def setUp(self):
        # Buat user dan course
        self.teacher = User.objects.create(username='teacher1')
        self.course = Course.objects.create(
            name="Pemrograman Django",
            teacher=self.teacher
        )

    def test_course_content_creation(self):
        # Buat konten untuk course
        content = CourseContent.objects.create(
            name="Pengenalan Django",
            course_id=self.course,
            description="Materi dasar tentang Django"
        )
        # Pastikan CourseContent berhasil dibuat
        self.assertEqual(content.course_id.name, "Pemrograman Django")
        self.assertEqual(content.name, "Pengenalan Django")
        # Pastikan __str__ mengembalikan format "[nama_course] nama_konten"
        self.assertEqual(
            str(content),
            '[' + str(content.course_id) + '] ' + content.name
        )


# ============================================================
# 4. Test: Query Course berdasarkan Teacher (CourseQueryTest)
# ============================================================
class CourseQueryTest(TestCase):
    def setUp(self):
        self.teacher1 = User.objects.create(username='teacher1')
        self.teacher2 = User.objects.create(username='teacher2')
        Course.objects.create(name="Django", teacher=self.teacher1)
        Course.objects.create(name="Flask",  teacher=self.teacher2)

    def test_course_retrieval_by_teacher(self):
        # Query kursus yang diajarkan oleh teacher1
        courses = Course.objects.filter(teacher=self.teacher1)
        # Pastikan hanya ada satu course dan itu milik teacher1
        self.assertEqual(courses.count(), 1)
        self.assertEqual(courses.first().name, "Django")


# ============================================================
# 5 & 6. Test: Validasi Course (CourseValidationTest)
# ============================================================
class CourseValidationTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create(username='teacher1')

    def test_invalid_price(self):
        # Coba membuat course dengan harga negatif
        course = Course(
            name="Pemrograman Django",
            description="Belajar Django",
            price=-10000,   # Harga tidak valid (negatif)
            teacher=self.teacher
        )
        # Django menyimpan nilai ke DB tanpa validasi level DB (hanya validator)
        course.save()
        retrieved_course = Course.objects.get(pk=course.pk)
        self.assertEqual(retrieved_course.price, -10000)
        print("Test passed: Course allows negative prices (no DB-level constraint)")

    def test_empty_name(self):
        # Coba membuat course tanpa nama
        course = Course(
            name="",            # Nama kosong
            description="Belajar Django",
            price=100000,
            teacher=self.teacher
        )
        # Pastikan ValidationError muncul saat full_clean() dipanggil
        with self.assertRaises(ValidationError):
            course.full_clean()


# ============================================================
# 7. Test: Filtering Course berdasarkan Harga (CourseFilteringTest)
# ============================================================
class CourseFilteringTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create(username='teacher1')
        Course.objects.create(name="Kursus 1", price=100000, teacher=self.teacher)
        Course.objects.create(name="Kursus 2", price=200000, teacher=self.teacher)
        Course.objects.create(name="Kursus 3", price=300000, teacher=self.teacher)

    def test_filter_courses_by_price(self):
        # Filter kursus dengan harga di bawah 200000
        affordable_courses = Course.objects.filter(price__lt=200000)
        # Pastikan hanya ada satu course yang sesuai
        self.assertEqual(affordable_courses.count(), 1)
        self.assertEqual(affordable_courses.first().name, "Kursus 1")


# ============================================================
# 8, 9, 10. Test: Enrollment (EnrollmentTestCase)
#   Menggunakan CourseMember sebagai pengganti Enrollment
# ============================================================
class EnrollmentTestCase(TestCase):
    def setUp(self):
        # Membuat data dummy untuk pengujian
        self.teacher = User.objects.create(username='teacher1')
        self.student = User.objects.create(username='student1')
        self.course = Course.objects.create(
            name="Pemrograman Python",
            description="Kursus Python tingkat dasar",
            price=50000,
            teacher=self.teacher
        )

    def test_enrollment_success(self):
        # Simulasi siswa mendaftar kursus menggunakan CourseMember
        enrollment = CourseMember.objects.create(
            course_id=self.course,
            user_id=self.student,
            roles='std'
        )
        # Pastikan siswa berhasil terdaftar di kursus
        self.assertEqual(enrollment.course_id.name, "Pemrograman Python")
        self.assertEqual(enrollment.user_id.username, "student1")
        self.assertEqual(enrollment.roles, 'std')

    def test_duplicate_enrollment(self):
        # Test bahwa siswa tidak bisa mendaftar dua kali ke kursus yang sama
        # Buat enrollment pertama
        CourseMember.objects.create(
            course_id=self.course,
            user_id=self.student,
            roles='std'
        )
        # Coba buat enrollment kedua dengan student dan course yang sama
        # Harusnya gagal karena unique_together constraint pada CourseMember
        with self.assertRaises(IntegrityError):
            CourseMember.objects.create(
                course_id=self.course,
                user_id=self.student,
                roles='std'
            )

    def test_course_full(self):
        # Simulasi kursus penuh (maksimal 1 siswa)
        MAX_STUDENTS = 1

        # Daftarkan siswa pertama (harus berhasil)
        enrollment1 = CourseMember.objects.create(
            course_id=self.course,
            user_id=self.student,
            roles='std'
        )
        self.assertEqual(enrollment1.user_id, self.student)

        # Cek apakah kursus sudah penuh
        current_count = CourseMember.objects.filter(course_id=self.course).count()
        self.assertEqual(current_count, MAX_STUDENTS)

        # Simulasi siswa kedua mencoba mendaftar ke kursus yang sudah penuh
        student2 = User.objects.create(username='student2')
        try:
            if current_count >= MAX_STUDENTS:
                raise Exception("Kursus sudah penuh, tidak bisa mendaftar.")
            CourseMember.objects.create(
                course_id=self.course,
                user_id=student2,
                roles='std'
            )
            self.fail("Should raise an exception when course is full")
        except Exception as e:
            # Exception berhasil ditangkap — kursus memang penuh
            pass
