from django.contrib import admin
from .models import Course, CourseContent, CourseMember, Comment, Completion

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Menampilkan nama kursus dan waktu dibuat di halaman daftar admin
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    
    # PAKSA SEMBUNYIKAN FIELD HARGA DAN PENGAJAR DARI FORM TAMBAH MATKUL:
    exclude = ('price', 'teacher')

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_id', 'parent_id')
    list_filter = ('course_id',)
    search_fields = ('name',)

@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'course_id', 'roles')
    list_filter = ('roles', 'course_id')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'content_id', 'created_at')

@admin.register(Completion)
class CompletionAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'content_id', 'last_update')

from django.contrib import admin

# Pastikan script ini disuntikkan ke Admin Site Django
admin.site.site_header = "Administrasi Django"

# Trik menyuntikkan JavaScript kustom ke seluruh halaman admin
class ControlAdminMessages:
    class Media:
        js = (
            'data:text/javascript,' + 
            'document.addEventListener("DOMContentLoaded", function() {'
            '    setTimeout(function() {'
            '        var messages = document.querySelectorAll(".messagelist, .success, .info, .warning, .error");'
            '        messages.forEach(function(el) {'
            '            el.style.transition = "opacity 0.5s ease";'
            '            el.style.opacity = "0";'
            '            setTimeout(function() { el.remove(); }, 500);'
            '        });'
            '    }, 5000);'
            '});',
        )

# Terapkan script ke admin default
admin.ModelAdmin.__bases__ = (ControlAdminMessages,) + admin.ModelAdmin.__bases__