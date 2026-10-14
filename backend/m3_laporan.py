# ==============================================================================
# PROYEK "2EZ4U APP" - STRUKTUR DATA & ANALISA ALGORITMA (EC234303)
# Modul: backend/m3_laporan.py
# Milestone 3: Pengurutan & Pencarian (Sort & Search)
# - Insertion Sort O(n^2) In-Place & Stabil
# - Merge Sort O(n log n) Stabil & Skala Penuh (200.000 data)
# - Linear Search O(n) Telusur Sekuensial
# - Binary Search O(log n) Pencarian Biner Terurut
# Kepatuhan: 100% Bebas Fungsi/Struktur Instan Bawaan (Bebas dict, set, sorted, dsb.)
# ==============================================================================

import time
import csv
from backend.m1_pesanan import Pesanan


def ambil_kunci(item, kunci="oid"):
    """
    Mengekstrak nilai kunci dari suatu objek pesanan, tuple, atau tipe data primitif.
    Dilarang menggunakan dict bawaan.
    """
    if item is None:
        return None
    if isinstance(item, (int, float, str)):
        return item
    if kunci is None:
        return item
    if callable(kunci):
        return kunci(item)
    if isinstance(item, (list, tuple)):
        if isinstance(kunci, int):
            return item[kunci]
        return item[0]

    # Objek Pesanan
    if kunci == "harga":
        return item.harga
    if kunci == "oid":
        return item.oid
    if kunci == "selesai" or kunci == "t_selesai_detik":
        return item.t_selesai_detik if item.t_selesai_detik is not None else 999999999
    if kunci == "masuk" or kunci == "t_masuk_detik":
        return item.t_masuk_detik
    if kunci == "prioritas":
        return item.prioritas
    if kunci == "pelanggan":
        return item.pelanggan
    if kunci == "resto":
        return item.resto
    if kunci == "menu":
        return item.menu
    if kunci == "status":
        return item.status

    if hasattr(item, kunci):
        val = getattr(item, kunci)
        if kunci in ("selesai", "t_selesai_detik") and val is None:
            return 999999999
        return val

    return item


def insertion_sort(larik, kunci="harga"):
    """
    Algoritma Insertion Sort:
    - Bekerja di tempat (in-place) dan stabil.
    - Kompleksitas Waktu: O(n^2) terburuk/rata-rata, O(n) terbaik (data hampir terurut).
    - Stabil: syarat perbandingan memakai '>' (BUKAN '>=').
    - Batas keamanan: Menolak data > 20.000 baris dengan pesan penolakan resmi.
    
    Mengembalikan tuple: (larik_terurut, jumlah_perbandingan, jumlah_pemindahan, durasi_ms)
    """
    n = len(larik)
    if n > 20000:
        pesan_tolak = "DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh"
        return larik, 0, 0, 0.0, pesan_tolak

    comps = 0
    moves = 0
    t0 = time.perf_counter()

    for i in range(1, n):
        key_item = larik[i]
        key_val = ambil_kunci(key_item, kunci)
        j = i - 1
        while j >= 0:
            comps += 1
            if ambil_kunci(larik[j], kunci) > key_val:
                larik[j + 1] = larik[j]
                moves += 1
                j -= 1
            else:
                break
        larik[j + 1] = key_item
        moves += 1

    durasi_ms = (time.perf_counter() - t0) * 1000.0
    return larik, comps, moves, durasi_ms, None


def merge_sort(larik, kunci="oid"):
    """
    Algoritma Merge Sort:
    - Membelah data menjadi dua bagian rekursif hingga basis len <= 1,
      lalu menggabungkan (merge) dua bagian terurut.
    - Kompleksitas Waktu: O(n log n) di semua kasus.
    - Stabil: syarat perbandingan memakai '<=' agar elemen dari bagian kiri
      didahulukan saat kuncinya sama.
    - Sanggup mengurutkan seluruh 200.000 data.
    
    Mengembalikan tuple: (larik_terurut, jumlah_perbandingan, jumlah_pemindahan, durasi_ms)
    """
    comps = 0
    moves = 0
    t0 = time.perf_counter()

    def _rekursif(sub):
        nonlocal comps, moves
        m_len = len(sub)
        if m_len <= 1:
            return sub

        mid = m_len // 2
        left = _rekursif(sub[:mid])
        right = _rekursif(sub[mid:])

        merged = [None] * m_len
        i = 0
        j = 0
        k = 0
        n_l = len(left)
        n_r = len(right)

        while i < n_l and j < n_r:
            comps += 1
            if ambil_kunci(left[i], kunci) <= ambil_kunci(right[j], kunci):
                merged[k] = left[i]
                moves += 1
                i += 1
            else:
                merged[k] = right[j]
                moves += 1
                j += 1
            k += 1

        while i < n_l:
            merged[k] = left[i]
            moves += 1
            i += 1
            k += 1

        while j < n_r:
            merged[k] = right[j]
            moves += 1
            j += 1
            k += 1

        return merged

    hasil = _rekursif(larik)

    # Sinkronkan kembali ke larik masukan in-place jika memungkinkan
    try:
        for idx in range(len(larik)):
            larik[idx] = hasil[idx]
    except Exception:
        pass

    durasi_ms = (time.perf_counter() - t0) * 1000.0
    return hasil, comps, moves, durasi_ms


def linear_search(larik, target, kunci="oid"):
    """
    Algoritma Linear Search:
    - Menelusuri elemen satu per satu dari awal larik.
    - Berhenti begitu elemen target ditemukan.
    - Kompleksitas Waktu: O(n).
    
    Mengembalikan tuple: (indeks_ditemukan, jumlah_perbandingan, durasi_ms, pesanan_ditemukan)
    Jika tidak ditemukan, indeks_ditemukan bernilai -1 dan pesanan_ditemukan bernilai None.
    """
    comps = 0
    t0 = time.perf_counter()
    n = len(larik)
    found_idx = -1
    found_item = None

    for i in range(n):
        comps += 1
        if ambil_kunci(larik[i], kunci) == target:
            found_idx = i
            found_item = larik[i]
            break

    durasi_ms = (time.perf_counter() - t0) * 1000.0
    return found_idx, comps, durasi_ms, found_item


def binary_search(larik, target, kunci="oid"):
    """
    Algoritma Binary Search:
    - Membagi interval pencarian menjadi separuh pada setiap langkah.
    - Menuntut larik telah terurut berdasarkan kunci pencarian.
    - Kompleksitas Waktu: O(log n).
    
    Mengembalikan tuple: (indeks_ditemukan, jumlah_perbandingan, durasi_ms, pesanan_ditemukan)
    Jika tidak ditemukan, indeks_ditemukan bernilai -1 dan pesanan_ditemukan bernilai None.
    """
    comps = 0
    t0 = time.perf_counter()
    lo = 0
    hi = len(larik) - 1
    found_idx = -1
    found_item = None

    while lo <= hi:
        mid = (lo + hi) // 2
        comps += 1
        mid_val = ambil_kunci(larik[mid], kunci)
        if mid_val == target:
            found_idx = mid
            found_item = larik[mid]
            break
        elif mid_val < target:
            lo = mid + 1
        else:
            hi = mid - 1

    durasi_ms = (time.perf_counter() - t0) * 1000.0
    return found_idx, comps, durasi_ms, found_item


class SistemLaporanM3:
    """
    Orkestrator Milestone 3 (M3): Sort & Search.
    Menangani:
    - Laporan Harian (pesanan terurut menurut waktu selesai/harga/oid)
    - Pengurutan data (Insertion Sort vs Merge Sort)
    - Pencarian data cepat (Linear Search vs Binary Search)
    - Penyimpanan Cache Larik Terurut OID untuk Binary Search
    - Interpreter Konsol Perintah Sesuai Panduan Dosen ITS
    """
    __slots__ = (
        'daftar_pesanan',
        'laporan_terurut',
        'kunci_laporan_aktif',
        'algoritma_laporan_aktif',
        'oid_sorted_cache',
        'oid_cache_build_ms',
        'last_sort_info',
        'last_search_info'
    )

    def __init__(self):
        self.daftar_pesanan = []
        self.laporan_terurut = []
        self.kunci_laporan_aktif = "selesai"
        self.algoritma_laporan_aktif = "merge"
        self.oid_sorted_cache = None
        self.oid_cache_build_ms = 0.0
        self.last_sort_info = None
        self.last_search_info = None

    def sinkronkan_dari_m1(self, sistem_m1):
        """Menyalin referensi pesanan dari SistemPesananM1."""
        if sistem_m1 and hasattr(sistem_m1, 'array'):
            arr = sistem_m1.array
            n = arr.size
            self.daftar_pesanan = [None] * n
            for i in range(n):
                self.daftar_pesanan[i] = arr.get(i)
        self.oid_sorted_cache = None
        self.oid_cache_build_ms = 0.0

    def muat_dari_csv(self, path_csv="data/pesanan.csv"):
        """Memuat data pesanan langsung dari berkas CSV."""
        daftar = []
        with open(path_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) >= 9:
                    p = Pesanan(
                        oid=row[0],
                        pelanggan=row[1],
                        resto=row[2],
                        menu=row[3],
                        harga=row[4],
                        prioritas=row[5],
                        t_masuk_detik=row[6],
                        t_selesai_detik=row[7],
                        status=row[8]
                    )
                    daftar.append(p)
        self.daftar_pesanan = daftar
        self.oid_sorted_cache = None
        self.oid_cache_build_ms = 0.0
        return len(daftar)

    def pastikan_oid_cache(self):
        """
        Membangun cache larik terurut menurut oid menggunakan merge sort.
        Diperlukan agar binary search dapat beroperasi sah dan tepat.
        """
        if self.oid_sorted_cache is not None:
            return self.oid_sorted_cache, 0.0, False

        salinan = list(self.daftar_pesanan)
        t0 = time.perf_counter()
        hasil, comps, moves, ms = merge_sort(salinan, kunci="oid")
        self.oid_cache_build_ms = ms
        self.oid_sorted_cache = hasil
        return self.oid_sorted_cache, ms, True

    def buat_laporan_harian(self, kunci="selesai", algoritma="merge"):
        """
        Menyusun laporan harian pesanan terurut.
        Secara default mengurutkan berdasarkan waktu selesai (t_selesai_detik).
        """
        if not self.daftar_pesanan:
            return [], 0, 0, 0.0, None

        # Filter pesanan yang relevan untuk laporan harian (status DONE atau seluruh data)
        salinan = list(self.daftar_pesanan)
        self.kunci_laporan_aktif = kunci
        self.algoritma_laporan_aktif = algoritma

        if algoritma == "insertion":
            hasil, comps, moves, ms, err = insertion_sort(salinan, kunci=kunci)
            if err:
                return [], 0, 0, 0.0, err
        else:
            hasil, comps, moves, ms = merge_sort(salinan, kunci=kunci)
            err = None

        self.laporan_terurut = hasil
        self.last_sort_info = (algoritma, len(salinan), kunci, comps, moves, ms)
        return hasil, comps, moves, ms, err

    def jalankan_sort(self, n=2000, kunci="harga", algoritma="merge"):
        """
        Menjalankan pengurutan pada n elemen pertama dari daftar pesanan.
        """
        if not self.daftar_pesanan:
            return [], 0, 0, 0.0, "Data pesanan belum dimuat."

        total_ada = len(self.daftar_pesanan)
        n_ambil = min(n, total_ada) if n is not None and n > 0 else total_ada
        sub_data = [self.daftar_pesanan[i] for i in range(n_ambil)]

        if algoritma == "insertion":
            hasil, comps, moves, ms, err = insertion_sort(sub_data, kunci=kunci)
            if err:
                return sub_data, 0, 0, 0.0, err
        else:
            hasil, comps, moves, ms = merge_sort(sub_data, kunci=kunci)
            err = None

        self.last_sort_info = (algoritma, n_ambil, kunci, comps, moves, ms)
        return hasil, comps, moves, ms, None

    def jalankan_linear_search(self, target_oid):
        """Pencarian target_oid menggunakan Linear Search."""
        if not self.daftar_pesanan:
            return -1, 0, 0.0, None

        idx, comps, ms, item = linear_search(self.daftar_pesanan, target_oid, kunci="oid")
        self.last_search_info = ("linear", target_oid, idx, comps, ms)
        return idx, comps, ms, item

    def jalankan_binary_search(self, target_oid):
        """
        Pencarian target_oid menggunakan Binary Search.
        Jika cache terurut belum ada, dibangun sekali dengan merge sort.
        """
        if not self.daftar_pesanan:
            return -1, 0, 0.0, None, 0.0, False

        larik_terurut, build_ms, baru_dibangun = self.pastikan_oid_cache()
        idx, comps, ms, item = binary_search(larik_terurut, target_oid, kunci="oid")
        self.last_search_info = ("binary", target_oid, idx, comps, ms)
        return idx, comps, ms, item, build_ms, baru_dibangun

    def eksekusi_perintah(self, cmd_line):
        """
        Mengeksekusi perintah teks dari COMMAND panel persis seperti contoh PDF ITS:
        > insertion_sort jumlah=2000 kunci=harga
        > merge_sort jumlah=2000 kunci=harga
        > linear_search O-199999
        > binary_search O-199999
        """
        baris = cmd_line.strip()
        if not baris:
            return ""

        parts = baris.split()
        cmd = parts[0].lower()

        # 1. insertion_sort
        if cmd == "insertion_sort":
            jumlah = 2000
            kunci = "harga"
            for p in parts[1:]:
                if p.startswith("jumlah="):
                    try:
                        jumlah = int(p.split("=")[1])
                    except ValueError:
                        pass
                elif p.startswith("kunci="):
                    kunci = p.split("=")[1]

            if jumlah > 20000:
                return "DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh"

            hasil, comps, moves, ms, err = self.jalankan_sort(n=jumlah, kunci=kunci, algoritma="insertion")
            if err:
                return err

            jumlah_str = "{:,}".format(len(hasil)).replace(",", ".")
            comps_str = "{:,}".format(comps).replace(",", ".")
            return "%s pesanan terurut | %s perbandingan [M3 - insertion sort] %.2f ms" % (
                jumlah_str, comps_str, ms
            )

        # 2. merge_sort
        if cmd == "merge_sort":
            jumlah = 2000
            kunci = "harga"
            for p in parts[1:]:
                if p.startswith("jumlah="):
                    try:
                        jumlah = int(p.split("=")[1])
                    except ValueError:
                        pass
                elif p.startswith("kunci="):
                    kunci = p.split("=")[1]

            hasil, comps, moves, ms, err = self.jalankan_sort(n=jumlah, kunci=kunci, algoritma="merge")
            if err:
                return err

            jumlah_str = "{:,}".format(len(hasil)).replace(",", ".")
            comps_str = "{:,}".format(comps).replace(",", ".")
            if ms >= 1000.0:
                waktu_str = "%.2f s" % (ms / 1000.0)
            else:
                waktu_str = "%.2f ms" % ms
            return "%s pesanan terurut | %s perbandingan [M3 - merge sort] %s" % (
                jumlah_str, comps_str, waktu_str
            )

        # 3. linear_search
        if cmd == "linear_search":
            if len(parts) < 2:
                return "Galat: format perintah 'linear_search <TARGET_OID>'"
            target = parts[1]
            idx, comps, ms, item = self.jalankan_linear_search(target)
            comps_str = "{:,}".format(comps).replace(",", ".")
            if idx >= 0:
                idx_str = "{:,}".format(idx).replace(",", ".")
                return "ditemukan di indeks %s | %s perbandingan [M3 - linear] %.2f ms" % (
                    idx_str, comps_str, ms
                )
            else:
                return "tidak ditemukan | %s perbandingan [M3 - linear] %.2f ms" % (
                    comps_str, ms
                )

        # 4. binary_search
        if cmd == "binary_search":
            if len(parts) < 2:
                return "Galat: format perintah 'binary_search <TARGET_OID>'"
            target = parts[1]
            idx, comps, ms, item, build_ms, baru = self.jalankan_binary_search(target)
            baris_keluaran = []
            if baru:
                baris_keluaran.append("daftar terurut oid dibangun sekali (merge sort) %.2f ms" % build_ms)
            if idx >= 0:
                baris_str = "{:,}".format(idx + 1).replace(",", ".")
                baris_keluaran.append("ditemukan di baris %s | %d perbandingan [M3 - binary] %.2f ms" % (
                    baris_str, comps, ms
                ))
            else:
                baris_keluaran.append("tidak ditemukan | %d perbandingan [M3 - binary] %.2f ms" % (
                    comps, ms
                ))
            return "\n".join(baris_keluaran)

        return "Perintah tidak dikenal: %s" % cmd
