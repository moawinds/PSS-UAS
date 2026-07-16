# Rencana Implementasi: Autentikasi Awal & Google Sign-In/Sign-Up

Rencana ini bertujuan untuk membatasi akses beranda (home) agar pengguna wajib login terlebih dahulu saat pertama kali membuka web, serta menambahkan fitur pendaftaran/masuk menggunakan Google.

## Pilihan Implementasi Google Sign-In

Kami menawarkan **dua metode** untuk integrasi Google Sign-In/Sign-Up. Mohon pilih metode yang paling sesuai dengan kebutuhan Anda:

### Metode A: Mock Google Login (Sangat Direkomendasikan untuk Demo/Presentasi UTS)
* **Kelebihan**: Bekerja secara instan dan 100% andal secara lokal tanpa memerlukan setup akun developer Google, Client ID, Client Secret, atau koneksi internet. Sangat cocok untuk demonstrasi dosen.
* **Cara Kerja**: Kami akan mendesain tombol "Daftar/Masuk dengan Google" yang indah. Ketika diklik, akan muncul jendela simulasi login Google (mirip popup asli). Pengguna dapat memilih akun simulasi dan sistem akan otomatis membuat/mendaftarkan akun Django lokal (berdasarkan email google simulasi) dan meloginkan mereka.

### Metode B: Real Google OAuth2 (Menggunakan `django-allauth`)
* **Kelebihan**: Integrasi asli menggunakan API Google. Pengguna benar-benar login melalui Google.
* **Cara Kerja**: Menggunakan library `django-allauth`.
* **Konsekuensi**: Anda harus membuat project di Google Cloud Console, membuat OAuth Credentials, menyetel Redirect URIs, lalu memasukkan Client ID dan Secret ke Django Admin secara manual. Jika setup ini salah, login Google akan error (gagal fungsi).

---

## Rencana Perubahan Kode

### 1. Pembatasan Halaman Utama (Wajib Login saat Pertama Buka)

* **Berkas**: [settings.py](file:///d:/PSS/PROJECT%20UTS%20PSS/code/simplelms/settings.py)
  * Menambahkan `LOGIN_URL = 'login'` di konfigurasi agar `@login_required` mengarah ke halaman login kustom `/login/`.
* **Berkas**: [views.py](file:///d:/PSS/PROJECT%20UTS%20PSS/code/core/views.py)
  * Menambahkan decorator `@login_required` pada fungsi `course_list`.

---

### 2. Antarmuka Login & Register (Google)

* **Berkas**: [login.html](file:///d:/PSS/PROJECT%20UTS%20PSS/code/templates/core/login.html)
  * Mendesain ulang halaman login agar memiliki tab/opsi "Masuk" dan "Daftar".
  * Menambahkan tombol desain Google ("Daftar/Masuk dengan Google") yang premium dengan logo resmi Google.
  * Mengintegrasikan alur login/registrasi (sesuai metode yang dipilih).

---

## Rencana Verifikasi

### Verifikasi Manual
1. Membuka browser pada alamat root `http://127.0.0.1:8000/`. Sistem harus otomatis mengalihkan (redirect) ke `http://127.0.0.1:8000/login/`.
2. Menguji alur Login biasa (username/password).
3. Menguji alur Google Sign-In/Sign-Up (baik secara mock maupun OAuth asli).
4. Memastikan setelah login berhasil, pengguna dialihkan ke daftar kursus.
5. Menguji alur logout dan memastikan pengguna dialihkan kembali ke login.
