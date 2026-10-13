# Proyek "2EZ4U APP" — Milestone 1 (M1)

**Studi Kasus Proyek Akhir — Struktur Data & Analisa Algoritma (EC234303)**  
**Dosen Pengampu:** Ir. Arta Kusuma Hernanda, S.T., M.T.  
*Program Sarjana, Departemen Teknik Komputer, Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC) — Institut Teknologi Sepuluh Nopember (ITS)*

---

## 1. Deskripsi Proyek & Milestone 1 (M1)

Proyek **2EZ4U APP** adalah pengembangan engine *backend* layanan pesan-antar makanan dan barang (*mini on-demand delivery service* seperti GoFood/GrabFood/ShopeeFood) berskala besar dengan beban lalu lintas tinggi.

Pada **Milestone 1 (M1)**, fokus utama adalah fondasi penyimpanan data pesanan yang masuk ke sistem:
- Data pesanan harus tersimpan aman, dapat dilihat kembali detailnya berdasarkan urutan (`lihat_pesanan(i)`), dapat ditambah pesanan baru, dan dapat dibatalkan/dihapus (`hapus_pesanan(i)`).
- Data yang sama disimpan pada **dua struktur data sekaligus**:
  1. **Larik Dinamis (Array)** dengan alokasi tetap dan penggandaan kapasitas 2× (*amortized* $O(1)$).
  2. **Rantai (Linked List)** berkait tunggal dengan penunjuk `head` dan `tail`.
- Keduanya diadu secara langsung menggunakan dataset produksi berukuran **200.000 baris** (`data/pesanan.csv`).

---

## 2. Aturan Bisnis & Tiga Titik Penyisipan

Aplikasi menerapkan aturan prioritas pemesanan dengan 3 kategori layanan:
1. **Pesanan REGULER (Prioritas 3)**:
   - Masuk dan mengantre di barisan paling belakang (posisi $n$).
2. **Pesanan PRIORITAS (Prioritas 2)**:
   - Menyerobot tepat ke tengah barisan (posisi $\lfloor n/2 \rfloor$).
3. **Pesanan VIP (Prioritas 1)**:
   - Langsung menempati urutan pertama antrean (posisi $0$ / terdepan).

Ketiga lokasi penyisipan ini dirancang secara sengaja untuk mengekspos karakteristik biaya waktu dan manipulasi memori dari kedua struktur data dasar.

---

## 3. Analisis Teoretis Kompleksitas Waktu (Big-O)

| Operasi | Deskripsi di Aplikasi | Array (Larik) | Linked List (Rantai) | Analisis Mekanisme |
| :--- | :--- | :---: | :---: | :--- |
| **Lihat pesanan ke-$i$** | Akses detail pesanan tertentu | $O(1)$ | $O(n)$ telusur | Array mengakses langsung via *offset* memori; Linked list harus merambati $i$ buah simpul dari `head`. |
| **Tambah REGULER** | Antre paling belakang ($n$) | $O(1)$ *amortized* | $O(1)$ | Array langsung mengisi indeks kosong terakhir; Linked list langsung menyambung via pointer `tail`. |
| **Tambah PRIORITAS**| Menyerobot ke tengah ($\lfloor n/2 \rfloor$) | $O(n)$ geser | $O(n)$ telusur | Array menggeser $\approx 100.000$ elemen ke kanan; Linked list menelusuri $\approx 100.000$ simpul lalu menyambung pointer sekali. |
| **Tambah VIP** | Masuk urutan terdepan ($0$) | $O(n)$ geser | $O(1)$ ubah pointer | Array wajib menggeser seluruh $200.000$ elemen; Linked list hanya membelokkan satu pointer `head` ke simpul baru. |
| **Hapus pesanan ke-$i$**| Pesanan dicabut dari antrean | $O(n)$ geser | $O(n)$ telusur | Array mencabut dan merapatkan sisa elemen ke kiri; Linked list menelusuri simpul ke-$(i-1)$ lalu memotong pointer `next`. |

---

## 4. Mekanisme Internal Struktur Data

### A. Larik Dinamis (Array Berukuran Tetap 2×)
Sebuah array primitif menempati petak memori berukuran tetap (`capacity`). Ketika kapasitas penuh dan elemen baru masuk:
1. Sistem mengalokasikan petak memori baru dengan kapasitas **dua kali lipat ($2 \times \text{capacity}$)**.
2. Seluruh elemen lama disalin ke petak baru.
3. Petak lama dibebaskan.

```
Kapasitas 4 (Penuh):   [ O-101 | O-102 | O-103 | O-104 ]  <- append(O-105) datang (tidak muat)
                                     |
                          Alokasi 2x & salin elemen
                                     v
Kapasitas 8:           [ O-101 | O-102 | O-103 | O-104 | O-105 | kosong | kosong | kosong ]
```

> **Mengapa amortized $O(1)$?**  
> Proses penyalinan berbiaya $O(n)$, namun hanya terjadi setiap kali kapasitas berlipat (sekitar 18 kali untuk 200.000 data). Jika biaya penyalinan dibagi rata ke seluruh operasi `append`, rata-rata biaya per operasi tetap konstan ($O(1)$).

### B. Rantai (Linked List dengan Head & Tail)
Linked List tidak memerlukan memori bersambung. Setiap pesanan dibungkus dalam objek simpul (`Node`) yang menyimpan data dan alamat simpul berikutnya (`next`).
- **Penunjuk `tail`**: Disimpan secara khusus agar operasi penambahan di ujung belakang (`append`) berjalan dalam $O(1)$ konstan tanpa perlu menelusuri dari depan.
- **Operasi VIP (`prepend`)**: Cukup membuat simpul baru dengan pointer mengarah ke `head` lama, lalu memperbarui `head`. Sangat efisien ($O(1)$).

---

## 5. Hasil Uji Empiris pada 200.000 Baris Data

Pengujian riil dijalankan pada mesin dengan dataset `data/pesanan.csv` (200.000 entitas pesanan):

| Jenis Operasi | Array (ms) | Linked List (ms) | Bukti Mekanisme Nyata |
| :--- | :---: | :---: | :--- |
| **REGULER** *(Ujung Belakang)* | **0.01 ms** | **0.01 ms** | Keduanya konstan $O(1)$. Array mengisi slot kosong cadangan, Linked List menyambung di pointer `tail`. |
| **PRIORITAS** *(Tengah Barisan)* | **3.71 - 5.96 ms** | **2.10 - 2.19 ms** | Array memindahkan $100.000$ elemen memori ke kanan; Linked list melangkah $100.000$ kali antar-simpul lalu menyambung sekali. |
| **VIP** *(Urutan Terdepan)* | **6.82 - 10.68 ms** | **0.00 - 0.01 ms** | **Linked list menang mutlak**: cukup 1 mutasi pointer. Array terbebani karena wajib menggeser seluruh $200.000$ elemen. |
| **LIHAT KE-$i$** *(Tengah)* | **0.00 - 0.01 ms** | **2.15 ms** | **Array menang mutlak**: $O(1)$ via kalkulasi alamat memori. Linked list harus menelusuri simpul demi simpul $O(n)$. |

---

## 6. Kepatuhan Aturan Main (*Strict Rule Compliance*)

Sesuai dengan ketentuan tugas (Aturan Main No. 2):
1. **100% Bebas Fungsi/Struktur Instan**:
   - TIDAK menggunakan `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, maupun `collections.*`.
   - TIDAK menggunakan sintaks literal `{}` kurung kurawal sama sekali di seluruh kode backend.
2. **Primitif & Mandiri**:
   - Menggunakan alokasi buffer `[None] * capacity` dan `list` primitif.
   - Menggunakan `tuple` dan kelas OOP dengan `__slots__` murni tanpa dictionary bawaan.
   - Seluruh logika pengindeksan, penyisipan, penggeseran memori, dan penautan simpul dibangun mandiri dari nol.

---

## 7. Struktur Repositori

```text
StrukDat/
|-- README.md                   <- Laporan komprehensif Milestone 1
|-- README-Proyek-2EZ4U.pdf     <- Panduan spesifikasi proyek
|-- app.py                      <- Entrypoint utama aplikasi desktop Tkinter
|
|-- data/
|   |-- pesanan.csv             <- Dataset 200.000 pesanan
|   `-- peta.csv                <- Data lokasi & peta graf
|
|-- backend/
|   |-- __init__.py
|   `-- m1_pesanan.py           <- Backend M1: Kelas Array, LinkList, Node, Pesanan, SistemPesananM1
|
|-- frontend/
|   |-- __init__.py
|   `-- ui.py                   <- Tampilan GUI satu jendela Tkinter (Sidebar, Form, Output, Command)
|
`-- tests/
    |-- __init__.py
    `-- test_m1.py              <- Pengujian unit otomatis (Array, LinkList, & sinkronisasi)
```

---

## 8. Cara Menjalankan

### Persyaratan Lingkungan
- Python versi 3.10 atau 3.11+
- Tkinter (sudah terpasang secara standar bersama instalasi resmi Python di Windows/macOS/Linux)

### 1. Menjalankan Aplikasi Antarmuka (GUI)
Jalankan perintah berikut di terminal:
```bash
python app.py
```

**Panduan Penggunaan GUI:**
1. Klik menu **DATA** $\rightarrow$ **Load** di bilah kiri, lalu tekan tombol **LOAD DATA** untuk memuat 200.000 pesanan dari `data/pesanan.csv`.
2. Pilih salah satu menu operasi pada **M1 - DATA PESANAN**:
   - `ARRAY - LIHAT PESANAN` / `LINKEDLIST - LIHAT PESANAN` (masukkan indeks ke-$i$)
   - `ARRAY - TAMBAH PESANAN REGULER` / `LINKEDLIST - TAMBAH PESANAN REGULER`
   - `ARRAY - TAMBAH PESANAN PRIORITAS` / `LINKEDLIST - TAMBAH PESANAN PRIORITAS`
   - `ARRAY - TAMBAH PESANAN VIP` / `LINKEDLIST - TAMBAH PESANAN VIP`
   - `ARRAY - HAPUS PESANAN` / `LINKEDLIST - HAPUS PESANAN`
3. Pilih menu **ADU PERFORMA ARRAY VS LINKEDLIST** untuk mengeksekusi *benchmark real-time* kelima operasi secara berdampingan.
4. Perhatikan panel **COMMAND** di bagian bawah yang mencatat waktu eksekusi setiap perintah secara presisi dalam milidetik (`ms`).

### 2. Menjalankan Pengujian Unit Otomatis
Untuk memvalidasi integritas logika dan batas kasus:
```bash
python -m unittest tests/test_m1.py
```
Seluruh 6 unit test akan lolos dalam waktu $\approx 1.2$ detik.
