# ==============================================================================
# PROYEK "2EZ4U APP" - STRUKTUR DATA & ANALISA ALGORITMA (EC234303)
# Modul: backend/m1_pesanan.py
# Milestone 1: Larik (Array Berukuran Tetap + Penggandaan) vs Rantai (Linked List)
# Kepatuhan: Struktur data buatan sendiri secara mandiri dari nol (primitif)
# ==============================================================================

import time
import csv


class Pesanan:
    """
    Representasi entitas sebuah pesanan makanan/barang.
    Menggunakan __slots__ untuk efisiensi memori tingkat tinggi.
    """
    __slots__ = (
        'oid',
        'pelanggan',
        'resto',
        'menu',
        'harga',
        'prioritas',
        't_masuk_detik',
        't_selesai_detik',
        'status'
    )

    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas,
                 t_masuk_detik, t_selesai_detik=None, status="ANTRE"):
        self.oid = str(oid)
        self.pelanggan = str(pelanggan)
        self.resto = str(resto)
        self.menu = str(menu)
        self.harga = int(harga) if (harga is not None and harga != "") else 0
        self.prioritas = int(prioritas) if (prioritas is not None and prioritas != "") else 3
        self.t_masuk_detik = int(t_masuk_detik) if (t_masuk_detik is not None and t_masuk_detik != "") else 0
        if t_selesai_detik is not None and t_selesai_detik != "":
            self.t_selesai_detik = int(t_selesai_detik)
        else:
            self.t_selesai_detik = None
        self.status = str(status)

    def to_tuple(self):
        return (
            self.oid,
            self.pelanggan,
            self.resto,
            self.menu,
            self.harga,
            self.prioritas,
            self.t_masuk_detik,
            self.t_selesai_detik,
            self.status
        )

    def format_t_masuk(self):
        total = self.t_masuk_detik
        jam = total // 3600
        sisa = total % 3600
        menit = sisa // 60
        detik = sisa % 60
        return "%02d:%02d:%02d" % (jam, menit, detik)

    def format_t_selesai(self):
        if self.t_selesai_detik is None:
            return "-"
        total = self.t_selesai_detik
        jam = total // 3600
        sisa = total % 3600
        menit = sisa // 60
        detik = sisa % 60
        return "%02d:%02d:%02d" % (jam, menit, detik)

    def format_harga(self):
        s = str(self.harga)
        n = len(s)
        if n <= 3:
            return s
        parts = []
        rem = n % 3
        if rem > 0:
            parts.append(s[:rem])
        idx = rem
        while idx < n:
            parts.append(s[idx:idx + 3])
            idx += 3
        return ".".join(parts)

    def __repr__(self):
        return "Pesanan(%s, %s, %s, %d)" % (self.oid, self.pelanggan, self.menu, self.harga)


class Array:
    """
    Implementasi Larik Dinamis berukuran tetap (fixed-size buffer) buatan sendiri.
    Ketika kapasitas penuh, kapasitas dilipatduakan (2x), seluruh elemen disalin,
    lalu buffer lama dilepas. Memenuhi biaya amortized O(1) untuk append.
    """
    def __init__(self, initial_capacity=4):
        init_cap = initial_capacity if initial_capacity > 0 else 4
        self.capacity = init_cap
        self.size = 0
        self.data = [None] * self.capacity
        self.last_shift_count = 0
        self.resize_count = 0

    def _resize(self, new_capacity):
        """Alokasi petak baru berukuran 2x, salin isi lama."""
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity
        self.resize_count += 1

    def append(self, v):
        """
        Tambah elemen di barisan paling belakang.
        Amortized O(1). Elemen digeser: 0.
        """
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.size] = v
        self.size += 1
        self.last_shift_count = 0
        return 0

    def insert(self, i, v):
        """
        Sisipkan elemen pada indeks i.
        O(n). Menggeser elemen dari size - 1 sampai i ke kanan.
        """
        if i < 0:
            i = 0
        elif i > self.size:
            i = self.size

        if self.size == self.capacity:
            self._resize(self.capacity * 2)

        shifts = 0
        for j in range(self.size, i, -1):
            self.data[j] = self.data[j - 1]
            shifts += 1

        self.data[i] = v
        self.size += 1
        self.last_shift_count = shifts
        return shifts

    def get(self, i):
        """
        Akses elemen pada indeks i.
        O(1) langsung via alamat memori terindeks.
        """
        if i < 0 or i >= self.size:
            raise IndexError("Indeks array di luar rentang: " + str(i))
        return self.data[i]

    def ubah(self, i, v):
        """Ubah elemen pada indeks i. O(1)."""
        if i < 0 or i >= self.size:
            raise IndexError("Indeks array di luar rentang: " + str(i))
        self.data[i] = v

    def put(self, i, v):
        """Alias untuk ubah(i, v)."""
        self.ubah(i, v)

    def delete(self, i):
        """
        Hapus elemen pada indeks i.
        O(n). Menggeser elemen dari i + 1 sampai size - 1 ke kiri.
        """
        if i < 0 or i >= self.size:
            raise IndexError("Indeks array di luar rentang: " + str(i))
        removed = self.data[i]
        shifts = 0
        for j in range(i, self.size - 1):
            self.data[j] = self.data[j + 1]
            shifts += 1
        self.data[self.size - 1] = None
        self.size -= 1
        self.last_shift_count = shifts
        return removed

    # Alias sesuai modul M1
    def lihat_pesanan(self, i):
        return self.get(i)

    def tambah_reguler(self, v):
        """REGULER: masuk barisan paling belakang O(1) amortized."""
        self.append(v)
        return self.last_shift_count

    def tambah_prioritas(self, v):
        """PRIORITAS: menyerobot ke tengah barisan (n // 2) O(n)."""
        tengah = self.size // 2
        return self.insert(tengah, v)

    def tambah_vip(self, v):
        """VIP: langsung ke urutan pertama (indeks 0) O(n)."""
        return self.insert(0, v)

    def hapus_pesanan(self, i):
        return self.delete(i)

    def is_empty(self):
        return self.size == 0

    def clear(self):
        self.capacity = 4
        self.size = 0
        self.data = [None] * self.capacity
        self.last_shift_count = 0
        self.resize_count = 0

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        return self.get(i)

    def __setitem__(self, i, v):
        self.ubah(i, v)

    def __iter__(self):
        for idx in range(self.size):
            yield self.data[idx]

    def pop(self, i=None):
        if i is None:
            i = self.size - 1
        return self.delete(i)

    def find_by_oid(self, oid):
        for idx in range(self.size):
            if self.data[idx] is not None and self.data[idx].oid == oid:
                return idx
        return -1


class Node:
    """Simpul Linked List tunggal."""
    __slots__ = ('data', 'next')

    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


class LinkList:
    """
    Implementasi Linked List buatan sendiri dengan pointer head dan tail.
    Tail disimpan agar penambahan di ujung belakang (append) tetap O(1).
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.last_traversal_count = 0

    def append(self, v):
        """
        Tambah elemen di barisan paling belakang.
        O(1) karena menggunakan penunjuk tail.
        """
        new_node = Node(v)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        self.last_traversal_count = 0
        return 0

    def prepend(self, v):
        """
        Tambah elemen di urutan pertama (head).
        O(1) langsung ubah penunjuk head tanpa telusur.
        """
        new_node = Node(v, self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1
        self.last_traversal_count = 0
        return 0

    def insert(self, i, v):
        """
        Sisipkan elemen pada posisi indeks i.
        O(n) telusur untuk mencari simpul ke-(i-1).
        """
        if i <= 0:
            return self.prepend(v)
        if i >= self.size:
            return self.append(v)

        curr = self.head
        traversals = 0
        for _ in range(i - 1):
            curr = curr.next
            traversals += 1

        new_node = Node(v, curr.next)
        curr.next = new_node
        self.size += 1
        self.last_traversal_count = traversals + 1
        return traversals + 1

    def get(self, i):
        """
        Akses elemen pada indeks i.
        O(n) telusur simpul langkah demi langkah.
        """
        if i < 0 or i >= self.size:
            raise IndexError("Indeks linked list di luar rentang: " + str(i))
        curr = self.head
        traversals = 0
        for _ in range(i):
            curr = curr.next
            traversals += 1
        self.last_traversal_count = traversals
        return curr.data

    def delete(self, i):
        """
        Hapus elemen pada indeks i.
        O(n) telusur untuk menemukan simpul pendahulu lalu putus sambungan.
        """
        if i < 0 or i >= self.size:
            raise IndexError("Indeks linked list di luar rentang: " + str(i))

        if i == 0:
            removed = self.head.data
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            self.last_traversal_count = 0
            return removed

        prev = self.head
        traversals = 0
        for _ in range(i - 1):
            prev = prev.next
            traversals += 1

        target = prev.next
        removed = target.data
        prev.next = target.next
        if prev.next is None:
            self.tail = prev
        self.size -= 1
        self.last_traversal_count = traversals + 1
        return removed

    # Alias sesuai modul M1
    def lihat_pesanan(self, i):
        return self.get(i)

    def tambah_reguler(self, v):
        """REGULER: masuk barisan paling belakang O(1)."""
        return self.append(v)

    def tambah_prioritas(self, v):
        """PRIORITAS: menyerobot ke tengah barisan (n // 2) O(n) telusur."""
        tengah = self.size // 2
        return self.insert(tengah, v)

    def tambah_vip(self, v):
        """VIP: langsung ke urutan pertama O(1) ubah satu penunjuk."""
        return self.prepend(v)

    def hapus_pesanan(self, i):
        return self.delete(i)

    def is_empty(self):
        return self.size == 0

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.last_traversal_count = 0

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        return self.get(i)

    def __iter__(self):
        curr = self.head
        while curr is not None:
            yield curr.data
            curr = curr.next

    def pop(self, i=None):
        if i is None:
            i = self.size - 1
        return self.delete(i)

    def find_by_oid(self, oid):
        curr = self.head
        idx = 0
        while curr is not None:
            if curr.data is not None and curr.data.oid == oid:
                return idx
            curr = curr.next
            idx += 1
        return -1


class SistemPesananM1:
    """
    Pengelola Backend Milestone 1.
    Menyimpan data pesanan pada dua struktur data sekaligus:
    Array dan LinkList, sehingga performa dapat diadu secara adil.
    """
    def __init__(self):
        self.array = Array(4)
        self.linklist = LinkList()
        self.max_id_num = 0
        self.is_loaded = False

    def muat_csv(self, filepath):
        """
        Membaca data pesanan dari berkas CSV dan memuatnya ke kedua struktur.
        Mengembalikan tuple: (total_baris, durasi_array_ms, durasi_ll_ms).
        """
        self.array.clear()
        self.linklist.clear()
        self.max_id_num = 0

        # Muat ke Array
        t0 = time.perf_counter()
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # lewati header
            for row in reader:
                if len(row) < 9:
                    continue
                p = Pesanan(row[0], row[1], row[2], row[3], row[4],
                            row[5], row[6], row[7], row[8])
                self.array.append(p)
                oid_str = row[0]
                if oid_str.startswith("O-"):
                    try:
                        num = int(oid_str[2:])
                        if num > self.max_id_num:
                            self.max_id_num = num
                    except ValueError:
                        pass
        t1 = time.perf_counter()
        durasi_array_ms = (t1 - t0) * 1000.0

        # Muat ke LinkList
        t0 = time.perf_counter()
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) < 9:
                    continue
                p = Pesanan(row[0], row[1], row[2], row[3], row[4],
                            row[5], row[6], row[7], row[8])
                self.linklist.append(p)
        t1 = time.perf_counter()
        durasi_ll_ms = (t1 - t0) * 1000.0

        self.is_loaded = True
        return (self.array.size, durasi_array_ms, durasi_ll_ms)

    def generate_oid(self):
        self.max_id_num += 1
        return "O-%06d" % self.max_id_num

    # ================= Operasi Array =================
    def array_lihat(self, i):
        t0 = time.perf_counter()
        p = self.array.lihat_pesanan(i)
        t1 = time.perf_counter()
        return (p, (t1 - t0) * 1000.0, 0)

    def array_tambah_reguler(self, p, sinkron=True):
        p.prioritas = 3
        t0 = time.perf_counter()
        self.array.tambah_reguler(p)
        t1 = time.perf_counter()
        durasi = (t1 - t0) * 1000.0
        shifts = self.array.last_shift_count
        if sinkron:
            self.linklist.tambah_reguler(p)
        return (p, durasi, shifts)

    def array_tambah_prioritas(self, p, sinkron=True):
        p.prioritas = 2
        t0 = time.perf_counter()
        self.array.tambah_prioritas(p)
        t1 = time.perf_counter()
        durasi = (t1 - t0) * 1000.0
        shifts = self.array.last_shift_count
        if sinkron:
            self.linklist.tambah_prioritas(p)
        return (p, durasi, shifts)

    def array_tambah_vip(self, p, sinkron=True):
        p.prioritas = 1
        t0 = time.perf_counter()
        self.array.tambah_vip(p)
        t1 = time.perf_counter()
        durasi = (t1 - t0) * 1000.0
        shifts = self.array.last_shift_count
        if sinkron:
            self.linklist.tambah_vip(p)
        return (p, durasi, shifts)

    def array_hapus(self, i, sinkron=True):
        t0 = time.perf_counter()
        p = self.array.hapus_pesanan(i)
        t1 = time.perf_counter()
        durasi = (t1 - t0) * 1000.0
        shifts = self.array.last_shift_count
        if sinkron and i < self.linklist.size:
            self.linklist.hapus_pesanan(i)
        return (p, durasi, shifts)

    # ================= Operasi LinkList =================
    def linklist_lihat(self, i):
        t0 = time.perf_counter()
        p = self.linklist.lihat_pesanan(i)
        t1 = time.perf_counter()
        durasi = (t1 - t0) * 1000.0
        traversals = self.linklist.last_traversal_count
        return (p, durasi, traversals)

    def linklist_tambah_reguler(self, p, sinkron=True):
        p.prioritas = 3
        t0 = time.perf_counter()
        self.linklist.tambah_reguler(p)
        t1 = time.perf_counter()
        durasi = (t1 - t0) * 1000.0
        traversals = self.linklist.last_traversal_count
        if sinkron:
            self.array.tambah_reguler(p)
        return (p, durasi, traversals)

    def linklist_tambah_prioritas(self, p, sinkron=True):
        p.prioritas = 2
        t0 = time.perf_counter()
        self.linklist.tambah_prioritas(p)
        t1 = time.perf_counter()
        durasi = (t1 - t0) * 1000.0
        traversals = self.linklist.last_traversal_count
        if sinkron:
            self.array.tambah_prioritas(p)
        return (p, durasi, traversals)

    def linklist_tambah_vip(self, p, sinkron=True):
        p.prioritas = 1
        t0 = time.perf_counter()
        self.linklist.tambah_vip(p)
        t1 = time.perf_counter()
        durasi = (t1 - t0) * 1000.0
        traversals = self.linklist.last_traversal_count
        if sinkron:
            self.array.tambah_vip(p)
        return (p, durasi, traversals)

    def linklist_hapus(self, i, sinkron=True):
        t0 = time.perf_counter()
        p = self.linklist.hapus_pesanan(i)
        t1 = time.perf_counter()
        durasi = (t1 - t0) * 1000.0
        traversals = self.linklist.last_traversal_count
        if sinkron and i < self.array.size:
            self.array.hapus_pesanan(i)
        return (p, durasi, traversals)
