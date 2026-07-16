// SKRIP QUERY MONGODB SESUAI DENGAN LOG DOSEN (latmongo.cmd.txt)
// Anda dapat menyalin dan menjalankan baris-baris perintah ini di MongoDB Shell (mongosh)

// 1. Pindah / Gunakan database a71b
use a71b;

// 2. Tambah user Najwa
db.users.insertOne({
  name: "Najwa",
  username: "najwa",
  password: "123456"
});

// Tampilkan isi table/koleksi users
db.users.find();

// 3. Tambah user Ghiyatsi
db.users.insertOne({
  name: "Ghiyatsi",
  username: "ghiyatsi",
  password: "123456"
});

// Tampilkan data saat ini
db.users.find();

// 4. Update password Ghiyatsi menjadi 12345678
db.users.updateOne(
  { name: "Ghiyatsi" },
  { $set: { password: "12345678" } }
);

// Tampilkan untuk melihat hasil update password
db.users.find();

// 5. Tambah user sementara 'xxxx'
db.users.insertOne({
  name: "xxxx",
  username: "xxxx",
  password: "123456"
});

// Tampilkan untuk melihat data user 'xxxx' berhasil masuk
db.users.find();

// 6. Hapus user 'xxxx' yang telah dibuat
db.users.deleteOne({ name: "xxxx" });

// Tampilkan kembali data untuk memastikan 'xxxx' sudah terhapus
db.users.find();

// 7. Tambah beberapa user secara massal (anis & puji) menggunakan insertMany
db.users.insertMany([
  {
    name: "anis",
    username: "anis",
    password: "123456"
  },
  {
    name: "puji",
    username: "puji",
    password: "1234567"
  }
]);

// Tampilkan semua data users hasil akhir praktikum
db.users.find();
