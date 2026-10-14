# ==============================================================================
# PROYEK "2EZ4U APP" - STRUKTUR DATA & ANALISA ALGORITMA (EC234303)
# Unit Test: tests/test_m3.py
# Pengujian Unit Otomatis untuk Modul M3 (Sort & Search)
# Kepatuhan: Sesuai Checklist Resmi Halaman 21-22 PDF Panduan Dosen ITS
# ==============================================================================

import unittest
import os
import sys

# Tambahkan direktori root proyek ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.m1_pesanan import Pesanan
from backend.m3_laporan import (
    ambil_kunci,
    insertion_sort,
    merge_sort,
    linear_search,
    binary_search,
    SistemLaporanM3
)


class TestM3SortAndSearch(unittest.TestCase):
    """Pengujian Unit Menyeluruh untuk Algoritma Pengurutan dan Pencarian M3."""

    def test_keempat_algoritma_dan_pelaporan_perbandingan(self):
        """Checklist 1: Keempat algoritma ada, dan masing-masing melaporkan jumlah perbandingannya."""
        data_angka = [50, 20, 80, 10, 30]

        # 1. Insertion Sort
        larik_ins = list(data_angka)
        res_ins, c_ins, m_ins, t_ins, err_ins = insertion_sort(larik_ins)
        self.assertIsNone(err_ins)
        self.assertEqual(res_ins, [10, 20, 30, 50, 80])
        self.assertTrue(c_ins > 0)
        self.assertTrue(m_ins > 0)

        # 2. Merge Sort
        larik_merge = list(data_angka)
        res_merge, c_merge, m_merge, t_merge = merge_sort(larik_merge)
        self.assertEqual(res_merge, [10, 20, 30, 50, 80])
        self.assertTrue(c_merge > 0)
        self.assertTrue(m_merge > 0)

        # 3. Linear Search
        idx_lin, c_lin, t_lin, item_lin = linear_search(res_merge, 30)
        self.assertEqual(idx_lin, 2)
        self.assertEqual(item_lin, 30)
        self.assertEqual(c_lin, 3)  # Memeriksa indeks 0 (10), 1 (20), 2 (30) -> 3 perbandingan

        # 4. Binary Search
        idx_bin, c_bin, t_bin, item_bin = binary_search(res_merge, 30)
        self.assertEqual(idx_bin, 2)
        self.assertEqual(item_bin, 30)
        self.assertTrue(c_bin > 0)

    def test_kestabilan_kedua_sort_dan_hasil_identik(self):
        """
        Checklist 2: Kedua sort terbukti stabil, dan hasilnya identik baris per baris pada data yang sama.
        Dua data dengan kunci sama (misal harga 11.000) harus tetap mempertahankan urutan asalnya.
        """
        p1 = Pesanan("O-000002", "Cici", "resto", "bubur", 11000, 3, 1000)
        p2 = Pesanan("O-000009", "Dina", "resto", "mie", 11000, 3, 2000)
        p3 = Pesanan("O-000001", "Andi", "resto", "nasi", 15000, 3, 3000)
        p4 = Pesanan("O-000005", "Budi", "resto", "soto", 20000, 3, 4000)
        p5 = Pesanan("O-000003", "Eka", "resto", "es", 11000, 3, 5000)

        daftar_asli = [p4, p1, p3, p2, p5]

        # Uji Insertion Sort
        larik_ins = list(daftar_asli)
        res_ins, _, _, _, _ = insertion_sort(larik_ins, kunci="harga")
        # Ketiga pesanan berharga 11000 wajib muncul dengan urutan asal: p1 -> p2 -> p5
        self.assertEqual(res_ins[0].oid, "O-000002")
        self.assertEqual(res_ins[1].oid, "O-000009")
        self.assertEqual(res_ins[2].oid, "O-000003")
        self.assertEqual(res_ins[3].oid, "O-000001")
        self.assertEqual(res_ins[4].oid, "O-000005")

        # Uji Merge Sort
        larik_merge = list(daftar_asli)
        res_merge, _, _, _ = merge_sort(larik_merge, kunci="harga")
        self.assertEqual(res_merge[0].oid, "O-000002")
        self.assertEqual(res_merge[1].oid, "O-000009")
        self.assertEqual(res_merge[2].oid, "O-000003")
        self.assertEqual(res_merge[3].oid, "O-000001")
        self.assertEqual(res_merge[4].oid, "O-000005")

        # Hasil kedua sort wajib IDENTIK baris per baris
        for i in range(len(daftar_asli)):
            self.assertEqual(res_ins[i].oid, res_merge[i].oid)
            self.assertEqual(res_ins[i].harga, res_merge[i].harga)

    def test_merge_sort_acak_terurut_terbalik_duplikat(self):
        """Checklist 3: Merge sort benar pada data acak, terurut, terbalik, dan berisi duplikat."""
        # 1. Data Acak
        acak = [45, 12, 89, 3, 77, 21, 60]
        res_acak, _, _, _ = merge_sort(list(acak))
        self.assertEqual(res_acak, [3, 12, 21, 45, 60, 77, 89])

        # 2. Data Sudah Terurut
        terurut = [1, 2, 3, 4, 5, 6, 7]
        res_terurut, _, _, _ = merge_sort(list(terurut))
        self.assertEqual(res_terurut, [1, 2, 3, 4, 5, 6, 7])

        # 3. Data Terbalik (Reverse)
        terbalik = [90, 80, 70, 60, 50, 40]
        res_terbalik, _, _, _ = merge_sort(list(terbalik))
        self.assertEqual(res_terbalik, [40, 50, 60, 70, 80, 90])

        # 4. Data Berisi Banyak Duplikat
        duplikat = [5, 2, 5, 1, 2, 5, 3, 1, 5]
        res_duplikat, _, _, _ = merge_sort(list(duplikat))
        self.assertEqual(res_duplikat, [1, 1, 2, 2, 3, 5, 5, 5, 5])

    def test_binary_search_empat_kasus_dan_larik_kosong(self):
        """
        Checklist 4: Binary search benar pada empat kasus:
        - target di tengah
        - target di kiri (elemen pertama)
        - target di kanan (elemen terakhir)
        - target tidak ada
        + kasus larik kosong
        """
        larik = [10, 25, 33, 48, 59, 72, 84, 91]

        # 1. Target di Tengah (misal 48 atau 59)
        idx, comps, _, item = binary_search(larik, 48)
        self.assertEqual(idx, 3)
        self.assertEqual(item, 48)

        # 2. Target di Ujung Kiri (elemen pertama: 10)
        idx_kiri, comps_kiri, _, item_kiri = binary_search(larik, 10)
        self.assertEqual(idx_kiri, 0)
        self.assertEqual(item_kiri, 10)

        # 3. Target di Ujung Kanan (elemen terakhir: 91)
        idx_kanan, comps_kanan, _, item_kanan = binary_search(larik, 91)
        self.assertEqual(idx_kanan, 7)
        self.assertEqual(item_kanan, 91)

        # 4. Target Tidak Ada (misal 50)
        idx_none, comps_none, _, item_none = binary_search(larik, 50)
        self.assertEqual(idx_none, -1)
        self.assertIsNone(item_none)
        self.assertTrue(comps_none > 0)

        # 5. Kasus Larik Kosong
        idx_empty, comps_empty, _, item_empty = binary_search([], 100)
        self.assertEqual(idx_empty, -1)
        self.assertIsNone(item_empty)
        self.assertEqual(comps_empty, 0)

    def test_insertion_sort_penolakan_data_terlalu_besar(self):
        """Checklist 5: Menu insertion sort menolak data terlalu besar dengan pesan, bukan membeku."""
        # Buat larik dengan 20.001 elemen dummy
        data_besar = [i for i in range(20001)]
        res, comps, moves, ms, err = insertion_sort(data_besar)
        self.assertIsNotNone(err)
        self.assertIn("DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh", err)
        self.assertEqual(comps, 0)
        self.assertEqual(moves, 0)

    def test_pola_perbandingan_n_dilipatduakan(self):
        """
        Checklist 6: Begitu n dilipatduakan, perbandingan insertion sort menjadi kira-kira 4x,
        sedangkan merge sort hanya sekitar 2x.
        Uji coba sesuai angka acuan ITS: n=2000 dan n=4000 dari data/pesanan.csv jika ada.
        """
        csv_path = "data/pesanan.csv"
        if not os.path.exists(csv_path):
            self.skipTest("Berkas data/pesanan.csv tidak ditemukan")

        sistem = SistemLaporanM3()
        sistem.muat_dari_csv(csv_path)

        # 1. Insertion Sort n=2000 vs n=4000
        _, c_ins_2k, _, _, _ = sistem.jalankan_sort(n=2000, kunci="harga", algoritma="insertion")
        _, c_ins_4k, _, _, _ = sistem.jalankan_sort(n=4000, kunci="harga", algoritma="insertion")

        # Perbandingan insertion sort: 962.430 dan 3.831.520 (rasio ~3.98x mendekati 4x)
        self.assertEqual(c_ins_2k, 962430)
        self.assertEqual(c_ins_4k, 3831520)
        rasio_ins = c_ins_4k / c_ins_2k
        self.assertTrue(3.8 <= rasio_ins <= 4.2)

        # 2. Merge Sort n=2000 vs n=4000
        _, c_merge_2k, _, _, _ = sistem.jalankan_sort(n=2000, kunci="harga", algoritma="merge")
        _, c_merge_4k, _, _, _ = sistem.jalankan_sort(n=4000, kunci="harga", algoritma="merge")

        # Perbandingan merge sort: 19.240 dan 42.355 (rasio ~2.2x mendekati 2x)
        self.assertEqual(c_merge_2k, 19240)
        self.assertEqual(c_merge_4k, 42355)
        rasio_merge = c_merge_4k / c_merge_2k
        self.assertTrue(2.0 <= rasio_merge <= 2.5)

    def test_linear_vs_binary_search_pada_dataset_penuh(self):
        """
        Checklist 7: Linear search memakai belasan ribu kali lebih banyak perbandingan
        daripada binary search pada data yang sama (misal O-199999).
        """
        csv_path = "data/pesanan.csv"
        if not os.path.exists(csv_path):
            self.skipTest("Berkas data/pesanan.csv tidak ditemukan")

        sistem = SistemLaporanM3()
        sistem.muat_dari_csv(csv_path)

        # Linear Search O-199999
        idx_lin, c_lin, t_lin, item_lin = sistem.jalankan_linear_search("O-199999")
        self.assertEqual(idx_lin, 199998)
        self.assertEqual(c_lin, 199999)
        self.assertIsNotNone(item_lin)

        # Binary Search O-199999
        idx_bin, c_bin, t_bin, item_bin, build_ms, baru = sistem.jalankan_binary_search("O-199999")
        self.assertEqual(idx_bin, 199998)
        self.assertEqual(c_bin, 17)
        self.assertIsNotNone(item_bin)

        # Selisih perbandingan: 199.999 vs 17 (Linear > 11.000 kali lebih banyak perbandingan)
        self.assertTrue(c_lin > 10000 * c_bin)

    def test_eksekusi_perintah_command_line(self):
        """Pengujian interpreter perintah teks untuk COMMAND panel."""
        csv_path = "data/pesanan.csv"
        if not os.path.exists(csv_path):
            self.skipTest("Berkas data/pesanan.csv tidak ditemukan")

        sistem = SistemLaporanM3()
        sistem.muat_dari_csv(csv_path)

        # 1. insertion_sort n=2000
        out_ins = sistem.eksekusi_perintah("insertion_sort jumlah=2000 kunci=harga")
        self.assertIn("2.000 pesanan terurut", out_ins)
        self.assertIn("962.430 perbandingan", out_ins)
        self.assertIn("[M3 - insertion sort]", out_ins)

        # 2. merge_sort n=2000
        out_merge = sistem.eksekusi_perintah("merge_sort jumlah=2000 kunci=harga")
        self.assertIn("2.000 pesanan terurut", out_merge)
        self.assertIn("19.240 perbandingan", out_merge)
        self.assertIn("[M3 - merge sort]", out_merge)

        # 3. insertion_sort penolakan
        out_tolak = sistem.eksekusi_perintah("insertion_sort jumlah=200000")
        self.assertEqual(out_tolak, "DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh")

        # 4. linear_search O-199999
        out_lin = sistem.eksekusi_perintah("linear_search O-199999")
        self.assertIn("ditemukan di indeks 199.998", out_lin)
        self.assertIn("199.999 perbandingan", out_lin)

        # 5. binary_search O-199999
        out_bin = sistem.eksekusi_perintah("binary_search O-199999")
        self.assertIn("ditemukan di baris 199.999", out_bin)
        self.assertIn("17 perbandingan", out_bin)


if __name__ == "__main__":
    unittest.main()
