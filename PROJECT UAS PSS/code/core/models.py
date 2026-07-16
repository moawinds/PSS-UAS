from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Course(models.Model):
    name = models.CharField("nama matkul", max_length=100)
    description = models.TextField("deskripsi", default='-')
    price = models.IntegerField("harga", default=10000, validators=[MinValueValidator(0)])
    image = models.ImageField("gambar", null=True, blank=True)
    teacher = models.ForeignKey(User, verbose_name="pengajar", on_delete=models.RESTRICT, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mata Kuliah"
        verbose_name_plural = "Mata Kuliah"

    def __str__(self) -> str:
        return self.name + " : " + str(self.price)

ROLE_OPTIONS = [('std', "Siswa"), ('ast', "Asisten")]

class CourseMember(models.Model):
    course_id = models.ForeignKey(Course, verbose_name="matkul", on_delete=models.RESTRICT)
    user_id = models.ForeignKey(User, verbose_name="siswa", on_delete=models.RESTRICT)
    roles = models.CharField("peran", max_length=3, choices=ROLE_OPTIONS, default='std')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscriber Matkul"
        verbose_name_plural = "Subscriber Matkul"
        unique_together = ('course_id', 'user_id')  # Cegah pendaftaran ganda

    def __str__(self) -> str:
        return str(self.course_id) + " : " + str(self.user_id)

class CourseContent(models.Model):
    name = models.CharField("judul konten", max_length=200)
    description = models.TextField("deskripsi", default='-')
    video_url = models.CharField("URL Video", max_length=200, null=True, blank=True)
    file_attachment = models.FileField("File", null=True, blank=True)
    course_id = models.ForeignKey(Course, verbose_name="matkul", on_delete=models.RESTRICT)
    parent_id = models.ForeignKey("self", verbose_name="induk", on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Konten Matkul"
        verbose_name_plural = "Konten Matkul"

    def __str__(self) -> str:
        return "[" + str(self.course_id) + "] " + self.name

class Comment(models.Model):
    content_id = models.ForeignKey(CourseContent, verbose_name="konten", on_delete=models.CASCADE)
    member_id = models.ForeignKey(CourseMember, verbose_name="pengguna", on_delete=models.CASCADE)
    comment = models.TextField("komentar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Komentar"

    def __str__(self) -> str:
        return str(self.member_id) + " : " + self.comment[:20]

class Completion(models.Model):
    member_id = models.ForeignKey(CourseMember, on_delete=models.CASCADE)
    content_id = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        # Menjamin satu member hanya punya satu status penyelesaian per konten
        unique_together = ('member_id', 'content_id')

    def __str__(self) -> str:
        return f"{self.member_id.user_id.username} selesai {self.content_id.name}"


class Certificate(models.Model):
    # Dihubungkan ke CourseMember agar konsisten dengan model Completion
    member = models.ForeignKey(
        CourseMember,
        on_delete=models.CASCADE,
        related_name="certificates"
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_number = models.CharField(
        max_length=50,
        unique=True
    )

    class Meta:
        unique_together = ("member",) # Satu pendaftaran kursus hanya dapat satu sertifikat

    def __str__(self):
        return self.certificate_number