# ==============================================================================
# PROYEK "2EZ4U APP" - STRUKTUR DATA & ANALISA ALGORITMA (EC234303)
# Unit Test: tests/test_m2.py
# Pengujian Unit Otomatis untuk Modul M2 (Stack, Kasir, Antrean Naif & Melingkar, Undo/Redo)
# Kepatuhan: 100% bebas fungsi/struktur instan bawaan
# ==============================================================================

import unittest
import os
import sys

# Tambahkan direktori root proyek ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.m1_pesanan import Pesanan
from backend.m2_antrean import (
    Stack,
    KasirPostfix,
    AntreanNaif,
    AntreanMelingkar,
    SistemAntreanM2,
    CatatanAksi
)


class TestStack(unittest.TestCase):
    """Pengujian Unit untuk Struktur Data Tumpukan (Stack LIFO)."""

    def test_stack_dasar(self):
        s = Stack(4)
        self.assertTrue(s.is_empty())
        self.assertEqual(len(s), 0)
        self.assertIsNone(s.peek())

        s.push(10)
        s.push(20)
        s.push(30)
        self.assertFalse(s.is_empty())
        self.assertEqual(len(s), 3)
        self.assertEqual(s.peek(), 30)

        self.assertEqual(s.pop(), 30)
        self.assertEqual(s.pop(), 20)
        self.assertEqual(len(s), 1)
        self.assertEqual(s.peek(), 10)
        self.assertEqual(s.pop(), 10)
        self.assertTrue(s.is_empty())

    def test_stack_underflow(self):
        s = Stack(2)
        with self.assertRaises(IndexError):
            s.pop()

    def test_stack_penggandaan_kapasitas(self):
        s = Stack(2)
        self.assertEqual(s.capacity, 2)
        s.push("A")
        s.push("B")
        self.assertEqual(s.capacity, 2)

        # Memicu alokasi 2x ke 4
        s.push("C")
        self.assertEqual(s.capacity, 4)
        self.assertEqual(len(s), 3)

        # Memicu alokasi 2x ke 8
        s.push("D")
        s.push("E")
        self.assertEqual(s.capacity, 8)
        self.assertEqual(len(s), 5)
        self.assertEqual(s.pop(), "E")
        self.assertEqual(s.pop(), "D")
        self.assertEqual(s.pop(), "C")

    def test_stack_clear(self):
        s = Stack(4)
        s.push(1)
        s.push(2)
        s.clear()
        self.assertTrue(s.is_empty())
        self.assertEqual(len(s), 0)
        self.assertIsNone(s.peek())


class TestKasirPostfix(unittest.TestCase):
    """Pengujian Unit untuk Mesin Kasir Postfix (Shunting-Yard & Evaluator)."""

    def test_pisah_token(self):
        # Angka berdigit banyak harus tetap utuh (12000, bukan 1 lalu 2)
        expr = "( 3 * 12000 ) + ( 2 * 8500 ) - 5000"
        tokens = KasirPostfix.pisah_token(expr)
        expected = ["(", "3", "*", "12000", ")", "+", "(", "2", "*", "8500", ")", "-", "5000"]
        self.assertEqual(tokens, expected)

    def test_ke_postfix_empat_ekspresi(self):
        # 1. Tanpa kurung
        t1, _ = KasirPostfix.ke_postfix("3 * 12000 + 2 * 8500 - 5000")
        self.assertEqual(t1, ["3", "12000", "*", "2", "8500", "*", "+", "5000", "-"])

        # 2. Berkurung (Contoh acuan PDF halaman 8)
        t2, steps2 = KasirPostfix.ke_postfix("( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
        self.assertEqual(t2, ["3", "12000", "*", "2", "8500", "*", "+", "5000", "-"])
        self.assertTrue(len(steps2) > 0)

        # 3. Ada tanda beruntun (Left-associative untuk -)
        t3, _ = KasirPostfix.ke_postfix("10000 - 2000 - 1000")
        self.assertEqual(t3, ["10000", "2000", "-", "1000", "-"])

        # 4. Kurung bersarang
        t4, _ = KasirPostfix.ke_postfix("( ( 2 + 3 ) * ( 10 - 4 ) ) / 5")
        self.assertEqual(t4, ["2", "3", "+", "10", "4", "-", "*", "5", "/"])

    def test_hitung_urutan_pop_minus_dan_pembagian(self):
        # Memastikan operand kanan diambil duluan: b = pop(), a = pop(), res = a - b
        # Uji pengurangan: 10000 - 2000 - 1000 = 7000
        t_minus, _ = KasirPostfix.ke_postfix("10000 - 2000 - 1000")
        hasil_minus, _ = KasirPostfix.hitung(t_minus)
        self.assertEqual(hasil_minus, 7000)

        # Uji pembagian: 100 / 4 / 5 = 5 (bukan 0 atau galat urutan)
        t_bagi, _ = KasirPostfix.ke_postfix("100 / 4 / 5")
        hasil_bagi, _ = KasirPostfix.hitung(t_bagi)
        self.assertEqual(hasil_bagi, 5)

        # Uji kurung bersarang: ((2 + 3) * (10 - 4)) / 5 = (5 * 6) / 5 = 6
        t_sarang, _ = KasirPostfix.ke_postfix("( ( 2 + 3 ) * ( 10 - 4 ) ) / 5")
        hasil_sarang, _ = KasirPostfix.hitung(t_sarang)
        self.assertEqual(hasil_sarang, 6)

    def test_hitung_total_struk_acuan_its(self):
        # Sesuai PDF: ( 3 * 12000 ) + ( 2 * 8500 ) - 5000 -> TOTAL Rp 48.000
        tokens, _ = KasirPostfix.ke_postfix("( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
        total, steps = KasirPostfix.hitung(tokens)
        self.assertEqual(total, 48000)
        self.assertTrue(len(steps) > 0)


class TestAntreanNaif(unittest.TestCase):
    """Pengujian Unit untuk Antrean Naif (Larik + pop(0) dengan pergeseran memori)."""

    def test_enqueue_dan_dequeue_dasar(self):
        q = AntreanNaif(4)
        self.assertTrue(q.is_empty())
        self.assertEqual(len(q), 0)

        q.enqueue("A")
        q.enqueue("B")
        q.enqueue("C")
        self.assertEqual(len(q), 3)
        self.assertEqual(q.peek(), "A")

        # Dequeue indeks 0: menggeser 2 elemen ("B", "C")
        out1 = q.dequeue()
        self.assertEqual(out1, "A")
        self.assertEqual(q.last_shift_count, 2)
        self.assertEqual(q.total_geseran, 2)
        self.assertEqual(len(q), 2)
        self.assertEqual(q.peek(), "B")

        # Dequeue kedua: menggeser 1 elemen ("C")
        out2 = q.dequeue()
        self.assertEqual(out2, "B")
        self.assertEqual(q.last_shift_count, 1)
        self.assertEqual(q.total_geseran, 3)

        out3 = q.dequeue()
        self.assertEqual(out3, "C")
        self.assertEqual(q.last_shift_count, 0)
        self.assertTrue(q.is_empty())

        # Dequeue saat kosong
        self.assertIsNone(q.dequeue())

    def test_dequeue_banyak_dan_get(self):
        q = AntreanNaif(8)
        for i in range(5):
            q.enqueue("item_%d" % i)

        self.assertEqual(q.get(0), "item_0")
        self.assertEqual(q.get(4), "item_4")
        self.assertIsNone(q.get(5))

        hasil, shifts = q.dequeue_banyak(3)
        self.assertEqual(len(hasil), 3)
        self.assertEqual(hasil[0], "item_0")
        self.assertEqual(hasil[1], "item_1")
        self.assertEqual(hasil[2], "item_2")
        self.assertEqual(len(q), 2)
        self.assertEqual(q.peek(), "item_3")


class TestAntreanMelingkar(unittest.TestCase):
    """Pengujian Unit untuk Antrean Melingkar (Circular Queue berpenunjuk front, rear, count)."""

    def test_circular_berputar_kapasitas_kecil(self):
        """
        Uji Paling Kritis M2 (Poin 6 Panduan):
        K=4: masukkan 3, keluarkan 2, masukkan 3 lagi.
        Pastikan penunjuk berputar (modulo K) dan datanya tetap benar sesuai urutan FIFO!
        """
        q = AntreanMelingkar(4)
        self.assertEqual(q.capacity, 4)
        self.assertEqual(q.front, 0)
        self.assertEqual(q.rear, 0)
        self.assertEqual(q.count, 0)

        # 1. Masukkan 3: 'A', 'B', 'C'
        q.enqueue("A")
        q.enqueue("B")
        q.enqueue("C")
        self.assertEqual(q.front, 0)
        self.assertEqual(q.rear, 3)
        self.assertEqual(q.count, 3)

        # 2. Keluarkan 2: 'A', 'B'
        x1 = q.dequeue()
        x2 = q.dequeue()
        self.assertEqual(x1, "A")
        self.assertEqual(x2, "B")
        self.assertEqual(q.front, 2)
        self.assertEqual(q.rear, 3)
        self.assertEqual(q.count, 1)

        # 3. Masukkan 3 lagi: 'D', 'E', 'F' -> Penunjuk rear berputar melingkari buffer!
        q.enqueue("D")  # rear jadi (3+1)%4 = 0
        self.assertEqual(q.rear, 0)
        q.enqueue("E")  # rear jadi (0+1)%4 = 1
        self.assertEqual(q.rear, 1)
        q.enqueue("F")  # rear jadi (1+1)%4 = 2 (sekarang count = 4, buffer penuh)
        self.assertEqual(q.rear, 2)
        self.assertEqual(q.front, 2)
        self.assertEqual(q.count, 4)

        # Periksa akses get(i) relatif terhadap front
        self.assertEqual(q.get(0), "C")
        self.assertEqual(q.get(1), "D")
        self.assertEqual(q.get(2), "E")
        self.assertEqual(q.get(3), "F")

        # 4. Keluarkan semua dan pastikan urutan FIFO tetap sempurna
        hasil = []
        while not q.is_empty():
            hasil.append(q.dequeue())
        self.assertEqual(hasil, ["C", "D", "E", "F"])
        self.assertTrue(q.is_empty())

    def test_circular_resize_saat_penuh(self):
        """Memastikan alokasi 2x menata ulang data dari urutan front melingkar ke linier baru."""
        q = AntreanMelingkar(4)
        q.enqueue("A")
        q.enqueue("B")
        q.enqueue("C")
        q.dequeue()
        q.dequeue()
        q.enqueue("D")
        q.enqueue("E")
        q.enqueue("F")
        self.assertEqual(q.capacity, 4)
        self.assertEqual(q.count, 4)

        # Enqueue ke-5 saat kapasitas 4 memicu penggandaan ke 8
        q.enqueue("G")
        self.assertEqual(q.capacity, 8)
        self.assertEqual(q.count, 5)
        self.assertEqual(q.front, 0)
        self.assertEqual(q.rear, 5)

        # Urutan FIFO tetap utuh
        hasil = []
        while not q.is_empty():
            hasil.append(q.dequeue())
        self.assertEqual(hasil, ["C", "D", "E", "F", "G"])

    def test_circular_0_geseran_elemen(self):
        """Memverifikasi bahwa Circular Queue tidak menggeser satu pun elemen memori."""
        q = AntreanMelingkar(10)
        for i in range(10):
            q.enqueue(i)

        for _ in range(5):
            q.dequeue()
            self.assertEqual(q.last_shift_count, 0)


class TestSistemAntreanM2(unittest.TestCase):
    """Pengujian Unit untuk Orkestrator SistemAntreanM2 (Undo/Redo & Integrasi)."""

    def setUp(self):
        self.sistem = SistemAntreanM2()

    def test_muat_csv_hanya_status_antre(self):
        csv_path = "data/pesanan.csv"
        if not os.path.exists(csv_path):
            self.skipTest("Berkas data/pesanan.csv tidak ditemukan")

        count, ms = self.sistem.muat_dari_csv(csv_path)
        # Sesuai spesifikasi, pesanan berstatus ANTRE berjumlah 19.850 baris
        self.assertEqual(count, 19850)
        self.assertEqual(len(self.sistem.antrean_naif), 19850)
        self.assertEqual(len(self.sistem.antrean_circular), 19850)
        self.assertEqual(self.sistem.antrean_circular.capacity, 32768)

    def test_enqueue_kedua_dan_undo_redo(self):
        p1 = Pesanan(self.sistem.generate_oid(), "Pelanggan 1", "resto", "menu", 10000, 3, 0)
        self.sistem.enqueue_kedua(p1)

        self.assertEqual(len(self.sistem.antrean_naif), 1)
        self.assertEqual(len(self.sistem.antrean_circular), 1)
        self.assertEqual(len(self.sistem.undo_stack), 1)
        self.assertEqual(len(self.sistem.redo_stack), 0)

        # 1. UNDO ENQUEUE: Pesanan dikeluarkan lagi dari belakang kedua antrean
        aksi_u, ms_u, pesan_u = self.sistem.undo_last()
        self.assertEqual(aksi_u.tipe, "ENQUEUE")
        self.assertEqual(len(self.sistem.antrean_naif), 0)
        self.assertEqual(len(self.sistem.antrean_circular), 0)
        self.assertEqual(len(self.sistem.undo_stack), 0)
        self.assertEqual(len(self.sistem.redo_stack), 1)

        # 2. REDO ENQUEUE: Pesanan dimasukkan kembali ke belakang kedua antrean
        aksi_r, ms_r, pesan_r = self.sistem.redo_last()
        self.assertEqual(aksi_r.tipe, "ENQUEUE")
        self.assertEqual(len(self.sistem.antrean_naif), 1)
        self.assertEqual(len(self.sistem.antrean_circular), 1)
        self.assertEqual(len(self.sistem.undo_stack), 1)
        self.assertEqual(len(self.sistem.redo_stack), 0)

    def test_aksi_baru_mengosongkan_redo(self):
        # Aksi baru apa pun wajib mengosongkan tumpukan Redo (Poin 8 & Halaman 9)
        p1 = Pesanan(self.sistem.generate_oid(), "P1", "resto", "menu", 10000, 3, 0)
        self.sistem.enqueue_kedua(p1)
        self.sistem.undo_last()
        self.assertEqual(len(self.sistem.redo_stack), 1)

        # Aksi baru dilakukan
        p2 = Pesanan(self.sistem.generate_oid(), "P2", "resto", "menu", 20000, 3, 0)
        self.sistem.enqueue_kedua(p2)
        self.assertEqual(len(self.sistem.redo_stack), 0)

        # Mencoba redo saat tumpukan kosong
        aksi_r, _, pesan_r = self.sistem.redo_last()
        self.assertIsNone(aksi_r)
        self.assertIn("kosong", pesan_r)

    def test_dequeue_circular_dan_undo_redo(self):
        # Masukkan 3 pesanan
        for i in range(3):
            p = Pesanan("O-%03d" % i, "Pelanggan %d" % i, "resto", "menu", 10000, 3, 0)
            self.sistem.enqueue_kedua(p)
        self.sistem.undo_stack.clear()

        # Dequeue 2 pesanan dari circular
        hasil, shifts, ms = self.sistem.dequeue_circular(2, catat_undo=True)
        self.assertEqual(len(hasil), 2)
        self.assertEqual(shifts, 0)
        self.assertEqual(len(self.sistem.antrean_circular), 1)
        self.assertEqual(len(self.sistem.undo_stack), 1)

        # Undo dequeue: Mengembalikan seluruh pesanan ke DEPAN antrean circular dalam urutan yang benar
        aksi_u, ms_u, pesan_u = self.sistem.undo_last()
        self.assertEqual(aksi_u.tipe, "DEQUEUE")
        self.assertEqual(len(self.sistem.antrean_circular), 3)
        self.assertEqual(self.sistem.antrean_circular.peek().oid, "O-000")
        self.assertEqual(self.sistem.antrean_circular.get(1).oid, "O-001")
        self.assertEqual(self.sistem.antrean_circular.get(2).oid, "O-002")

        # Redo dequeue: Mengeluarkan kembali 2 pesanan dari depan antrean circular
        aksi_r, ms_r, pesan_r = self.sistem.redo_last()
        self.assertEqual(aksi_r.tipe, "DEQUEUE")
        self.assertEqual(len(self.sistem.antrean_circular), 1)
        self.assertEqual(self.sistem.antrean_circular.peek().oid, "O-002")

    def test_perbandingan_pergeseran_naif_vs_circular(self):
        # Menguji bahwa naive menggeser elemen sedangkan circular menggeser 0
        for i in range(100):
            p = Pesanan("O-%03d" % i, "P", "resto", "menu", 1000, 3, 0)
            self.sistem.enqueue_kedua(p)

        # Dequeue 10 pada naive
        hasil_n, shifts_n, _ = self.sistem.dequeue_naif(10)
        self.assertEqual(len(hasil_n), 10)
        self.assertTrue(shifts_n > 0)

        # Dequeue 10 pada circular
        hasil_c, shifts_c, _ = self.sistem.dequeue_circular(10, catat_undo=False)
        self.assertEqual(len(hasil_c), 10)
        self.assertEqual(shifts_c, 0)

    def test_stats_method(self):
        stats = self.sistem.stats()
        self.assertEqual(len(stats), 6)
        # (len_naif, len_circ, capacity_circ, total_geseran_naif, undo_depth, redo_depth)
        self.assertEqual(stats[0], 0)
        self.assertEqual(stats[1], 0)
        self.assertEqual(stats[3], 0)
        self.assertEqual(stats[4], 0)
        self.assertEqual(stats[5], 0)


if __name__ == "__main__":
    unittest.main()
