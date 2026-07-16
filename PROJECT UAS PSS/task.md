# Rencana Tugas (Task Checklist) - Implementasi Mock Google Login & Autentikasi Awal

- [ ] Batasi Halaman Utama (Wajib Login)
  - [ ] Tambahkan `LOGIN_URL = 'login'` di `code/simplelms/settings.py`
  - [ ] Tambahkan `@login_required` ke fungsi `course_list` di `code/core/views.py`
- [ ] Integrasikan Mock Google Login & Sign-Up di Backend
  - [ ] Buat view `google_login_mock` di `code/core/views.py` yang menerima email, username, dan nama dari request AJAX, kemudian mendaftarkan atau meloginkan user ke Django Auth.
  - [ ] Daftarkan URL path `google-login-mock/` di `code/core/urls.py`
- [ ] Perbarui Desain & Interaksi Frontend (Login / Sign-Up Google)
  - [ ] Edit `code/templates/core/login.html` untuk memuat Tab "Masuk" dan "Daftar"
  - [ ] Tambahkan tombol "Sign in with Google" / "Sign up with Google" yang premium
  - [ ] Buat modal/popup Bootstrap di frontend yang mensimulasikan pilihan akun Google (misal: `alwi123@gmail.com` atau masukkan akun google kustom)
  - [ ] Kirim AJAX post ke backend untuk log in / sign up secara otomatis jika dipilih
- [ ] Verifikasi Hasil Akhir
