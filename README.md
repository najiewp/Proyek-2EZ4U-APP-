# Proyek "2EZ4U APP" — Milestone 1 (M1), Milestone 2 (M2), & Milestone 3 (M3)

**Studi Kasus Proyek Akhir — Struktur Data & Analisa Algoritma (EC234303)**  
**Dosen Pengampu:** Ir. Arta Kusuma Hernanda, S.T., M.T.  
*Program Sarjana, Departemen Teknik Komputer, Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC) — Institut Teknologi Sepuluh Nopember (ITS)*

---

## 1. Deskripsi Proyek

Proyek **2EZ4U APP** adalah pengembangan engine *backend* layanan pesan-antar makanan dan barang (*mini on-demand delivery service* seperti GoFood/GrabFood/ShopeeFood) berskala besar dengan beban lalu lintas tinggi.

Pengembangan dibagi ke dalam milestone terstruktur:
- **Milestone 1 (M1)**: Fondasi data pesanan menggunakan **Larik Dinamis (Array)** vs **Rantai (Linked List)** berpenunjuk `head` dan `tail`.
- **Milestone 2 (M2)**: Manajemen aliran layanan dapur & kasir menggunakan **Tumpukan (Stack LIFO)** untuk evaluator struk kasir & Undo/Redo, serta perbandingan **Antrean Naif (Naive Queue)** vs **Antrean Melingkar (Circular Queue FIFO)**.
- **Milestone 3 (M3)**: Penyusunan laporan harian operasional terurut & pencarian cepat menggunakan **Insertion Sort** ($O(n^2)$ stabil in-place) vs **Merge Sort** ($O(n \log n)$ stabil skala penuh $200.000$ data), serta **Linear Search** ($O(n)$) vs **Binary Search** ($O(\log n)$ berbasis indeks OID terurut).

---

## 2. Milestone 1 (M1): Data Pesanan (Array vs Linked List)

### A. Aturan Bisnis & Tiga Titik Penyisipan
Aplikasi menerapkan aturan prioritas pemesanan dengan 3 kategori layanan:
1. **Pesanan REGULER (Prioritas 3)**:
   - Masuk dan mengantre di barisan paling belakang (posisi $n$).
2. **Pesanan PRIORITAS (Prioritas 2)**:
   - Menyerobot tepat ke tengah barisan (posisi $\lfloor n/2 \rfloor$).
3. **Pesanan VIP (Prioritas 1)**:
   - Langsung menempati urutan pertama antrean (posisi $0$ / terdepan).

### B. Analisis Teoretis Kompleksitas Waktu M1 (Big-O)

| Operasi | Deskripsi di Aplikasi | Array (Larik) | Linked List (Rantai) | Analisis Mekanisme |
| :--- | :--- | :---: | :---: | :--- |
| **Lihat pesanan ke-$i$** | Akses detail pesanan tertentu | $O(1)$ | $O(n)$ telusur | Array mengakses langsung via *offset* memori; Linked list harus merambati $i$ buah simpul dari `head`. |
| **Tambah REGULER** | Antre paling belakang ($n$) | $O(1)$ *amortized* | $O(1)$ | Array langsung mengisi indeks kosong terakhir; Linked list langsung menyambung via pointer `tail`. |
| **Tambah PRIORITAS**| Menyerobot ke tengah ($\lfloor n/2 \rfloor$) | $O(n)$ geser | $O(n)$ telusur | Array menggeser $\approx 100.000$ elemen ke kanan; Linked list menelusuri $\approx 100.000$ simpul lalu menyambung sekali. |
| **Tambah VIP** | Masuk urutan terdepan ($0$) | $O(n)$ geser | $O(1)$ ubah pointer | Array wajib menggeser seluruh $200.000$ elemen; Linked list hanya membelokkan satu pointer `head` ke simpul baru. |
| **Hapus pesanan ke-$i$**| Pesanan dicabut dari antrean | $O(n)$ geser | $O(n)$ telusur | Array mencabut dan merapatkan sisa elemen ke kiri; Linked list menelusuri simpul ke-$(i-1)$ lalu memotong pointer `next`. |

### C. Hasil Uji Empiris M1 pada 200.000 Baris Data (`pesanan.csv`)

| Jenis Operasi | Array (ms) | Linked List (ms) | Bukti Mekanisme Nyata |
| :--- | :---: | :---: | :--- |
| **REGULER** *(Ujung Belakang)* | **0.01 ms** | **0.01 ms** | Keduanya konstan $O(1)$. Array mengisi slot kosong cadangan, Linked List menyambung di pointer `tail`. |
| **PRIORITAS** *(Tengah Barisan)* | **3.71 - 5.96 ms** | **2.10 - 2.19 ms** | Array memindahkan $100.000$ elemen memori ke kanan; Linked list melangkah $100.000$ kali antar-simpul. |
| **VIP** *(Urutan Terdepan)* | **6.82 - 10.68 ms** | **0.00 - 0.01 ms** | **Linked list menang mutlak**: cukup 1 mutasi pointer `head`. Array terbebani pergeseran $200.000$ elemen. |
| **LIHAT KE-$i$** *(Tengah)* | **0.00 - 0.01 ms** | **2.15 ms** | **Array menang mutlak**: $O(1)$ kalkulasi memori. Linked list harus menelusuri simpul demi simpul $O(n)$. |

---

## 3. Milestone 2 (M2): Antrean & Tumpukan (Queue & Stack)

Pada **Milestone 2 (M2)**, dua persoalan operasional diselesaikan:
1. **Di Kasir**: Struk pesanan ditulis dalam bentuk infix, misalnya `( 3 * 12000 ) + ( 2 * 8500 ) - 5000`. Komputer mengevaluasi ekspresi ini secara presisi melalui konversi ke **postfix** menggunakan **Stack (LIFO)**.
2. **Di Dapur**: Pesanan yang masuk harus dilayani berdasarkan prinsip *First-In, First-Out* (**FIFO**). Diimplementasikan dua varian antrean: **Antrean Naif** (larik linier + `pop(0)`) dan **Antrean Melingkar (Circular Queue)** berbasis pointer modulo, lengkap dengan mekanisme **Tumpukan Ganda (Undo & Redo)**.

### A. Mesin Kasir Postfix (Shunting-Yard & Evaluasi Nilai)

#### 1. Pemecah Token Berdigit Banyak
Angka berdigit banyak (seperti `12000` atau `8500`) diproses sebagai satu kesatuan bilangan utuh, bukan digit terpisah `1` lalu `2`.

#### 2. Tahap 1: Konversi Infix ke Postfix (Algoritma Shunting-Yard)
- Operand (angka) langsung diteruskan ke keluaran (*output*).
- Tanda kurung buka `(` didorong (*push*) ke tumpukan operator.
- Tanda kurung tutup `)` mengeluarkan (*pop*) operator dari tumpukan ke keluaran sampai bertemu `(`, lalu kurung buka tersebut dibuang.
- Operator aritmetika (`*`, `/`, `+`, `-`): jika operator di puncak tumpukan memiliki prioritas lebih tinggi atau sama kuat, puncak dikeluarkan terlebih dahulu ke keluaran sebelum operator baru didorong ke tumpukan. Prioritas `*` dan `/` ($2$) lebih tinggi dari `+` dan `-` ($1$).
- Setelah seluruh token habis, seluruh operator yang tersisa di tumpukan dikeluarkan ke keluaran.

#### 3. Tahap 2: Evaluasi Nilai Postfix (Pencegahan Bug Non-Komutatif)
Pada evaluasi ekspresi postfix:
- Angka didorong (*push*) ke dalam tumpukan nilai.
- Operator biner mengeluarkan dua operand teratas.
> [!IMPORTANT]
> **Urutan Pop Menentukan Kebenaran**:
> Operand yang keluar pertama adalah operand **kanan** ($b = \text{pop}()$), baru kemudian operand **kiri** ($a = \text{pop}()$). Operasi yang dihitung adalah $a - b$ dan $a / b$.
> Jika urutan terbalik, operasi `+` dan `*` tetap benar karena komutatif, namun `-` dan `/` akan menghasilkan nilai yang fatal keliru.

#### Transkrip Transparansi Eksekusi Struk Acuan ITS:
Ekspresi: `( 3 * 12000 ) + ( 2 * 8500 ) - 5000`
- **Hasil Notasi Postfix**: `3 12000 * 2 8500 * + 5000 -`
- **Total Pembayaran**: **Rp 48.000** (waktu komputasi $\approx 0.08\text{ ms}$).

---

### B. Antrean Naif vs Antrean Melingkar (Circular Queue)

Sebanyak **19.850 pesanan berstatus 'ANTRE'** dari `data/pesanan.csv` dimuat secara serentak ke dalam kedua struktur antrean untuk perbandingan jujur (*side-by-side*).

```text
1. CARA NAIF: Larik Linier + pop(0)
   [ A | B | C | D | E ] -> A keluar (dilayani)
     <=== <=== <=== <===   seluruh elemen sisa WAJIB digeser 1 petak ke kiri!
   Biaya per pesanan: O(n) pergeseran elemen memori.

2. ANTREAN MELINGKAR: Buffer Sirkular + Modulo K
         front = 2          rear = 5
             |                 |
             v                 v
   [ ... | O-103 | O-104 | O-105 | kosong | ... ]
   Melayani satu pesanan HANYA memajukan: front = (front + 1) % K
   0 ELEMEN DIGESER (O(1) konstan mutlak).
```

#### Mengapa Variabel `count` Mutlak Diperlukan?
> [!NOTE]
> Pada Antrean Melingkar, jika hanya penunjuk `front` dan `rear` yang disimpan:
> - Keadaan **kosong**: `front == rear`
> - Keadaan **penuh**: `front == rear`
>
> Kedua keadaan tersebut menghasilkan kondisi aritmetika pointer yang identik (*ambigu*).  
> Dengan menyertakan variabel pencacah `count`:
> - Kondisi kosong terdefinisi tegas saat `count == 0`.
> - Kondisi penuh terdefinisi tegas saat `count == capacity`.
> - Akses elemen ke-$i$ dari depan antrean dapat dihitung langsung secara $O(1)$ melalui rumus: `(front + i) % capacity`.

---

### C. Tumpukan Ganda: Undo dan Redo

Sistem menyediakan tombol **UNDO** dan **REDO** untuk membatalkan dan mengerjakan ulang mutasi pada antrean:

| Aksi Asal | Catatan di Tumpukan | Kebalikan saat `undo_last()` | Aksi Ulang saat `redo_last()` |
| :--- | :--- | :--- | :--- |
| **ENQUEUE** (`p`) | `CatatanAksi('ENQUEUE', [p])` | Cabut pesanan dari ujung belakang kedua antrean (`pop_belakang()`). | Masukkan kembali pesanan ke ujung belakang kedua antrean (`enqueue()`). |
| **DEQUEUE** (`daftar`) | `CatatanAksi('DEQUEUE', daftar)` | Kembalikan seluruh pesanan ke **DEPAN** antrean circular (`enqueue_depan()`). | Keluarkan kembali pesanan dari depan antrean circular (`dequeue_banyak()`). |

> [!WARNING]
> **Mengapa Aksi Baru WAJIB Mengosongkan Tumpukan Redo?**  
> Setelah satu atau beberapa kali *undo*, sistem berada pada simpul riwayat lampau. Jika pengguna mengeksekusi aksi baru (misalnya `ENQUEUE` pesanan baru), riwayat status telah **bercabang**. Aksi-aksi yang sebelumnya dibatalkan di tumpukan redo menjadi tidak valid secara kronologis. Jika tumpukan redo tidak dikosongkan, penekanan tombol redo berikutnya akan menempelkan mutasi usang ke keadaan baru sehingga urutan FIFO rusak permanen tanpa pesan kesalahan.

---

### D. Hasil Uji Empiris M2 pada 19.850 Antrean Riil

Pengujian riil dieksekusi langsung pada mesin dengan dataset produksi `pesanan.csv` (19.850 pesanan berstatus `ANTRE`):

| Operasi Antrean | Antrean Naif (Larik + pop(0)) | Antrean Melingkar (Circular Queue) | Keterangan Mekanisme Internal |
| :--- | :---: | :---: | :--- |
| **ENQUEUE (1 pesanan)** | **0.01 ms** *(0 geser)* | **0.01 ms** *(0 geser)* | Keduanya murah konstan $O(1)$ karena langsung mengisi petak cadangan di ujung belakang. |
| **DEQUEUE 1 pesanan** | **1.07 - 4.88 ms** *(19.850 geseran)* | **0.01 - 0.13 ms** *(0 geseran)* | **Circular menang mutlak**: Naif memindahkan seluruh 19.850 memori ke kiri; Circular hanya `front = (front+1) % K`. |
| **DEQUEUE 100 pesanan**| **90.15 - 93.27 ms** *(1.979.950 geseran)* | **0.03 ms** *(0 geseran)* | **Circular ~3.000× lebih cepat**: Naif melipatgandakan pergeseran memori hingga $\approx 2$ juta kali operasi. |
| **STACK UNDO (100 pesanan)**| — | **0.04 ms** | 100 pesanan dikembalikan langsung ke `front` antrean circular secara instan. |
| **STACK REDO (100 pesanan)**| — | **0.03 ms** | 100 pesanan dikeluarkan kembali ke status dilayani secara instan. |

---

## 4. Milestone 3 (M3): Pengurutan & Pencarian (Sort & Search)

### A. Latar Belakang & Studi Kasus Laporan Harian Warung

Layanan pesan-antar **2EZ4U** tutup pukul 9 malam. Pemilik warung membutuhkan **laporan harian** yang memuat seluruh pesanan hari itu, **terurut berdasarkan waktu selesai** (`t_selesai_detik`), untuk memetakan jam-jam sibuk (*peak hours*) dan mengevaluasi beban dapur.

Setelah laporan selesai disusun, muncul pertanyaan susulan dari manajer operasional:
> *"Pesanan O-4217 tadi selesai jam berapa?"*

Jawaban tidak boleh dicari dengan membaca seluruh laporan satu per satu dari baris pertama. Oleh karena itu, diimplementasikan dua pasang algoritma klasik:
1. **Dua Cara Mengurutkan**: **Insertion Sort** ($O(n^2)$) vs **Merge Sort** ($O(n \log n)$).
2. **Dua Cara Mencari**: **Linear Search** ($O(n)$) vs **Binary Search** ($O(\log n)$).

> [!IMPORTANT]
> **Mengapa Melaporkan Jumlah Perbandingan?**  
> Waktu eksekusi (milidetik) dipengaruhi oleh jenis prosesor, beban sistem operasi, dan *cache memory*. Sebaliknya, **jumlah perbandingan adalah parameter deterministik matematis** yang nilainya mutlak identik di komputer mana pun, dan angka perbandingan inilah yang membuktikan secara empiris perbedaan nyata antara kelas $O(n^2)$ melawan $O(n \log n)$ serta $O(n)$ melawan $O(\log n)$.

---

### B. Analisis Algoritma Pengurutan: Insertion Sort vs Merge Sort

#### 1. Insertion Sort (In-Place & Stabil)
- **Mekanisme**: Meniru cara seseorang merapikan kartu di tangan. Mulai dari elemen kedua, elemen disisipkan ke bagian kiri yang telah terurut dengan menggeser kartu-kartu yang lebih besar ke kanan.
- **Kompleksitas Waktu**:
  - Kasus Terburuk & Rata-rata: $O(n^2)$ karena rata-rata separuh elemen di sebelah kiri harus digeser untuk setiap elemen baru.
  - Kasus Terbaik: $O(n)$ pada data yang sudah atau hampir terurut (hampir tidak ada pergeseran).
- **Pembuktian Kestabilan (Stability)**:
  Pengurutan disebut **stabil** jika dua elemen dengan kunci sama tetap mempertahankan urutan relatif asalnya. Dalam kode `backend/m3_laporan.py`, syarat pergeseran menggunakan perbandingan **lebih besar secara tegas** (`>`), **BUKAN** lebih besar atau sama dengan (`>=`):
  ```python
  while j >= 0 and ambil_kunci(larik[j], kunci) > key_val:
      larik[j + 1] = larik[j]
      j -= 1
  ```
  Pada pengujian 10 data pertama dengan kunci `harga`, dua pesanan berharga sama **Rp 11.000** tetap terurut **O-000002** mendahului **O-000009** persis seperti urutan asalnya.
- **Batas Aman Penolakan ($n > 20.000$)**:
  Untuk $n = 200.000$, Insertion Sort membutuhkan $\approx \frac{n(n-1)}{4} \approx 10\text{ MILYAR}$ perbandingan yang akan membekukan antarmuka selama berjam-jam. Sistem secara tegas menolak $n > 20.000$ dengan pesan resmi:
  `DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh`

#### 2. Merge Sort (Divide & Conquer Stabil Skala Penuh)
- **Mekanisme**: Membelah data menjadi dua bagian secara rekursif hingga berukuran 1 elemen (basis rekursi), lalu menggabungkan (*merge*) kembali dua bagian terurut.
- **Kompleksitas Waktu**: $O(n \log n)$ di semua kondisi (terbaik, rata-rata, dan terburuk) karena pohon rekursi selalu berkedalaman $\log_2 n$ tingkat dan setiap tingkat memerlukan penggabungan berbiaya $O(n)$.
- **Pencegahan Dua Bug Klasik Penggabungan**:
  1. *Kehilangan data sisa*: Seluruh sisa elemen dari sub-larik kiri maupun kanan wajib disalin kembali setelah salah satu sub-larik habis.
  2. *Kehilangan kestabilan*: Syarat penggabungan wajib menggunakan operator **lebih kecil atau sama dengan** (`<=`), agar elemen dari sub-larik kiri selalu didahulukan saat nilai kuncinya sama.
- **Daya Tahan Skala Penuh**: Sanggup menuntaskan pengurutan seluruh **200.000 data** dalam waktu $\approx 1.13 - 2.07\text{ detik}$.

---

### C. Analisis Algoritma Pencarian: Linear Search vs Binary Search

#### 1. Linear Search ($O(n)$)
- **Mekanisme**: Menelusuri elemen larik dari indeks $0$ satu per satu sampai target ditemukan atau larik habis.
- **Keunggulan**: Bebas prasyarat — data boleh berantakan dan tidak terurut.
- **Biaya Kasus Terburuk**: Untuk mencari elemen di posisi paling belakang (`O-199999`), algoritma memeriksa seluruh $199.999$ baris ($199.999$ perbandingan).

#### 2. Binary Search ($O(\log n)$)
- **Mekanisme**: Mengambil nilai tengah (`mid = (lo + hi) // 2`). Jika target lebih besar, buang seluruh separuh kiri (`lo = mid + 1`); jika lebih kecil, buang separuh kanan (`hi = mid - 1`).
- **Efisiensi Radikal**: Membagi dua ruang pencarian pada setiap langkah. Pada $200.000$ baris data, pencarian selesai hanya dalam **16–17 perbandingan** ($0.01 - 0.03\text{ ms}$).
- **Kasus Batas yang Lolos Uji**:
  - Target tepat di tengah
  - Target di ujung paling kiri (indeks 0)
  - Target di ujung paling kanan (indeks $n-1$)
  - Target tidak ditemukan (mengembalikan $-1$)
  - Kasus larik kosong (mengembalikan $-1$ tanpa galat indeks)

#### 3. Analisis Trade-off: Kapan Memilih Tiap Algoritma?
> [!NOTE]
> **Binary Search Tidak Gratis**:
> Binary Search menuntut larik telah terurut berdasarkan kunci yang dicari. Jika data belum terurut menurut `oid`, larik terurut harus dibangun terlebih dahulu menggunakan Merge Sort (membutuhkan waktu $\approx 317 - 562\text{ ms}$).
> - **Pencarian Sekali-Dua Kali**: Linear Search ($O(n) \approx 24 - 53\text{ ms}$) lebih murah secara total daripada mengurutkan seluruh data terlebih dahulu.
> - **Pencarian Berulang-kali / Sistem Produksi**: Mengurutkan sekali di awal ($O(n \log n)$) memberikan keuntungan eksponensial karena ribuan pencarian berikutnya hanya berbiaya $O(\log n) \approx 0.02\text{ ms}$.

---

### D. Hasil Uji Empiris M3 pada Dataset Riil (`pesanan.csv`)

Pengujian empiris dieksekusi langsung pada dataset riil `data/pesanan.csv` ($200.000$ baris):

#### 1. Tabel Komparasi Pengurutan ($n$ vs Perbandingan & Waktu)

| Ukuran Data ($n$) | Kunci Pengurutan | Insertion Sort Perbandingan | Insertion Sort Waktu (ms) | Merge Sort Perbandingan | Merge Sort Waktu (ms) | Bukti Rasio & Teori Matematis |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **$n = 10$** | `harga` | **24** *(25 moves)* | **0.02 ms** | **21** *(34 moves)* | **0.03 ms** | Data kecil: keduanya instan. Kestabilan terbukti (`O-000002` lalu `O-000009`). |
| **$n = 2.000$** | `harga` | **962.430** | **163 - 278 ms** | **19.240** | **6.36 - 12.8 ms** | Merge Sort **~50× lebih sedikit** perbandingan dibanding Insertion Sort. |
| **$n = 4.000$** | `harga` | **3.831.520** | **660 - 1.125 ms** | **42.355** | **13.6 - 23.8 ms** | **Bukti Kuadratik**: $n$ naik 2× $\rightarrow$ Insertion melonjak **~3.98× (mendekati 4×)**; Merge naik **~2.20× (mendekati 2×)**. |
| **$n = 4.000$** | `oid` | — | — | **23.728** *(47.904 moves)*| **9.92 - 14.5 ms** | Sesuai persis dengan data uji acuan ITS pada halaman 18 PDF. |
| **$n = 200.000$** | `harga` | **DITOLAK** *(> 20.000)* | — | **3.226.139** | **1.13 - 2.07 s** | **Merge Sort sanggup menuntaskan data penuh**; Insertion Sort ditolak demi keamanan sistem. |

#### 2. Tabel Komparasi Pencarian pada $200.000$ Data Penuh

| Metode Pencarian | Target OID | Indeks / Baris Hasil | Jumlah Perbandingan | Waktu Komputasi | Efisiensi & Analisis Mekanisme |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Linear Search** | `O-137442` | Indeks 137.441 | **137.442** | **26.28 - 38.70 ms** | Memeriksa 1 per 1 baris yang dilewati sampai target ketemu di indeks 137.441. |
| **Binary Search** | `O-137442` | Baris 137.442 | **16 - 17** | **0.01 - 0.05 ms** | **~8.000× lebih hemat**: Memotong ruang pencarian secara biner dalam $\approx 16$ langkah. |
| **Linear Search** | `O-199999` | Indeks 199.998 | **199.999** | **24.52 - 53.01 ms** | Kasus terburuk: memeriksa hampir seluruh 200.000 elemen larik. |
| **Binary Search** | `O-199999` | Baris 199.999 | **17** | **0.02 - 0.03 ms** | **~11.700× lebih hemat**: Hanya butuh 17 perbandingan biner ($\lceil \log_2 200.000 \rceil = 18$). |
| **Binary Search** | `O-999999` | Tidak Ada (-1) | **18** | **0.02 ms** | Target tidak ada terdeteksi instan tanpa menyentuh seluruh isi larik. |

---

### E. Visualisasi Grafik Pertumbuhan Perbandingan

Grafik perbandingan jumlah operasi komputasi saat ukuran data $n$ dilipatduakan:

```text
JUMLAH PERBANDINGAN SORTING (Skala Logaritmik):
Operasi
 10^7 |                                                      [Insertion: ~10 Milyar (DITOLAK)]
      |                                                                 :
 10^6 |                                  * (3.831.520)                  :
      |                    * (962.430)   |                              :
 10^5 |                    |             |                              :
      |                    |             |                              * (3.226.139)
 10^4 |                    |             |              * (42.355)      |
      |                    |             * (19.240)     |               |
 10^2 |                    |             |              |               |
      |    * (24)          |             |              |               |
  10  |____*_(21)__________|_____________|______________|_______________|____
          n = 10         n = 2.000     n = 4.000      n = 4.000 (oid)  n = 200.000

LEGENDA:
[ * Atas ] : Insertion Sort O(n^2)  --> Pertumbuhan melonjak ~4x setiap n dilipatduakan.
[ * Bawah] : Merge Sort O(n log n)  --> Pertumbuhan landai ~2x setiap n dilipatduakan.
```

---

### F. Transkrip Eksekusi Konsol COMMAND (Sesuai Spesifikasi ITS)

Sistem menyediakan konsol perintah interaktif langsung pada panel **COMMAND** antarmuka GUI:

```text
> insertion_sort jumlah=2000 kunci=harga
2.000 pesanan terurut | 962.430 perbandingan [M3 - insertion sort] 163,26 ms

> merge_sort jumlah=2000 kunci=harga
2.000 pesanan terurut | 19.240 perbandingan [M3 - merge sort] 6,36 ms

> insertion_sort jumlah=4000 kunci=harga
4.000 pesanan terurut | 3.831.520 perbandingan [M3 - insertion sort] 660,36 ms

> merge_sort jumlah=4000 kunci=harga
4.000 pesanan terurut | 42.355 perbandingan [M3 - merge sort] 13,66 ms

> merge_sort jumlah=200000 kunci=harga
200.000 pesanan terurut | 3.226.139 perbandingan [M3 - merge sort] 1,13 s

> insertion_sort jumlah=200000
DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh

> linear_search O-199999
ditemukan di indeks 199.998 | 199.999 perbandingan [M3 - linear] 24,52 ms

> binary_search O-199999
daftar terurut oid dibangun sekali (merge sort) 562,58 ms
ditemukan di baris 199.999 | 17 perbandingan [M3 - binary] 0,03 ms

> cari_di_laporan O-004217
Pesanan O-004217 selesai pada pukul 08:35:12 (30912 detik) | 16 comps [M3 - binary] 0.02 ms
```

---

### G. Checklist Kesiapan Submit M3 (Halaman 21-22 PDF ITS)

- [x] **Keempat algoritma ada**: `insertion_sort`, `merge_sort`, `linear_search`, `binary_search`, dan masing-masing melaporkan jumlah perbandingannya.
- [x] **Kedua sort terbukti stabil**: Hasil pengurutan baris demi baris terbukti identik pada data yang sama (misal `O-000002` mendahului `O-000009` pada harga Rp 11.000).
- [x] **Merge sort benar di semua kondisi**: Berhasil pada data acak, terurut, terbalik (*reverse*), dan berisi banyak data duplikat.
- [x] **Binary search benar pada seluruh kasus**: Target tengah, target kiri (elemen pertama), target kanan (elemen terakhir), target tidak ditemukan, dan larik kosong.
- [x] **Menu insertion sort menolak data terlalu besar**: Input $> 20.000$ baris ditolak dengan pesan resmi tanpa membekukan GUI.
- [x] **Tabel $n$ versus perbandingan**: Lengkap tersaji di README beserta bukti empiris pelipatan kuadratik 4× vs 2× dan diagram grafiknya.
- [x] **Alasan pemilihan algoritma**: Terdokumentasi lengkap dan siap dijelaskan lisan pada sesi live demo.
- [x] **Seluruh tes otomatis hijau**: Sebanyak **36 unit tests (M1, M2, M3)** lulus 100% OK; Git tag `m3` tersemat dan ter-push ke Github.

---

## 5. Kepatuhan Aturan Main (*Strict Rule Compliance*)

Sesuai ketentuan tugas (Aturan Main No. 2):
1. **100% Bebas Fungsi/Struktur Instan Bawaan**:
   - TIDAK menggunakan `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, maupun modul `collections.*`.
   - TIDAK menggunakan literal `{}` kurung kurawal sama sekali di seluruh kode *backend*.
2. **Primitif & Mandiri**:
   - Menggunakan alokasi buffer `[None] * capacity` dan `list` primitif berindeks angka.
   - Menggunakan `tuple` dan kelas OOP dengan `__slots__` murni tanpa kamus bawaan.
   - Seluruh logika pengindeksan, mutasi pointer, modulo melingkar, tumpukan, partisi divide & conquer, serta binary search dibangun mandiri dari nol.

---

## 6. Struktur Repositori

```text
StrukDat/
|-- README.md                   <- Laporan komprehensif Milestone 1, 2, dan 3
|-- README-Proyek-2EZ4U.pdf     <- Panduan spesifikasi proyek dari dosen pengampu
|-- app.py                      <- Entrypoint utama aplikasi desktop Tkinter
|
|-- data/
|   |-- pesanan.csv             <- Dataset 200.000 pesanan (19.850 berstatus ANTRE)
|   `-- peta.csv                <- Data lokasi & peta graf
|
|-- backend/
|   |-- __init__.py
|   |-- m1_pesanan.py           <- Backend M1: Array, LinkList, Node, Pesanan, SistemPesananM1
|   |-- m2_antrean.py           <- Backend M2: Stack, KasirPostfix, AntreanNaif, AntreanMelingkar, SistemAntreanM2
|   |-- m3_laporan.py           <- Backend M3: InsertionSort, MergeSort, LinearSearch, BinarySearch, SistemLaporanM3
|   `-- m3_sort.py              <- Backend M3: Modul alias dan kompatibilitas M3
|
|-- frontend/
|   |-- __init__.py
|   `-- ui.py                   <- Tampilan GUI Tkinter (Sidebar, Form M1-M3, Tabel, Log, Postfix, Konsol Command)
|
`-- tests/
    |-- __init__.py
    |-- test_m1.py              <- Pengujian unit otomatis Milestone 1 (9 pengujian)
    |-- test_m2.py              <- Pengujian unit otomatis Milestone 2 (19 pengujian)
    `-- test_m3.py              <- Pengujian unit otomatis Milestone 3 (8 pengujian)
```

---

## 7. Cara Menjalankan

### Persyaratan Lingkungan
- Python versi 3.10 atau 3.11+
- Tkinter (pustaka standar bawaan Python)

### 1. Menjalankan Aplikasi Antarmuka (GUI)
Jalankan perintah berikut di terminal:
```bash
python app.py
```

**Panduan Penggunaan Fitur M3 pada GUI:**
1. **Pemuatan Data**:
   - Klik menu **DATA** $\rightarrow$ **Load** untuk memuat 200.000 pesanan. Sistem otomatis menyinkronkan data ke M1, M2, dan M3.
2. **Pengurutan Insertion Sort**:
   - Buka menu `SORT - INSERTION SORT`.
   - Masukkan jumlah baris $n$ (misal preset `10 (Uji PDF)`, `2.000`, atau `4.000`).
   - Pilih kunci pengurutan (`harga`, `oid`, `selesai`).
   - Tekan **URUTKAN (INSERTION SORT)** untuk melihat hasil terurut di tabel dan bukti perbandingan di panel COMMAND/Log.
   - Uji penolakan aman dengan menekan preset `200.000 (Uji Tolak)`.
3. **Pengurutan Merge Sort**:
   - Buka menu `SORT - MERGE SORT`.
   - Masukkan jumlah baris $n$ (misal `4.000` atau `200.000 (Semua Data)`).
   - Tekan **URUTKAN (MERGE SORT)** untuk mengurutkan seluruh 200.000 data dalam tempo $\approx 1.1\text{ detik}$.
4. **Pencarian Linear Search vs Binary Search**:
   - Buka menu `SEARCH - LINEAR SEARCH` atau `SEARCH - BINARY SEARCH`.
   - Masukkan target OID (misal preset `O-137442` atau `O-199999`).
   - Tekan tombol cari untuk membandingkan drastisnya perbedaan: Linear Search (199.999 perbandingan) vs Binary Search (hanya 17 perbandingan).
5. **Laporan Harian & Cari di Laporan**:
   - Buka `Laporan harian` untuk menyusun laporan harian terurut menurut waktu selesai dan melihat grafik sebaran jam sibuk dapur (*peak hours*).
   - Buka `Cari di laporan` untuk menjawab pertanyaan instan: *"pesanan O-4217 tadi selesai jam berapa?"*
6. **Adu Performa Otomatis M3**:
   - Klik menu `ADU PERFORMA SORT & SEARCH (M3)` untuk menjalankan pengujian komparasi side-by-side otomatis.
7. **Konsol Perintah Interaktif**:
   - Ketikkan perintah langsung di bilah `> ` di atas kotak COMMAND (misal: `insertion_sort jumlah=2000 kunci=harga` atau `binary_search O-199999`) lalu tekan **Enter** atau tombol **JALANKAN**.

### 2. Menjalankan Pengujian Unit Otomatis
Untuk menjalankan seluruh suite pengujian unit secara menyeluruh (M1, M2, & M3):
```bash
python -m unittest discover tests
```
Seluruh **36 pengujian unit** akan lolos (**OK**) dalam tempo $\approx 6.6$ detik.
