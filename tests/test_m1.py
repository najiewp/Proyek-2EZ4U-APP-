# ==============================================================================
# Unit Test: tests/test_m1.py
# Pengujian Unit untuk Modul M1 (Array vs LinkList)
# ==============================================================================

import unittest
import os
import sys

# Tambahkan direktori root ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.m1_pesanan import Pesanan, Array, LinkList, SistemPesananM1


class TestM1StrukturData(unittest.TestCase):

    def test_pesanan_model(self):
        p = Pesanan("O-000001", "Budi", "resto-a", "nasi-goreng", 15000, 3, 3600, 7200, "DONE")
        self.assertEqual(p.oid, "O-000001")
        self.assertEqual(p.pelanggan, "Budi")
        self.assertEqual(p.harga, 15000)
        self.assertEqual(p.format_t_masuk(), "01:00:00")
        self.assertEqual(p.format_t_selesai(), "02:00:00")
        self.assertEqual(p.format_harga(), "15.000")

    def test_array_dasar_dan_penggandaan(self):
        arr = Array(initial_capacity=2)
        self.assertEqual(arr.capacity, 2)
        self.assertEqual(len(arr), 0)

        # Append memicu resize
        arr.append("A")
        arr.append("B")
        self.assertEqual(arr.capacity, 2)
        self.assertEqual(len(arr), 2)

        arr.append("C")  # Memicu resize ke 4
        self.assertEqual(arr.capacity, 4)
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr.get(0), "A")
        self.assertEqual(arr.get(1), "B")
        self.assertEqual(arr.get(2), "C")

    def test_array_operasi_bisnis(self):
        arr = Array(4)
        p_reg = Pesanan("O-1", "Reguler", "resto", "menu", 10000, 3, 0)
        p_prio = Pesanan("O-2", "Prioritas", "resto", "menu", 10000, 2, 0)
        p_vip = Pesanan("O-3", "VIP", "resto", "menu", 10000, 1, 0)

        # 1. Tambah Reguler (ke belakang)
        arr.tambah_reguler(p_reg)
        self.assertEqual(len(arr), 1)
        self.assertEqual(arr.get(0).oid, "O-1")

        # 2. Tambah Prioritas (ke tengah: indeks 1 // 2 = 0)
        arr.tambah_prioritas(p_prio)
        self.assertEqual(len(arr), 2)
        self.assertEqual(arr.get(0).oid, "O-2")
        self.assertEqual(arr.get(1).oid, "O-1")

        # 3. Tambah VIP (ke indeks 0)
        arr.tambah_vip(p_vip)
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr.get(0).oid, "O-3")
        self.assertEqual(arr.get(1).oid, "O-2")
        self.assertEqual(arr.get(2).oid, "O-1")

        # 4. Hapus pesanan di indeks 1 (O-2)
        hapus = arr.hapus_pesanan(1)
        self.assertEqual(hapus.oid, "O-2")
        self.assertEqual(len(arr), 2)
        self.assertEqual(arr.get(0).oid, "O-3")
        self.assertEqual(arr.get(1).oid, "O-1")

    def test_linklist_dasar_dan_operasi_bisnis(self):
        ll = LinkList()
        self.assertEqual(len(ll), 0)
        self.assertTrue(ll.is_empty())

        p_reg = Pesanan("O-1", "Reguler", "resto", "menu", 10000, 3, 0)
        p_prio = Pesanan("O-2", "Prioritas", "resto", "menu", 10000, 2, 0)
        p_vip = Pesanan("O-3", "VIP", "resto", "menu", 10000, 1, 0)

        # 1. Tambah Reguler (ke belakang via tail)
        ll.tambah_reguler(p_reg)
        self.assertEqual(len(ll), 1)
        self.assertEqual(ll.head.data.oid, "O-1")
        self.assertEqual(ll.tail.data.oid, "O-1")

        # 2. Tambah Prioritas (ke tengah: indeks 1 // 2 = 0)
        ll.tambah_prioritas(p_prio)
        self.assertEqual(len(ll), 2)
        self.assertEqual(ll.get(0).oid, "O-2")
        self.assertEqual(ll.get(1).oid, "O-1")

        # 3. Tambah VIP (ke indeks 0 via head)
        ll.tambah_vip(p_vip)
        self.assertEqual(len(ll), 3)
        self.assertEqual(ll.get(0).oid, "O-3")
        self.assertEqual(ll.get(1).oid, "O-2")
        self.assertEqual(ll.get(2).oid, "O-1")

        # 4. Hapus pesanan di indeks 1 (O-2)
        hapus = ll.hapus_pesanan(1)
        self.assertEqual(hapus.oid, "O-2")
        self.assertEqual(len(ll), 2)
        self.assertEqual(ll.get(0).oid, "O-3")
        self.assertEqual(ll.get(1).oid, "O-1")

    def test_keselarasan_array_dan_linklist(self):
        """Memastikan urutan data di Array dan LinkList selalu identik."""
        arr = Array(4)
        ll = LinkList()

        for i in range(10):
            p = Pesanan("O-%03d" % i, "Pelanggan-%d" % i, "resto", "menu", 10000, 3, 0)
            arr.append(p)
            ll.append(p)

        self.assertEqual(len(arr), len(ll))
        for i in range(10):
            self.assertEqual(arr.get(i).oid, ll.get(i).oid)

        # Sisipkan VIP di indeks 0
        p_vip = Pesanan("O-VIP", "VIP", "resto", "menu", 20000, 1, 0)
        arr.tambah_vip(p_vip)
        ll.tambah_vip(p_vip)

        self.assertEqual(len(arr), len(ll))
        for i in range(len(arr)):
            self.assertEqual(arr.get(i).oid, ll.get(i).oid)

        # Sisipkan Prioritas di tengah
        p_prio = Pesanan("O-PRIO", "Prio", "resto", "menu", 15000, 2, 0)
        arr.tambah_prioritas(p_prio)
        ll.tambah_prioritas(p_prio)

        self.assertEqual(len(arr), len(ll))
        for i in range(len(arr)):
            self.assertEqual(arr.get(i).oid, ll.get(i).oid)

        # Hapus tengah
        arr.hapus_pesanan(5)
        ll.hapus_pesanan(5)

        self.assertEqual(len(arr), len(ll))
        for i in range(len(arr)):
            self.assertEqual(arr.get(i).oid, ll.get(i).oid)

    def test_sistem_m1_muat_csv(self):
        sistem = SistemPesananM1()
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "pesanan.csv")
        if os.path.exists(csv_path):
            total, ms_arr, ms_ll = sistem.muat_csv(csv_path)
            self.assertEqual(total, 200000)
            self.assertEqual(len(sistem.array), 200000)
            self.assertEqual(len(sistem.linklist), 200000)
            # Bandingkan elemen pertama dan terakhir
            p_first_arr = sistem.array.get(0)
            p_first_ll = sistem.linklist.get(0)
            self.assertEqual(p_first_arr.oid, p_first_ll.oid)
            self.assertEqual(p_first_arr.oid, "O-000001")


    def test_iterasi_dan_pop(self):
        arr = Array(4)
        ll = LinkList()
        for i in range(5):
            p = Pesanan("O-%d" % i, "User", "r", "m", 1000, 3, 0)
            arr.append(p)
            ll.append(p)

        # Test __iter__
        arr_oids = [p.oid for p in arr]
        ll_oids = [p.oid for p in ll]
        self.assertEqual(arr_oids, ["O-0", "O-1", "O-2", "O-3", "O-4"])
        self.assertEqual(ll_oids, ["O-0", "O-1", "O-2", "O-3", "O-4"])

        # Test pop() default (elemen terakhir)
        pop_arr = arr.pop()
        pop_ll = ll.pop()
        self.assertEqual(pop_arr.oid, "O-4")
        self.assertEqual(pop_ll.oid, "O-4")
        self.assertEqual(len(arr), 4)
        self.assertEqual(len(ll), 4)

    def test_kasus_batas_hapus_ujung(self):
        # 1. Hapus satu-satunya elemen
        ll = LinkList()
        p_single = Pesanan("O-S", "User", "r", "m", 1000, 3, 0)
        ll.append(p_single)
        removed = ll.delete(0)
        self.assertEqual(removed.oid, "O-S")
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(len(ll), 0)

        # 2. Hapus elemen terakhir pada list yang berisi beberapa elemen
        for i in range(3):
            ll.append(Pesanan("O-%d" % i, "User", "r", "m", 1000, 3, 0))
        # Hapus elemen terakhir (indeks 2)
        rem_last = ll.delete(2)
        self.assertEqual(rem_last.oid, "O-2")
        self.assertEqual(ll.tail.data.oid, "O-1")
        self.assertIsNone(ll.tail.next)
        self.assertEqual(len(ll), 2)

    def test_pencarian_oid(self):
        arr = Array(4)
        ll = LinkList()
        for i in range(5):
            p = Pesanan("O-%03d" % i, "User", "r", "m", 1000, 3, 0)
            arr.append(p)
            ll.append(p)

        self.assertEqual(arr.find_by_oid("O-002"), 2)
        self.assertEqual(ll.find_by_oid("O-002"), 2)
        self.assertEqual(arr.find_by_oid("O-999"), -1)
        self.assertEqual(ll.find_by_oid("O-999"), -1)


if __name__ == "__main__":
    unittest.main()
