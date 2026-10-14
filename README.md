# Proyek "2EZ4U APP" — Milestone 1 (M1) & Milestone 2 (M2)

**Studi Kasus Proyek Akhir — Struktur Data & Analisa Algoritma (EC234303)**  
**Dosen Pengampu:** Ir. Arta Kusuma Hernanda, S.T., M.T.  
*Program Sarjana, Departemen Teknik Komputer, Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC) — Institut Teknologi Sepuluh Nopember (ITS)*

---

## 1. Deskripsi Proyek

Proyek **2EZ4U APP** adalah pengembangan engine *backend* layanan pesan-antar makanan dan barang (*mini on-demand delivery service* seperti GoFood/GrabFood/ShopeeFood) berskala besar dengan beban lalu lintas tinggi.

Pengembangan dibagi ke dalam milestone terstruktur:
- **Milestone 1 (M1)**: Fondasi data pesanan menggunakan **Larik Dinamis (Array)** vs **Rantai (Linked List)** berpenunjuk `head` dan `tail`.
- **Milestone 2 (M2)**: Manajemen aliran layanan dapur & kasir menggunakan **Tumpukan (Stack LIFO)** untuk evaluator struk kasir & Undo/Redo, serta perbandingan **Antrean Naif (Naive Queue)** vs **Antrean Melingkar (Circular Queue FIFO)**.

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

---

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

## 4. Kepatuhan Aturan Main (*Strict Rule Compliance*)

Sesuai ketentuan tugas (Aturan Main No. 2):
1. **100% Bebas Fungsi/Struktur Instan Bawaan**:
   - TIDAK menggunakan `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, maupun modul `collections.*`.
   - TIDAK menggunakan literal `{}` kurung kurawal sama sekali di seluruh kode *backend*.
2. **Primitif & Mandiri**:
   - Menggunakan alokasi buffer `[None] * capacity` dan `list` primitif berindeks angka.
   - Menggunakan `tuple` dan kelas OOP dengan `__slots__` murni tanpa kamus bawaan.
   - Seluruh logika pengindeksan, mutasi pointer, modulo melingkar, dan tumpukan dibangun mandiri dari nol.

---

## 5. Struktur Repositori

```text
StrukDat/
|-- README.md                   <- Laporan komprehensif Milestone 1 & Milestone 2
|-- README-Proyek-2EZ4U.pdf     <- Panduan spesifikasi proyek dari dosen pengampu
|-- app.py                      <- Entrypoint utama aplikasi desktop Tkinter
|
|-- data/
|   |-- pesanan.csv             <- Dataset 200.000 pesanan (19.850 berstatus ANTRE)
|   `-- peta.csv                <- Data lokasi & peta graf
|
|-- backend/
|   |-- __init__.py
|   |-- m1_pesanan.py           <- Backend M1: Kelas Array, LinkList, Node, Pesanan, SistemPesananM1
|   `-- m2_antrean.py           <- Backend M2: Stack, KasirPostfix, AntreanNaif, AntreanMelingkar, SistemAntreanM2
|
|-- frontend/
|   |-- __init__.py
|   `-- ui.py                   <- Tampilan GUI Tkinter (Sidebar, Form, Tabel, Log, Postfix, Command)
|
`-- tests/
    |-- __init__.py
    |-- test_m1.py              <- Pengujian unit otomatis Milestone 1 (9 pengujian)
    `-- test_m2.py              <- Pengujian unit otomatis Milestone 2 (19 pengujian)
```

---

## 6. Cara Menjalankan

### Persyaratan Lingkungan
- Python versi 3.10 atau 3.11+
- Tkinter (bawaan standar Python)

### 1. Menjalankan Aplikasi Antarmuka (GUI)
Jalankan perintah berikut di terminal:
```bash
python app.py
```

**Panduan Penggunaan Fitur M2 pada GUI:**
1. Klik menu **DATA** $\rightarrow$ **Load** untuk memuat 200.000 data pesanan (sekaligus menginisialisasi 19.850 pesanan antre ke antrean M2).
2. **Mesin Kasir Postfix**:
   - Buka menu `STACK - POSTFIX (MESIN KASIR)`.
   - Masukkan ekspresi aritmetika struk atau gunakan tombol preset yang tersedia (misal: acuan ITS `( 3 * 12000 ) + ( 2 * 8500 ) - 5000`).
   - Tekan **HITUNG STRUK KASIR** untuk melihat tabel transkrip langkah demi langkah pada tab **Transkrip Postfix Kasir**.
3. **Uji Antrean FIFO**:
   - `QUEUE - ENQUEUE`: Menambah pesanan baru ke belakang antrean.
   - `QUEUE - DEQUEUE NAIF`: Melayani pesanan dengan demonstrasi pergeseran larik $O(n)$.
   - `QUEUE - DEQUEUE CIRCULAR`: Melayani pesanan instan dengan penunjuk modulo $O(1)$ (0 elemen digeser).
4. **Tumpukan Undo & Redo**:
   - Klik `STACK - UNDO` untuk membatalkan aksi antrean terakhir.
   - Klik `STACK - REDO` untuk mengerjakan ulang aksi yang dibatalkan.
5. **Adu Performa Langsung M2**:
   - Klik `ADU PERFORMA DEQUEUE NAIF VS CIRCULAR` untuk menjalankan pengujian komparasi otomatis $k=1$ dan $k=100$ pada dataset 19.850 antrean.

### 2. Menjalankan Pengujian Unit Otomatis
Untuk menjalankan seluruh suite pengujian unit secara menyeluruh (M1 & M2):
```bash
python -m unittest discover tests
```
Seluruh **28 pengujian unit** akan lolos (**OK**) dalam waktu $\approx 1.4$ detik.
