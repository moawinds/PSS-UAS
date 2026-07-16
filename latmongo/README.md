# Praktikum MongoDB (Pertemuan 12)

Folder ini berisi konfigurasi untuk menjalankan MongoDB menggunakan Docker dan contoh skrip inisialisasi database berdasarkan riwayat latihan kelas (`latmongo.cmd.txt`).

## Cara Menjalankan MongoDB dengan Docker

1. Buka aplikasi **Terminal** di Mac Anda.
2. Pindah ke direktori folder ini:
   ```bash
   cd "/Users/mohammadalwi/Downloads/UAS PSS/latmongo"
   ```
3. Jalankan container Docker:
   ```bash
   docker compose up -d
   ```
   *Catatan: Pastikan aplikasi Docker Desktop di Mac Anda sudah aktif.*

## Cara Masuk ke MongoDB Shell & Menjalankan Skrip

1. Setelah container berjalan, masuk ke MongoDB Shell dengan perintah:
   ```bash
   docker exec -it mongo mongosh
   ```
2. Setelah berhasil masuk ke MongoDB Shell, Anda dapat menyalin baris-baris perintah query yang ada di dalam berkas [skrip_mongodb.js](file:///Users/mohammadalwi/Downloads/UAS%20PSS/latmongo/skrip_mongodb.js) untuk mempraktikkan operasi CRUD dasar (Insert, Find, Update, dan Delete) seperti log kelas.
