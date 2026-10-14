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
        self.root.geometry("1180x740")
        self.root.minsize(1000, 640)
        self.root.configure(bg="#eef2f6")

        self.sistem = SistemPesananM1()
        self.current_menu = None
        self.menu_buttons = []

        # Variabel pagination tabel
        self.page_size = 100
        self.current_page = 1
        self.total_pages = 1
        self.show_all_mode = False

        self._init_styles()
        self._setup_ui()
        self._set_menu("ARRAY - LIHAT PESANAN")

        # Coba muat otomatis data jika ada
        if os.path.exists("data/pesanan.csv"):
            self._aksi_load_csv("data/pesanan.csv")

    def _init_styles(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Konfigurasi Header dan Isi Treeview
        self.style.configure(
            "Custom.Treeview.Heading",
            background="#d1d5db",
            foreground="#111827",
            font=("Segoe UI", 9, "bold"),
            relief="solid",
            borderwidth=1
        )
        self.style.configure(
            "Custom.Treeview",
            background="#ffffff",
            foreground="#1e293b",
            fieldbackground="#ffffff",
            font=("Segoe UI", 9),
            rowheight=24,
            relief="solid",
            borderwidth=1
        )
        self.style.map(
            "Custom.Treeview",
            background=[("selected", "#dbeafe")],
            foreground=[("selected", "#1e3a8a")]
        )

    def _setup_ui(self):
        # 1. Header Banner Atas
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

        # 2. Main Content Area (Split Kiri & Kanan)
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
        self.form_container = tk.Frame(parent, bg="#ffffff", padx=16, pady=8)
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
        self.subtitle_label.pack(fill=tk.X, pady=(2, 6))

        # Dynamic Form inputs
        self.form_fields_frame = tk.Frame(self.form_container, bg="#ffffff")
        self.form_fields_frame.pack(fill=tk.X, pady=(0, 4))

        # Action Info / Notification banner
        self.action_info_lbl = tk.Label(
            self.form_container,
            text="",
            bg="#f1f5f9",
            fg="#0f172a",
            font=("Segoe UI", 9),
            anchor="w",
            padx=8,
            pady=4,
            bd=1,
            relief=tk.GROOVE
        )
        self.action_info_lbl.pack(fill=tk.X, pady=(2, 0))

        # 2. Middle Section: Tabbed Notebook (Tabel & Log)
        self.notebook_frame = tk.Frame(parent, bg="#ffffff", padx=16, pady=4)
        self.notebook_frame.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Tabel Pesanan (Semua Data)
        self.tab_table = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.tab_table, text="  📋 Tabel Semua Pesanan  ")
        self._create_table_view(self.tab_table)

        # Tab 2: Log & Rincian
        self.tab_log = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.tab_log, text="  ⚡ Log & Adu Performa  ")
        self._create_log_view(self.tab_log)

        # 3. Bottom Section: COMMAND history panel
        cmd_container = tk.Frame(parent, bg="#ffffff", padx=16, pady=4)
        cmd_container.pack(fill=tk.X, side=tk.BOTTOM, pady=(0, 8))

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
            height=3,
            wrap=tk.NONE,
            bd=0
        )
        cmd_scroll_y = tk.Scrollbar(cmd_frame, orient=tk.VERTICAL, command=self.cmd_text.yview)
        self.cmd_text.configure(yscrollcommand=cmd_scroll_y.set)

        cmd_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.cmd_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _create_table_view(self, parent):
        table_container = tk.Frame(parent, bg="#ffffff")
        table_container.pack(fill=tk.BOTH, expand=True, pady=4)

        columns = (
            "oid",
            "pelanggan",
            "resto",
            "menu",
            "harga",
            "prioritas",
            "t_masuk_detik",
            "t_selesai_detik",
            "status"
        )

        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        col_configs = (
            ("oid", "oid", 95, tk.CENTER),
            ("pelanggan", "pelanggan", 210, tk.W),
            ("resto", "resto", 130, tk.W),
            ("menu", "menu", 130, tk.W),
            ("harga", "harga", 85, tk.CENTER),
            ("prioritas", "prioritas", 75, tk.CENTER),
            ("t_masuk_detik", "t_masuk_detik", 110, tk.CENTER),
            ("t_selesai_detik", "t_selesai_detik", 110, tk.CENTER),
            ("status", "status", 85, tk.CENTER),
        )

        for col_id, col_text, col_w, col_anchor in col_configs:
            self.tree.heading(col_id, text=col_text, anchor=col_anchor)
            self.tree.column(col_id, width=col_w, minwidth=60, anchor=col_anchor)

        # Scrollbars untuk Treeview
        tree_scroll_y = tk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll_x = tk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bar Kontrol & Navigasi Halaman di Bawah Tabel
        nav_bar = tk.Frame(parent, bg="#f8fafc", bd=1, relief=tk.SOLID, padx=6, pady=4)
        nav_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(4, 0))

        btn_first = tk.Button(nav_bar, text="⏮ Awal", font=("Segoe UI", 8), command=self._page_first)
        btn_first.pack(side=tk.LEFT, padx=2)

        btn_prev = tk.Button(nav_bar, text="◀ Sebelumnya", font=("Segoe UI", 8), command=self._page_prev)
        btn_prev.pack(side=tk.LEFT, padx=2)

        self.lbl_page_info = tk.Label(nav_bar, text="Halaman 1 / 1", bg="#f8fafc", font=("Segoe UI", 9, "bold"), padx=6)
        self.lbl_page_info.pack(side=tk.LEFT, padx=4)

        btn_next = tk.Button(nav_bar, text="Berikutnya ▶", font=("Segoe UI", 8), command=self._page_next)
        btn_next.pack(side=tk.LEFT, padx=2)

        btn_last = tk.Button(nav_bar, text="Akhir ⏭", font=("Segoe UI", 8), command=self._page_last)
        btn_last.pack(side=tk.LEFT, padx=2)

        tk.Label(nav_bar, text="| Tampilkan:", bg="#f8fafc", font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=(8, 2))

        btn_100 = tk.Button(nav_bar, text="100", font=("Segoe UI", 8), command=lambda: self._set_page_size(100))
        btn_100.pack(side=tk.LEFT, padx=1)

        btn_500 = tk.Button(nav_bar, text="500", font=("Segoe UI", 8), command=lambda: self._set_page_size(500))
        btn_500.pack(side=tk.LEFT, padx=1)

        btn_all = tk.Button(nav_bar, text="Semua Data", font=("Segoe UI", 8, "bold"), command=self._tampilkan_semua_data)
        btn_all.pack(side=tk.LEFT, padx=2)

        self.lbl_total_info = tk.Label(
            nav_bar,
            text="Total: 0 pesanan",
            bg="#f8fafc",
            fg="#475569",
            font=("Segoe UI", 9)
        )
        self.lbl_total_info.pack(side=tk.RIGHT, padx=6)

        # Event saat baris diklik
        self.tree.bind("<ButtonRelease-1>", self._on_tree_row_clicked)

    def _create_log_view(self, parent):
        log_container = tk.Frame(parent, bg="#ffffff", padx=4, pady=4)
        log_container.pack(fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(
            log_container,
            bg="#ffffff",
            fg="#0f172a",
            font=("Consolas", 10),
            bd=1,
            relief=tk.SOLID,
            padx=8,
            pady=8,
            wrap=tk.NONE
        )
        res_scroll_y = tk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.result_text.yview)
        res_scroll_x = tk.Scrollbar(log_container, orient=tk.HORIZONTAL, command=self.result_text.xview)
        self.result_text.configure(yscrollcommand=res_scroll_y.set, xscrollcommand=res_scroll_x.set)

        res_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        res_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _log_command(self, cmd_name, module_name, durasi_ms):
        log_line = "%-24s -> %-18s %8.2f ms\n" % (cmd_name, module_name, durasi_ms)
        self.cmd_text.insert(tk.END, log_line)
        self.cmd_text.see(tk.END)

    def _update_status(self, badge_text, info_text):
        self.status_badge.config(text=badge_text)
        self.status_info.config(text=info_text)

    def _on_tree_row_clicked(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        item_id = selected_items[0]
        values = self.tree.item(item_id, "values")
        if values and len(values) >= 9:
            msg = "Pesanan Dipilih: %s | Pelanggan: %s | Menu: %s | Harga: Rp %s | Prioritas: %s | Status: %s" % (
                values[0], values[1], values[3], values[4], values[5], values[8]
            )
            self.action_info_lbl.config(text=msg)

    def _refresh_table(self, highlight_idx=None):
        """Memperbarui baris tabel Treeview sesuai halaman saat ini."""
        self.tree.delete(*self.tree.get_children())
        total = self.sistem.array.size

        if total == 0:
            self.lbl_page_info.config(text="Halaman 0 / 0")
            self.lbl_total_info.config(text="Total: 0 pesanan")
            return

        if self.show_all_mode:
            start_idx = 0
            end_idx = total
            self.lbl_page_info.config(text="Semua Data")
        else:
            self.total_pages = (total + self.page_size - 1) // self.page_size
            if self.current_page > self.total_pages:
                self.current_page = self.total_pages
            if self.current_page < 1:
                self.current_page = 1

            start_idx = (self.current_page - 1) * self.page_size
            end_idx = min(start_idx + self.page_size, total)
            self.lbl_page_info.config(text="Halaman %d / %d" % (self.current_page, self.total_pages))

        self.lbl_total_info.config(text="Menampilkan %d - %d dari %d pesanan" % (start_idx + 1, end_idx, total))

        target_item_id = None
        for i in range(start_idx, end_idx):
            p = self.sistem.array.get(i)
            selesai_str = str(p.t_selesai_detik) if p.t_selesai_detik is not None else ""
            row_vals = (
                p.oid,
                p.pelanggan,
                p.resto,
                p.menu,
                str(p.harga),
                str(p.prioritas),
                str(p.t_masuk_detik),
                selesai_str,
                p.status
            )
            item_id = "row_%d" % i
            self.tree.insert("", tk.END, iid=item_id, values=row_vals)
            if highlight_idx is not None and i == highlight_idx:
                target_item_id = item_id

        if target_item_id:
            self.tree.selection_set(target_item_id)
            self.tree.see(target_item_id)

    def _page_first(self):
        self.show_all_mode = False
        self.current_page = 1
        self._refresh_table()

    def _page_prev(self):
        self.show_all_mode = False
        if self.current_page > 1:
            self.current_page -= 1
            self._refresh_table()

    def _page_next(self):
        self.show_all_mode = False
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._refresh_table()

    def _page_last(self):
        self.show_all_mode = False
        self.current_page = self.total_pages
        self._refresh_table()

    def _set_page_size(self, size):
        self.show_all_mode = False
        self.page_size = size
        self.current_page = 1
        self._refresh_table()

    def _tampilkan_semua_data(self):
        self.show_all_mode = True
        self._refresh_table()

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
                self.title_label.config(text="Array: Lihat Data Pesanan (Tabel Lengkap)")
                self.subtitle_label.config(text="Melihat seluruh daftar pesanan secara terstruktur atau melompat ke indeks ke-i (O(1)).")
            else:
                self.title_label.config(text="Linked List: Lihat Data Pesanan (Tabel Lengkap)")
                self.subtitle_label.config(text="Melihat seluruh daftar pesanan secara terstruktur atau melompat ke indeks ke-i (O(n) telusur).")

            row = tk.Frame(self.form_fields_frame, bg="#ffffff")
            row.pack(fill=tk.X, pady=2)

            tk.Label(row, text="Lompat ke Indeks (ke-i):", bg="#ffffff", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))
            idx_entry = tk.Entry(row, width=12, font=("Segoe UI", 9))
            idx_entry.insert(0, "0")
            idx_entry.pack(side=tk.LEFT, padx=(0, 10))

            btn_find = tk.Button(
                row,
                text="CARI & SOROT",
                bg="#1c3b57",
                fg="#ffffff",
                font=("Segoe UI", 9, "bold"),
                padx=12,
                pady=2,
                cursor="hand2",
                command=lambda: self._aksi_lihat_pesanan(is_arr, idx_entry.get().strip())
            )
            btn_find.pack(side=tk.LEFT, padx=(0, 10))

            btn_all = tk.Button(
                row,
                text="TAMPILKAN SEMUA DATA",
                bg="#0284c7",
                fg="#ffffff",
                font=("Segoe UI", 9, "bold"),
                padx=12,
                pady=2,
                cursor="hand2",
                command=self._tampilkan_semua_data
            )
            btn_all.pack(side=tk.LEFT)

            hint = tk.Label(
                self.form_fields_frame,
                text="masukkan nomor indeks (0 s/d n-1) untuk menguji kecepatan akses dan menyorot baris pada tabel di bawah",
                bg="#ffffff",
                fg="#64748b",
                font=("Segoe UI", 8)
            )
            hint.pack(anchor="w", pady=(2, 0))

        elif "HAPUS PESANAN" in menu_name:
            is_arr = "ARRAY" in menu_name
            if is_arr:
                self.title_label.config(text="Array: Hapus Pesanan ke-i")
                self.subtitle_label.config(text="pesanan dicabut dari barisan, menggeser sisa elemen ke kiri O(n).")
            else:
                self.title_label.config(text="Linked List: Hapus Pesanan ke-i")
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
                bg="#b91c1c",
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
                text="pesanan pada indeks yang ditentukan akan dihapus dan tabel akan diperbarui",
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
                text="pesanan baru akan disisipkan dan langsung ditampilkan pada tabel di bawah",
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

            self.current_page = 1
            self._refresh_table()
            self.notebook.select(0)

            msg = "Data berhasil dimuat: %d pesanan. Larik: %.2f ms (Kapasitas: %d) | Rantai: %.2f ms" % (
                total, ms_arr, self.sistem.array.capacity, ms_ll
            )
            self.action_info_lbl.config(text=msg)

            # Rincian teks pada tab Log
            self.result_text.delete("1.0", tk.END)
            txt = "=" * 60 + "\n"
            txt += "HASIL PEMUATAN DATA PESANAN\n"
            txt += "=" * 60 + "\n"
            txt += "Berkas sumber          : %s\n" % filepath
            txt += "Total data terbaca     : %d pesanan\n\n" % total
            txt += "1. STRUKTUR LARIK (ARRAY BERUKURAN TETAP 2x):\n"
            txt += "   - Ukuran data       : %d elemen\n" % self.sistem.array.size
            txt += "   - Kapasitas akhir   : %d slot\n" % self.sistem.array.capacity
            txt += "   - Total resize 2x   : %d kali penggandaan\n" % self.sistem.array.resize_count
            txt += "   - Durasi pemuatan   : %.2f ms (amortized O(1))\n\n" % ms_arr
            txt += "2. STRUKTUR RANTAI (LINKED LIST HEAD & TAIL):\n"
            txt += "   - Ukuran simpul     : %d simpul\n" % self.sistem.linklist.size
            txt += "   - Durasi pemuatan   : %.2f ms (O(1) via pointer tail)\n" % ms_ll
            txt += "=" * 60 + "\n"
            self.result_text.insert(tk.END, txt)

            badge = "[M1 - larik] %.2f ms" % ms_arr
            info = "Total: %d pesanan | Kapasitas: %d" % (total, self.sistem.array.capacity)
            self._update_status(badge, info)

        except Exception as e:
            messagebox.showerror("Galat Pemuatan", str(e))
            self._update_status("[ galat ]", str(e))

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
            info = "ARRAY: Pesanan pada indeks ke-%d (%s) ditemukan. Waktu akses: %.2f ms (O(1) langsung memori)." % (idx, p.oid, ms)
        else:
            p, ms, trav = self.sistem.linklist_lihat(idx)
            modul = "M1 - linked list"
            cmd = "linklist_get"
            info = "LINKED LIST: Pesanan pada indeks ke-%d (%s) ditemukan. Waktu: %.2f ms (%d simpul ditelusuri - O(n))." % (idx, p.oid, ms, trav)

        self._log_command(cmd, modul, ms)
        self._update_status("[%s] %.2f ms" % (modul, ms), "Lihat pesanan indeks ke-%d" % idx)
        self.action_info_lbl.config(text=info)

        # Buka tab tabel dan sorot baris yang dicari
        self.notebook.select(0)
        if not self.show_all_mode:
            target_page = (idx // self.page_size) + 1
            self.current_page = target_page
        self._refresh_table(highlight_idx=idx)

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
            info = "ARRAY: Pesanan %s dicabut dari indeks ke-%d. Pergeseran: %d elemen (O(n)). Waktu: %.2f ms." % (p.oid, idx, shifts, ms)
        else:
            p, ms, trav = self.sistem.linklist_hapus(idx, sinkron=True)
            modul = "M1 - linked list"
            cmd = "linklist_delete"
            info = "LINKED LIST: Pesanan %s dicabut dari indeks ke-%d. Penelusuran: %d simpul (O(n)). Waktu: %.2f ms." % (p.oid, idx, trav, ms)

        self._log_command(cmd, modul, ms)
        self._update_status("[%s] %.2f ms" % (modul, ms), "Hapus pesanan %s" % p.oid)
        self.action_info_lbl.config(text=info)

        self.notebook.select(0)
        self._refresh_table()

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

        target_highlight_idx = 0
        if is_arr:
            modul = "M1 - array"
            if jenis == "REGULER":
                cmd = "array_append_reguler"
                p, ms, shifts = self.sistem.array_tambah_reguler(p, sinkron=True)
                penjelasan = "masuk barisan paling belakang: %d elemen digeser (O(1) amortized)." % shifts
                target_highlight_idx = self.sistem.array.size - 1
            elif jenis == "PRIORITAS":
                cmd = "array_insert_prioritas"
                p, ms, shifts = self.sistem.array_tambah_prioritas(p, sinkron=True)
                penjelasan = "menyerobot ke tengah barisan: %d elemen digeser ke kanan (O(n))." % shifts
                target_highlight_idx = (self.sistem.array.size - 1) // 2
            else:  # VIP
                cmd = "array_insert_vip"
                p, ms, shifts = self.sistem.array_tambah_vip(p, sinkron=True)
                penjelasan = "langsung ke urutan pertama (indeks 0): %d elemen digeser ke kanan (O(n))." % shifts
                target_highlight_idx = 0

            info = "ARRAY: Pesanan %s (%s) berhasil ditambahkan. %s Waktu: %.2f ms." % (p.oid, jenis, penjelasan, ms)

        else:
            modul = "M1 - linked list"
            if jenis == "REGULER":
                cmd = "linklist_append_reguler"
                p, ms, trav = self.sistem.linklist_tambah_reguler(p, sinkron=True)
                penjelasan = "masuk paling belakang via tail: %d simpul ditelusuri (O(1))." % trav
                target_highlight_idx = self.sistem.linklist.size - 1
            elif jenis == "PRIORITAS":
                cmd = "linklist_insert_prioritas"
                p, ms, trav = self.sistem.linklist_tambah_prioritas(p, sinkron=True)
                penjelasan = "menyerobot ke tengah: %d simpul ditelusuri (O(n))." % trav
                target_highlight_idx = (self.sistem.linklist.size - 1) // 2
            else:  # VIP
                cmd = "linklist_prepend_vip"
                p, ms, trav = self.sistem.linklist_tambah_vip(p, sinkron=True)
                penjelasan = "langsung ke urutan pertama (head): %d simpul ditelusuri (O(1))." % trav
                target_highlight_idx = 0

            info = "LINKED LIST: Pesanan %s (%s) berhasil ditambahkan. %s Waktu: %.2f ms." % (p.oid, jenis, penjelasan, ms)

        self._log_command(cmd, modul, ms)
        self._update_status("[%s] %.2f ms" % (modul, ms), "Tambah pesanan %s (%s)" % (p.oid, jenis))
        self.action_info_lbl.config(text=info)

        # Tampilkan di tabel dan sorot baris baru
        self.notebook.select(0)
        if not self.show_all_mode:
            target_page = (target_highlight_idx // self.page_size) + 1
            self.current_page = target_page
        self._refresh_table(highlight_idx=target_highlight_idx)

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
        self.notebook.select(1)  # Buka tab log / hasil adu performa

        self._log_command("benchmark_m1", "M1 - adu performa", t_arr_vip)
        self._update_status("[M1 - benchmark] Selesai", "Adu performa Array vs Linked List berhasil.")
        self.action_info_lbl.config(text="Adu performa selesai. Hasil rincian ditampilkan pada tab Log & Adu Performa.")

    def _placeholder_milestone(self, m_name):
        messagebox.showinfo("Informasi Milestone", "Fitur %s akan dikembangkan pada tahapan tugas berikutnya." % m_name)
