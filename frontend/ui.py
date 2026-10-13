# ==============================================================================
# PROYEK "2EZ4U APP" - STRUKTUR DATA & ANALISA ALGORITMA (EC234303)
# Modul: frontend/ui.py
# Antarmuka Desktop Satu Jendela Tkinter
# Kepatuhan: Struktur data mandiri murni primitif
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import time
import os
from backend.m1_pesanan import Pesanan, SistemPesananM1


class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("1100x720")
        self.root.minsize(950, 600)
        self.root.configure(bg="#eef2f6")

        self.sistem = SistemPesananM1()
        self.current_menu = None
        self.menu_buttons = []

        self._setup_ui()
        self._set_menu("ARRAY - TAMBAH PESANAN REGULER")

    def _setup_ui(self):
        # 1. Header Banner
        header = tk.Frame(self.root, bg="#1c3b57", height=42)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title_lbl = tk.Label(
            header,
            text="2EZ4U Food Delivery",
            bg="#1c3b57",
            fg="#ffffff",
            font=("Segoe UI", 13, "bold"),
            padx=14
        )
        title_lbl.pack(side=tk.LEFT, fill=tk.Y)

        # 2. Main Content Area (Paned / Split Frame)
        main_pane = tk.Frame(self.root, bg="#eef2f6")
        main_pane.pack(fill=tk.BOTH, expand=True, padx=8, pady=(6, 2))

        # 2.1 Sidebar Frame (Kiri)
        self.sidebar_frame = tk.Frame(main_pane, bg="#f8fafc", width=290, bd=1, relief=tk.SOLID)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))
        self.sidebar_frame.pack_propagate(False)

        self._create_sidebar(self.sidebar_frame)

        # 2.2 Content Panel (Kanan)
        self.content_frame = tk.Frame(main_pane, bg="#ffffff", bd=1, relief=tk.SOLID)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._create_content_panel(self.content_frame)

        # 3. Status Bar (Bawah)
        self.bottom_bar = tk.Frame(self.root, bg="#e2e8f0", height=32, bd=1, relief=tk.GROOVE)
        self.bottom_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.bottom_bar.pack_propagate(False)

        self.status_badge = tk.Label(
            self.bottom_bar,
            text="siap",
            bg="#1c3b57",
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=2
        )
        self.status_badge.pack(side=tk.LEFT, padx=8, pady=3)

        self.status_info = tk.Label(
            self.bottom_bar,
            text="Data belum dimuat. Klik 'Load' di menu DATA.",
            bg="#e2e8f0",
            fg="#334155",
            font=("Segoe UI", 9)
        )
        self.status_info.pack(side=tk.LEFT, padx=10)

    def _create_sidebar(self, parent):
        canvas = tk.Canvas(parent, bg="#f8fafc", highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f8fafc")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=270)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Group 1: DATA
        self._add_group_label(scrollable_frame, "DATA")
        self._add_sidebar_button(scrollable_frame, "Load", lambda: self._set_menu("DATA - LOAD"))

        # Group 2: M1 - DATA PESANAN
        self._add_group_label(scrollable_frame, "M1 - DATA PESANAN")
        self._add_sidebar_button(scrollable_frame, "ARRAY - LIHAT PESANAN", lambda: self._set_menu("ARRAY - LIHAT PESANAN"))
        self._add_sidebar_button(scrollable_frame, "ARRAY - TAMBAH PESANAN REGULER", lambda: self._set_menu("ARRAY - TAMBAH PESANAN REGULER"))
        self._add_sidebar_button(scrollable_frame, "ARRAY - TAMBAH PESANAN PRIORITAS", lambda: self._set_menu("ARRAY - TAMBAH PESANAN PRIORITAS"))
        self._add_sidebar_button(scrollable_frame, "ARRAY - TAMBAH PESANAN VIP", lambda: self._set_menu("ARRAY - TAMBAH PESANAN VIP"))
        self._add_sidebar_button(scrollable_frame, "ARRAY - HAPUS PESANAN", lambda: self._set_menu("ARRAY - HAPUS PESANAN"))

        self._add_sidebar_button(scrollable_frame, "LINKEDLIST - LIHAT PESANAN", lambda: self._set_menu("LINKEDLIST - LIHAT PESANAN"))
        self._add_sidebar_button(scrollable_frame, "LINKEDLIST - TAMBAH PESANAN REGULER", lambda: self._set_menu("LINKEDLIST - TAMBAH PESANAN REGULER"))
        self._add_sidebar_button(scrollable_frame, "LINKEDLIST - TAMBAH PESANAN PRIORITAS", lambda: self._set_menu("LINKEDLIST - TAMBAH PESANAN PRIORITAS"))
        self._add_sidebar_button(scrollable_frame, "LINKEDLIST - TAMBAH PESANAN VIP", lambda: self._set_menu("LINKEDLIST - TAMBAH PESANAN VIP"))
        self._add_sidebar_button(scrollable_frame, "LINKEDLIST - HAPUS PESANAN", lambda: self._set_menu("LINKEDLIST - HAPUS PESANAN"))
        self._add_sidebar_button(scrollable_frame, "ADU PERFORMA ARRAY VS LINKEDLIST", lambda: self._set_menu("BENCHMARK M1"))

        # Group 3: M2 - ANTREAN DAN UNDO (Placeholder visual)
        self._add_group_label(scrollable_frame, "M2 - ANTREAN DAN UNDO")
        self._add_sidebar_button(scrollable_frame, "Isi antrean FIFO", lambda: self._placeholder_milestone("M2"))
        self._add_sidebar_button(scrollable_frame, "Layani berikutnya", lambda: self._placeholder_milestone("M2"))
        self._add_sidebar_button(scrollable_frame, "Undo", lambda: self._placeholder_milestone("M2"))

        # Group 4: M3 DAN M4 - LAPORAN DAN PENCARIAN
        self._add_group_label(scrollable_frame, "M3 DAN M4 - LAPORAN DAN PENCARIAN")
        self._add_sidebar_button(scrollable_frame, "Laporan harian", lambda: self._placeholder_milestone("M3"))
        self._add_sidebar_button(scrollable_frame, "Cari di laporan", lambda: self._placeholder_milestone("M3"))
        self._add_sidebar_button(scrollable_frame, "Bangun indeks hash", lambda: self._placeholder_milestone("M4"))
        self._add_sidebar_button(scrollable_frame, "Cari pesanan (oid)", lambda: self._placeholder_milestone("M4"))

        # Group 5: M5 - KATALOG DAN PRIORITAS
        self._add_group_label(scrollable_frame, "M5 - KATALOG DAN PRIORITAS")
        self._add_sidebar_button(scrollable_frame, "Menu per rentang harga", lambda: self._placeholder_milestone("M5"))
        self._add_sidebar_button(scrollable_frame, "Isi antrean prioritas", lambda: self._placeholder_milestone("M5"))

        # Group 6: M6 - PETA DAN RUTE
        self._add_group_label(scrollable_frame, "M6 - PETA DAN RUTE")
        self._add_sidebar_button(scrollable_frame, "Muat peta", lambda: self._placeholder_milestone("M6"))

    def _add_group_label(self, parent, text):
        lbl = tk.Label(
            parent,
            text=text,
            bg="#f8fafc",
            fg="#64748b",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
            padx=8,
            pady=4
        )
        lbl.pack(fill=tk.X, padx=4, pady=(6, 2))

    def _add_sidebar_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            bg="#ffffff",
            fg="#1e293b",
            activebackground="#e2e8f0",
            activeforeground="#0f172a",
            font=("Segoe UI", 8),
            bd=1,
            relief=tk.SOLID,
            anchor="w",
            padx=8,
            pady=3,
            cursor="hand2",
            command=command
        )
        btn.pack(fill=tk.X, padx=8, pady=1)
        self.menu_buttons.append((text, btn))

    def _create_content_panel(self, parent):
        # 1. Top Section: Header & Form
        self.form_container = tk.Frame(parent, bg="#ffffff", padx=16, pady=12)
        self.form_container.pack(fill=tk.X, side=tk.TOP)

        self.title_label = tk.Label(
            self.form_container,
            text="",
            bg="#ffffff",
            fg="#0f172a",
            font=("Segoe UI", 12, "bold"),
            anchor="w"
        )
        self.title_label.pack(fill=tk.X)

        self.subtitle_label = tk.Label(
            self.form_container,
            text="",
            bg="#ffffff",
            fg="#64748b",
            font=("Segoe UI", 9, "italic"),
            anchor="w"
        )
        self.subtitle_label.pack(fill=tk.X, pady=(2, 8))

        # Dynamic Form inputs
        self.form_fields_frame = tk.Frame(self.form_container, bg="#ffffff")
        self.form_fields_frame.pack(fill=tk.X, pady=(0, 6))

        # 2. Middle Section: Result Output Box
        result_box_frame = tk.Frame(parent, bg="#ffffff", padx=16, pady=4)
        result_box_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        self.result_text = tk.Text(
            result_box_frame,
            bg="#ffffff",
            fg="#0f172a",
            font=("Consolas", 10),
            bd=1,
            relief=tk.SOLID,
            padx=8,
            pady=8,
            wrap=tk.NONE
        )
        res_scroll_y = tk.Scrollbar(result_box_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        res_scroll_x = tk.Scrollbar(result_box_frame, orient=tk.HORIZONTAL, command=self.result_text.xview)
        self.result_text.configure(yscrollcommand=res_scroll_y.set, xscrollcommand=res_scroll_x.set)

        res_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        res_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 3. Bottom Section: COMMAND history panel
        cmd_container = tk.Frame(parent, bg="#ffffff", padx=16, pady=4)
        cmd_container.pack(fill=tk.X, side=tk.BOTTOM, pady=(0, 10))

        cmd_title = tk.Label(
            cmd_container,
            text="COMMAND",
            bg="#ffffff",
            fg="#64748b",
            font=("Segoe UI", 9, "bold"),
            anchor="w"
        )
        cmd_title.pack(fill=tk.X, pady=(0, 2))

        cmd_frame = tk.Frame(cmd_container, bd=1, relief=tk.SOLID)
        cmd_frame.pack(fill=tk.X)

        self.cmd_text = tk.Text(
            cmd_frame,
            bg="#f8fafc",
            fg="#1e293b",
            font=("Consolas", 9),
            height=4,
            wrap=tk.NONE,
            bd=0
        )
        cmd_scroll_y = tk.Scrollbar(cmd_frame, orient=tk.VERTICAL, command=self.cmd_text.yview)
        self.cmd_text.configure(yscrollcommand=cmd_scroll_y.set)

        cmd_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.cmd_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _log_command(self, cmd_name, module_name, durasi_ms):
        log_line = "%-22s -> %-18s %8.2f ms\n" % (cmd_name, module_name, durasi_ms)
        self.cmd_text.insert(tk.END, log_line)
        self.cmd_text.see(tk.END)

    def _update_status(self, badge_text, info_text):
        self.status_badge.config(text=badge_text)
        self.status_info.config(text=info_text)

    def _set_menu(self, menu_name):
        self.current_menu = menu_name

        # Highlight active menu button
        for name, btn in self.menu_buttons:
            if name == menu_name or (menu_name == "DATA - LOAD" and name == "Load") or (menu_name == "BENCHMARK M1" and name == "ADU PERFORMA ARRAY VS LINKEDLIST"):
                btn.config(bg="#d8e5f2", relief=tk.SOLID)
            else:
                btn.config(bg="#ffffff", relief=tk.SOLID)

        # Clear existing form fields
        for widget in self.form_fields_frame.winfo_children():
            widget.destroy()

        if menu_name == "DATA - LOAD":
            self.title_label.config(text="Data: Muat Berkas CSV Pesanan")
            self.subtitle_label.config(text="Membaca 200.000 data pesanan ke dalam Array dan Linked List secara simultan.")

            row = tk.Frame(self.form_fields_frame, bg="#ffffff")
            row.pack(fill=tk.X, pady=2)

            tk.Label(row, text="Path berkas CSV:", bg="#ffffff", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))
            csv_entry = tk.Entry(row, width=40, font=("Segoe UI", 9))
            csv_entry.insert(0, "data/pesanan.csv")
            csv_entry.pack(side=tk.LEFT, padx=(0, 10))

            btn = tk.Button(
                row,
                text="LOAD DATA",
                bg="#1c3b57",
                fg="#ffffff",
                font=("Segoe UI", 9, "bold"),
                padx=14,
                pady=2,
                cursor="hand2",
                command=lambda: self._aksi_load_csv(csv_entry.get().strip())
            )
            btn.pack(side=tk.LEFT)

        elif "LIHAT PESANAN" in menu_name:
            is_arr = "ARRAY" in menu_name
            if is_arr:
                self.title_label.config(text="Array: lihat pesanan ke-i")
                self.subtitle_label.config(text="buka detail satu pesanan secara langsung O(1).")
            else:
                self.title_label.config(text="Linked List: lihat pesanan ke-i")
                self.subtitle_label.config(text="buka detail satu pesanan dengan penelusuran simpul O(n).")

            row = tk.Frame(self.form_fields_frame, bg="#ffffff")
            row.pack(fill=tk.X, pady=2)

            tk.Label(row, text="Indeks pesanan (ke-i):", bg="#ffffff", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))
            idx_entry = tk.Entry(row, width=15, font=("Segoe UI", 9))
            idx_entry.insert(0, "0")
            idx_entry.pack(side=tk.LEFT, padx=(0, 10))

            btn = tk.Button(
                row,
                text="LIHAT",
                bg="#1c3b57",
                fg="#ffffff",
                font=("Segoe UI", 9, "bold"),
                padx=14,
                pady=2,
                cursor="hand2",
                command=lambda: self._aksi_lihat_pesanan(is_arr, idx_entry.get().strip())
            )
            btn.pack(side=tk.LEFT)

            hint = tk.Label(
                self.form_fields_frame,
                text="masukkan nomor indeks (0 sampai ukuran-1)",
                bg="#ffffff",
                fg="#64748b",
                font=("Segoe UI", 8)
            )
            hint.pack(anchor="w", pady=(2, 0))

        elif "HAPUS PESANAN" in menu_name:
            is_arr = "ARRAY" in menu_name
            if is_arr:
                self.title_label.config(text="Array: hapus pesanan ke-i")
                self.subtitle_label.config(text="pesanan dicabut dari barisan, menggeser sisa elemen ke kiri O(n).")
            else:
                self.title_label.config(text="Linked List: hapus pesanan ke-i")
                self.subtitle_label.config(text="pesanan dicabut dari barisan setelah menelusuri simpul ke-(i-1) O(n).")

            row = tk.Frame(self.form_fields_frame, bg="#ffffff")
            row.pack(fill=tk.X, pady=2)

            tk.Label(row, text="Indeks pesanan (ke-i):", bg="#ffffff", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))
            idx_entry = tk.Entry(row, width=15, font=("Segoe UI", 9))
            idx_entry.insert(0, "0")
            idx_entry.pack(side=tk.LEFT, padx=(0, 10))

            btn = tk.Button(
                row,
                text="HAPUS",
                bg="#1c3b57",
                fg="#ffffff",
                font=("Segoe UI", 9, "bold"),
                padx=14,
                pady=2,
                cursor="hand2",
                command=lambda: self._aksi_hapus_pesanan(is_arr, idx_entry.get().strip())
            )
            btn.pack(side=tk.LEFT)

            hint = tk.Label(
                self.form_fields_frame,
                text="pesanan pada indeks yang ditentukan akan dicabut",
                bg="#ffffff",
                fg="#64748b",
                font=("Segoe UI", 8)
            )
            hint.pack(anchor="w", pady=(2, 0))

        elif "TAMBAH PESANAN" in menu_name:
            is_arr = "ARRAY" in menu_name
            if "REGULER" in menu_name:
                jenis = "REGULER"
                if is_arr:
                    self.title_label.config(text="Array: pesanan REGULER, masuk paling belakang")
                    self.subtitle_label.config(text="append: pesanan biasa mengantre di barisan paling belakang O(1) amortized.")
                else:
                    self.title_label.config(text="Linked List: pesanan REGULER, masuk paling belakang")
                    self.subtitle_label.config(text="append: pesanan biasa ditambahkan di ujung tail O(1).")
            elif "PRIORITAS" in menu_name:
                jenis = "PRIORITAS"
                if is_arr:
                    self.title_label.config(text="Array: pesanan PRIORITAS, menyerobot ke tengah")
                    self.subtitle_label.config(text="insert di tengah (n//2): menggeser separuh isi array ke kanan O(n).")
                else:
                    self.title_label.config(text="Linked List: pesanan PRIORITAS, menyerobot ke tengah")
                    self.subtitle_label.config(text="insert di tengah (n//2): menelusuri n//2 simpul lalu menyambung sekali O(n).")
            else:  # VIP
                jenis = "VIP"
                if is_arr:
                    self.title_label.config(text="Array: pesanan VIP, langsung ke urutan pertama")
                    self.subtitle_label.config(text="insert di indeks 0: menggeser seluruh isi array ke kanan O(n).")
                else:
                    self.title_label.config(text="Linked List: pesanan VIP, langsung ke urutan pertama")
                    self.subtitle_label.config(text="prepend di indeks 0: langsung mengubah penunjuk head O(1).")

            row = tk.Frame(self.form_fields_frame, bg="#ffffff")
            row.pack(fill=tk.X, pady=2)

            tk.Label(row, text="Nama pelanggan:", bg="#ffffff", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))
            name_entry = tk.Entry(row, width=30, font=("Segoe UI", 9))
            name_entry.insert(0, "Pelanggan Baru")
            name_entry.pack(side=tk.LEFT, padx=(0, 10))

            btn = tk.Button(
                row,
                text="TAMBAH",
                bg="#1c3b57",
                fg="#ffffff",
                font=("Segoe UI", 9, "bold"),
                padx=14,
                pady=2,
                cursor="hand2",
                command=lambda: self._aksi_tambah_pesanan(is_arr, jenis, name_entry.get().strip())
            )
            btn.pack(side=tk.LEFT)

            hint = tk.Label(
                self.form_fields_frame,
                text="nama untuk pesanan yang akan dibuat",
                bg="#ffffff",
                fg="#64748b",
                font=("Segoe UI", 8)
            )
            hint.pack(anchor="w", pady=(2, 0))

        elif menu_name == "BENCHMARK M1":
            self.title_label.config(text="Adu Performa Langsung: Array vs Linked List")
            self.subtitle_label.config(text="Menguji kelima operasi bisnis secara langsung pada data 200.000 pesanan.")

            row = tk.Frame(self.form_fields_frame, bg="#ffffff")
            row.pack(fill=tk.X, pady=2)

            btn = tk.Button(
                row,
                text="JALANKAN PENGUJIAN ADU PERFORMA",
                bg="#1c3b57",
                fg="#ffffff",
                font=("Segoe UI", 9, "bold"),
                padx=14,
                pady=4,
                cursor="hand2",
                command=self._aksi_benchmark
            )
            btn.pack(side=tk.LEFT)

    def _tampilkan_tabel_pesanan(self, p, info_tambahan=""):
        self.result_text.delete("1.0", tk.END)

        if info_tambahan:
            self.result_text.insert(tk.END, info_tambahan + "\n\n")

        header_tbl = "%-16s | %s\n" % ("kolom", "isi")
        separator  = "%s\n" % ("-" * 50)
        self.result_text.insert(tk.END, header_tbl)
        self.result_text.insert(tk.END, separator)

        rows = (
            ("oid", p.oid),
            ("pelanggan", p.pelanggan),
            ("resto", p.resto),
            ("menu", p.menu),
            ("harga", p.format_harga()),
            ("prioritas", str(p.prioritas)),
            ("masuk", p.format_t_masuk()),
            ("selesai", p.format_t_selesai()),
            ("status", p.status),
        )

        for col, val in rows:
            line = "%-16s | %s\n" % (col, val)
            self.result_text.insert(tk.END, line)

    def _aksi_load_csv(self, filepath):
        if not os.path.exists(filepath):
            messagebox.showerror("Galat", "Berkas tidak ditemukan: " + filepath)
            return

        self._update_status("[ memuat... ]", "Sedang membaca berkas CSV...")
        self.root.update_idletasks()

        try:
            total, ms_arr, ms_ll = self.sistem.muat_csv(filepath)
            self._log_command("load", "M1 - larik", ms_arr)
            self._log_command("load", "M1 - linked list", ms_ll)

            self.result_text.delete("1.0", tk.END)
            msg = "=" * 60 + "\n"
            msg += "HASIL PEMUATAN DATA PESANAN\n"
            msg += "=" * 60 + "\n"
            msg += "Berkas sumber          : %s\n" % filepath
            msg += "Total data terbaca     : %d pesanan\n\n" % total
            msg += "1. STRUKTUR LARIK (ARRAY BERUKURAN TETAP 2x):\n"
            msg += "   - Ukuran data       : %d elemen\n" % self.sistem.array.size
            msg += "   - Kapasitas akhir   : %d slot\n" % self.sistem.array.capacity
            msg += "   - Total resize 2x   : %d kali penggandaan\n" % self.sistem.array.resize_count
            msg += "   - Durasi pemuatan   : %.2f ms (amortized O(1))\n\n" % ms_arr
            msg += "2. STRUKTUR RANTAI (LINKED LIST HEAD & TAIL):\n"
            msg += "   - Ukuran simpul     : %d simpul\n" % self.sistem.linklist.size
            msg += "   - Durasi pemuatan   : %.2f ms (O(1) via pointer tail)\n" % ms_ll
            msg += "=" * 60 + "\n"
            msg += "Data siap digunakan untuk pengujian operasi M1.\n"
            self.result_text.insert(tk.END, msg)

            badge = "[M1 - larik] %.2f ms" % ms_arr
            info = "Total: %d pesanan | Kapasitas: %d" % (total, self.sistem.array.capacity)
            self._update_status(badge, info)

        except Exception as e:
            messagebox.showerror("Galat Pemuatan", str(e))
            self._update_status("[ galat ]", str(e))

    def _pastikan_data_termuat(self):
        if not self.sistem.is_loaded or self.sistem.array.size == 0:
            csv_path = "data/pesanan.csv"
            if os.path.exists(csv_path):
                self._aksi_load_csv(csv_path)
                return True
            else:
                messagebox.showwarning("Peringatan", "Silakan muat data CSV terlebih dahulu melalui menu DATA -> Load.")
                return False
        return True

    def _aksi_lihat_pesanan(self, is_arr, idx_str):
        if not self._pastikan_data_termuat():
            return
        try:
            idx = int(idx_str)
        except ValueError:
            messagebox.showerror("Galat Input", "Indeks harus berupa bilangan bulat.")
            return

        ukuran = self.sistem.array.size if is_arr else self.sistem.linklist.size
        if idx < 0 or idx >= ukuran:
            messagebox.showerror("Galat Indeks", "Indeks %d di luar rentang (0 sampai %d)." % (idx, ukuran - 1))
            return

        if is_arr:
            p, ms, shifts = self.sistem.array_lihat(idx)
            modul = "M1 - array"
            cmd = "array_get"
            info = "ARRAY: Pesanan pada indeks ke-%d ditemukan.\nWaktu akses: %.2f ms (O(1) langsung via alamat memori)." % (idx, ms)
        else:
            p, ms, trav = self.sistem.linklist_lihat(idx)
            modul = "M1 - linked list"
            cmd = "linklist_get"
            info = "LINKED LIST: Pesanan pada indeks ke-%d ditemukan.\nWaktu akses: %.2f ms (O(n) - %d simpul ditelusuri)." % (idx, ms, trav)

        self._log_command(cmd, modul, ms)
        self._update_status("[%s] %.2f ms" % (modul, ms), "Lihat pesanan indeks ke-%d" % idx)
        self._tampilkan_tabel_pesanan(p, info)

    def _aksi_hapus_pesanan(self, is_arr, idx_str):
        if not self._pastikan_data_termuat():
            return
        try:
            idx = int(idx_str)
        except ValueError:
            messagebox.showerror("Galat Input", "Indeks harus berupa bilangan bulat.")
            return

        ukuran = self.sistem.array.size if is_arr else self.sistem.linklist.size
        if idx < 0 or idx >= ukuran:
            messagebox.showerror("Galat Indeks", "Indeks %d di luar rentang (0 sampai %d)." % (idx, ukuran - 1))
            return

        if is_arr:
            p, ms, shifts = self.sistem.array_hapus(idx, sinkron=True)
            modul = "M1 - array"
            cmd = "array_delete"
            info = "ARRAY: Pesanan %s dicabut dari indeks ke-%d.\nPergeseran: %d elemen digeser ke kiri (O(n)).\nWaktu eksekusi: %.2f ms." % (p.oid, idx, shifts, ms)
        else:
            p, ms, trav = self.sistem.linklist_hapus(idx, sinkron=True)
            modul = "M1 - linked list"
            cmd = "linklist_delete"
            info = "LINKED LIST: Pesanan %s dicabut dari indeks ke-%d.\nPenelusuran: %d simpul ditelusuri (O(n)).\nWaktu eksekusi: %.2f ms." % (p.oid, idx, trav, ms)

        self._log_command(cmd, modul, ms)
        self._update_status("[%s] %.2f ms" % (modul, ms), "Hapus pesanan %s" % p.oid)
        self._tampilkan_tabel_pesanan(p, info)

    def _aksi_tambah_pesanan(self, is_arr, jenis, nama_pelanggan):
        if not self._pastikan_data_termuat():
            return
        if not nama_pelanggan:
            nama_pelanggan = "Pelanggan Baru"

        oid_baru = self.sistem.generate_oid()
        prio_val = 3 if jenis == "REGULER" else (2 if jenis == "PRIORITAS" else 1)
        p = Pesanan(
            oid=oid_baru,
            pelanggan=nama_pelanggan,
            resto="kafe-teknik",
            menu="roti-bakar",
            harga=12000,
            prioritas=prio_val,
            t_masuk_detik=int(time.time()) % 86400,
            t_selesai_detik=None,
            status="ANTRE"
        )

        if is_arr:
            modul = "M1 - array"
            if jenis == "REGULER":
                cmd = "array_append_reguler"
                p, ms, shifts = self.sistem.array_tambah_reguler(p, sinkron=True)
                penjelasan = "masuk barisan paling belakang: %d elemen digeser (O(1) amortized)." % shifts
            elif jenis == "PRIORITAS":
                cmd = "array_insert_prioritas"
                p, ms, shifts = self.sistem.array_tambah_prioritas(p, sinkron=True)
                penjelasan = "menyerobot ke tengah barisan: %d elemen digeser ke kanan (O(n))." % shifts
            else:  # VIP
                cmd = "array_insert_vip"
                p, ms, shifts = self.sistem.array_tambah_vip(p, sinkron=True)
                penjelasan = "langsung ke urutan pertama (indeks 0): %d elemen digeser ke kanan (O(n))." % shifts

            info = "ARRAY: Pesanan %s (%s) berhasil ditambahkan.\nPerilaku: %s\nWaktu eksekusi: %.2f ms." % (p.oid, jenis, penjelasan, ms)

        else:
            modul = "M1 - linked list"
            if jenis == "REGULER":
                cmd = "linklist_append_reguler"
                p, ms, trav = self.sistem.linklist_tambah_reguler(p, sinkron=True)
                penjelasan = "masuk barisan paling belakang: %d simpul ditelusuri (O(1) via penunjuk tail)." % trav
            elif jenis == "PRIORITAS":
                cmd = "linklist_insert_prioritas"
                p, ms, trav = self.sistem.linklist_tambah_prioritas(p, sinkron=True)
                penjelasan = "menyerobot ke tengah: %d simpul ditelusuri lalu sambung sekali (O(n) telusur)." % trav
            else:  # VIP
                cmd = "linklist_prepend_vip"
                p, ms, trav = self.sistem.linklist_tambah_vip(p, sinkron=True)
                penjelasan = "langsung ke urutan pertama (head): %d simpul ditelusuri (O(1) ubah penunjuk head)." % trav

            info = "LINKED LIST: Pesanan %s (%s) berhasil ditambahkan.\nPerilaku: %s\nWaktu eksekusi: %.2f ms." % (p.oid, jenis, penjelasan, ms)

        self._log_command(cmd, modul, ms)
        self._update_status("[%s] %.2f ms" % (modul, ms), "Tambah pesanan %s (%s)" % (p.oid, jenis))
        self._tampilkan_tabel_pesanan(p, info)

    def _aksi_benchmark(self):
        if not self._pastikan_data_termuat():
            return

        self._update_status("[ menguji... ]", "Menjalankan adu performa M1...")
        self.root.update_idletasks()

        # Uji 1: REGULER
        p_reg1 = Pesanan(self.sistem.generate_oid(), "Tester Reguler", "kafe", "teh", 5000, 3, 0)
        p_reg2 = Pesanan(self.sistem.generate_oid(), "Tester Reguler", "kafe", "teh", 5000, 3, 0)
        t0 = time.perf_counter()
        self.sistem.array.tambah_reguler(p_reg1)
        t_arr_reg = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        self.sistem.linklist.tambah_reguler(p_reg2)
        t_ll_reg = (time.perf_counter() - t0) * 1000.0

        # Uji 2: PRIORITAS (tengah)
        p_prio1 = Pesanan(self.sistem.generate_oid(), "Tester Prioritas", "kafe", "kopi", 10000, 2, 0)
        p_prio2 = Pesanan(self.sistem.generate_oid(), "Tester Prioritas", "kafe", "kopi", 10000, 2, 0)
        t0 = time.perf_counter()
        self.sistem.array.tambah_prioritas(p_prio1)
        t_arr_prio = (time.perf_counter() - t0) * 1000.0
        shifts_prio = self.sistem.array.last_shift_count

        t0 = time.perf_counter()
        self.sistem.linklist.tambah_prioritas(p_prio2)
        t_ll_prio = (time.perf_counter() - t0) * 1000.0
        trav_prio = self.sistem.linklist.last_traversal_count

        # Uji 3: VIP (depan)
        p_vip1 = Pesanan(self.sistem.generate_oid(), "Tester VIP", "kafe", "steak", 50000, 1, 0)
        p_vip2 = Pesanan(self.sistem.generate_oid(), "Tester VIP", "kafe", "steak", 50000, 1, 0)
        t0 = time.perf_counter()
        self.sistem.array.tambah_vip(p_vip1)
        t_arr_vip = (time.perf_counter() - t0) * 1000.0
        shifts_vip = self.sistem.array.last_shift_count

        t0 = time.perf_counter()
        self.sistem.linklist.tambah_vip(p_vip2)
        t_ll_vip = (time.perf_counter() - t0) * 1000.0
        trav_vip = self.sistem.linklist.last_traversal_count

        # Uji 4: Lihat Pesanan di Tengah
        mid_idx = self.sistem.array.size // 2
        t0 = time.perf_counter()
        self.sistem.array.lihat_pesanan(mid_idx)
        t_arr_get = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        self.sistem.linklist.lihat_pesanan(mid_idx)
        t_ll_get = (time.perf_counter() - t0) * 1000.0

        self.result_text.delete("1.0", tk.END)
        msg = "=" * 80 + "\n"
        msg += "TABEL PERBANDINGAN PERFORMA REAL-TIME: ARRAY VS LINKED LIST (n = 200.000)\n"
        msg += "=" * 80 + "\n\n"

        msg += "%-16s | %-12s | %-14s | %s\n" % ("Jenis Operasi", "Array", "Linked List", "Apa yang sebenarnya terjadi")
        msg += "%s\n" % ("-" * 80)
        msg += "%-16s | %9.2f ms | %11.2f ms | Keduanya menempel di ujung belakang (O(1))\n" % ("REGULER", t_arr_reg, t_ll_reg)
        msg += "%-16s | %9.2f ms | %11.2f ms | Array geser %d; LL telusur %d simpul\n" % ("PRIORITAS", t_arr_prio, t_ll_prio, shifts_prio, trav_prio)
        msg += "%-16s | %9.2f ms | %11.2f ms | Array geser %d; LL hanya ubah 1 penunjuk\n" % ("VIP", t_arr_vip, t_ll_vip, shifts_vip)
        msg += "%-16s | %9.2f ms | %11.2f ms | Array O(1) direct memory; LL O(n) %d telusur\n" % ("LIHAT TENGAH", t_arr_get, t_ll_get, mid_idx)
        msg += "%s\n\n" % ("=" * 80)

        msg += "KESIMPULAN ANALISIS:\n"
        msg += "1. REGULER   : Keduanya setara konstan O(1) karena Array ber-amortisasi dan Linked List memakai pointer tail.\n"
        msg += "2. PRIORITAS : Keduanya berbiaya O(n), tetapi Array menggeser elemen memori sementara Linked List menelusuri simpul.\n"
        msg += "3. VIP       : Linked List menang telak O(1) karena hanya mengarahkan pointer head, sedangkan Array O(n) menggeser seluruh 200.000 elemen.\n"
        msg += "4. LIHAT     : Array menang mutlak O(1) via pengalamatan langsung memori, sedangkan Linked List harus menelusuri simpul demi simpul O(n).\n"

        self.result_text.insert(tk.END, msg)
        self._log_command("benchmark_m1", "M1 - adu performa", t_arr_vip)
        self._update_status("[M1 - benchmark] Selesai", "Adu performa Array vs Linked List berhasil.")

    def _placeholder_milestone(self, m_name):
        messagebox.showinfo("Informasi Milestone", "Fitur %s akan dikembangkan pada tahapan tugas berikutnya." % m_name)
