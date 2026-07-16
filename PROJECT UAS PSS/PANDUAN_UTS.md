# Panduan UTS: Simple LMS (Django) - Sesuai Pertemuan 5-7

Project ini telah diperbarui agar sesuai dengan materi Pertemuan 5, 6, dan 7.

## 📁 Struktur Project
- `code/`: Folder utama project.
  - `simplelms/`: Pengaturan Django (Settings, URLs).
  - `core/`: Aplikasi LMS Utama (Models, Views, Admin).
- `docker-compose.yml`: Konfigurasi Docker & PostgreSQL.
- `venv/`: Virtual Environment.

## 🚀 Cara Menjalankan
1. Aktifkan Venv: `source venv/bin/activate`
2. Masuk ke folder code: `cd code`
3. Jalankan: `python manage.py runserver`

### 1. Pertemuan 5: Pengenalan Django
- Mengikuti panduan bootstrap:
  - Project Name: `simplelms`
  - App Name: `core`

## 📊 Apa yang Harus Kamu Tunjukkan Saat Presentasi?
1. **Dasar Django (Pertemuan 5)**: Struktur folder dan routing URL ke views.
2. **Dasar ORM (Pertemuan 6)**: 
   - Model `Course`, `CourseContent` (Hierarki), `CourseMember`, dan `Comment`.
   - Relasi `ForeignKey` dan relasi ke diri sendiri (`self`).
3. **Profiling & Optimasi (Pertemuan 7)**:
   - **Django Debug Toolbar**: Cek jumlah SQL query di Beranda dan Detail Materi.
   - **Django Silk**: Akses `http://127.0.0.1:8000/silk/` untuk analisis mendalam.
   - **Optimasi**: Penggunaan `select_related` dan `prefetch_related` di `lms/views.py`.

## 🔑 Login & URL Penting
- **Admin**: `http://127.0.0.1:8000/admin/` (User: `admin`, Pass: `admin123`)
- **Silk Profiler**: `http://127.0.0.1:8000/silk/`
