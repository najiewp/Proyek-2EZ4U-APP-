# ==============================================================================
# PROYEK "2EZ4U APP" - STRUKTUR DATA & ANALISA ALGORITMA (EC234303)
# Modul: backend/m2_antrean.py
# Milestone 2: Antrean Melingkar (Circular Queue) + Tumpukan (Stack Undo/Redo/Kasir)
# Kepatuhan: Struktur data mandiri murni primitif
# ==============================================================================

import time
import csv
from backend.m1_pesanan import Pesanan


class Stack:
    """
    Implementasi Tumpukan (Stack LIFO) buatan sendiri di atas larik primitif.
    Menerapkan kapasitas awal dengan penggandaan 2x saat penuh.
    """
    def __init__(self, initial_capacity=16):
        init_cap = initial_capacity if initial_capacity > 0 else 16
        self.capacity = init_cap
        self.data = [None] * self.capacity
        self.top = 0

    def push(self, x):
        """Mendorong elemen ke puncak tumpukan. O(1) amortized."""
        if self.top == self.capacity:
            new_cap = self.capacity * 2
            new_data = [None] * new_cap
            for i in range(self.top):
                new_data[i] = self.data[i]
            self.data = new_data
            self.capacity = new_cap
        self.data[self.top] = x
        self.top += 1

    def pop(self):
        """Mengambil dan menghapus elemen dari puncak tumpukan. O(1)."""
        if self.top == 0:
            raise IndexError("Tumpukan kosong (Stack underflow)")
        self.top -= 1
        val = self.data[self.top]
        self.data[self.top] = None
        return val

    def peek(self):
        """Melihat elemen di puncak tumpukan tanpa menghapusnya. O(1)."""
        if self.top == 0:
            return None
        return self.data[self.top - 1]

    def is_empty(self):
        return self.top == 0

    def size(self):
        return self.top

    def clear(self):
        self.capacity = 16
        self.data = [None] * self.capacity
        self.top = 0

    def to_string(self):
        parts = []
        for i in range(self.top):
            parts.append(str(self.data[i]))
        return " ".join(parts)

    def __len__(self):
        return self.top


class KasirPostfix:
    """
    Mesin Kasir: Evaluator struk aritmetika berbasis Stack.
    1. Mengubah ekspresi infix menjadi postfix (Algoritma Shunting-Yard).
    2. Mengevaluasi ekspresi postfix menjadi total harga rupiah.
    Menyimpan transkrip baris demi baris persis sesuai spesifikasi panduan.
    """
    @staticmethod
    def _prioritas(op):
        if op == "*" or op == "/":
            return 2
        if op == "+" or op == "-":
            return 1
        return 0

    @staticmethod
    def pisah_token(ekspresi):
        """Memecah token dengan angka berdigit banyak (12000 utuh, bukan 1 lalu 2)."""
        tokens = []
        i = 0
        n = len(ekspresi)
        while i < n:
            ch = ekspresi[i]
            if ch == " " or ch == "\t" or ch == "\r" or ch == "\n":
                i += 1
                continue
            if ch.isdigit():
                start = i
                while i < n and ekspresi[i].isdigit():
                    i += 1
                tokens.append(ekspresi[start:i])
            elif ch in ("+", "-", "*", "/", "(", ")"):
                tokens.append(ch)
                i += 1
            else:
                i += 1
        return tokens

    @staticmethod
    def ke_postfix(ekspresi):
        """
        Tahap 1: Mengubah infix ke postfix menggunakan stack operator.
        Mengembalikan tuple: (postfix_tokens, daftar_langkah_transkrip).
        Tiap langkah: (no_langkah, token, tindakan, stack_str, output_str)
        """
        tokens = KasirPostfix.pisah_token(ekspresi)
        stack = Stack(16)
        output = []
        langkah_list = []
        step_num = 1

        for token in tokens:
            tindakan = ""
            if token.isdigit():
                output.append(token)
                tindakan = "operand, langsung ke output"
                stack_str = stack.to_string() if not stack.is_empty() else "kosong"
                out_str = " ".join(output)
                step_id = "1.%d" % step_num
                langkah_list.append((step_id, token, tindakan, stack_str, out_str))
                step_num += 1

            elif token == "(":
                stack.push(token)
                tindakan = "push ( ke stack"
                stack_str = stack.to_string()
                out_str = " ".join(output)
                step_id = "1.%d" % step_num
                langkah_list.append((step_id, token, tindakan, stack_str, out_str))
                step_num += 1

            elif token == ")":
                # Pop sampai bertemu '(', lalu buang '('
                while not stack.is_empty() and stack.peek() != "(":
                    op = stack.pop()
                    output.append(op)
                if not stack.is_empty() and stack.peek() == "(":
                    stack.pop()  # buang '('
                tindakan = "pop sampai ( , buang ("
                stack_str = stack.to_string() if not stack.is_empty() else "kosong"
                out_str = " ".join(output)
                step_id = "1.%d" % step_num
                langkah_list.append((step_id, token, tindakan, stack_str, out_str))
                step_num += 1

            elif token in ("+", "-", "*", "/"):
                # Pop operator yang lebih kuat atau sama kuat
                p_cur = KasirPostfix._prioritas(token)
                popped_list = []
                while not stack.is_empty():
                    top_op = stack.peek()
                    if top_op == "(":
                        break
                    p_top = KasirPostfix._prioritas(top_op)
                    if p_top >= p_cur:
                        popped_list.append(stack.pop())
                    else:
                        break
                for pop_op in popped_list:
                    output.append(pop_op)
                stack.push(token)
                if len(popped_list) > 0:
                    tindakan = "pop %s (sama/lebih kuat), push %s" % (" ".join(popped_list), token)
                else:
                    tindakan = "push %s" % token
                stack_str = stack.to_string()
                out_str = " ".join(output)
                step_id = "1.%d" % step_num
                langkah_list.append((step_id, token, tindakan, stack_str, out_str))
                step_num += 1

        # Sisa stack dikeluarkan
        while not stack.is_empty():
            op = stack.pop()
            if op != "(":
                output.append(op)

        step_id = "1.akhir"
        stack_str = "kosong"
        out_str = " ".join(output)
        langkah_list.append((step_id, "akhir", "pop sisa stack", stack_str, out_str))

        return (output, langkah_list)

    @staticmethod
    def hitung(postfix_tokens):
        """
        Tahap 2: Mengevaluasi postfix menggunakan stack angka.
        Mengembalikan tuple: (total_nilai, daftar_langkah_transkrip).
        Urutan pop menentukan kebenaran pengurangan dan pembagian:
        b = pop() (operand kanan), a = pop() (operand kiri) -> a op b.
        """
        stack = Stack(16)
        langkah_list = []
        step_num = 1

        for token in postfix_tokens:
            if token.isdigit():
                val = int(token)
                stack.push(val)
                tindakan = "operand, push %d" % val
                stack_str = stack.to_string()
                step_id = "2.%d" % step_num
                langkah_list.append((step_id, token, tindakan, stack_str, ""))
                step_num += 1
            elif token in ("+", "-", "*", "/"):
                if stack.size() < 2:
                    raise ValueError("Ekspresi postfix tidak valid")
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    res = a + b
                elif token == "-":
                    res = a - b
                elif token == "*":
                    res = a * b
                elif token == "/":
                    res = a // b if b != 0 else 0
                stack.push(res)
                tindakan = "pop %d dan %d -> %d %s %d = %d" % (b, a, a, token, b, res)
                stack_str = stack.to_string()
                step_id = "2.%d" % step_num
                langkah_list.append((step_id, token, tindakan, stack_str, str(res)))
                step_num += 1

        total = stack.pop() if not stack.is_empty() else 0
        return (total, langkah_list)


class AntreanNaif:
    """
    Antrean Naif (Naive Queue) di atas larik linier biasa.
    - enqueue: menempel di ujung belakang (O(1) amortized).
    - dequeue: mengambil indeks 0 (pop(0)), lalu menggeser SELURUH sisa elemen ke kiri (O(n)).
    Menyimpan penghitung total pergeseran elemen.
    """
    def __init__(self, initial_capacity=16):
        init_cap = initial_capacity if initial_capacity > 0 else 16
        self.capacity = init_cap
        self.data = [None] * self.capacity
        self.count = 0
        self.total_geseran = 0
        self.last_shift_count = 0

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self.count):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def enqueue(self, x):
        """Menambah pesanan di belakang antrean. O(1) amortized. 0 geseran."""
        if self.count == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.count] = x
        self.count += 1
        self.last_shift_count = 0
        return 0

    def dequeue(self):
        """
        Mengambil elemen terdepan (indeks 0).
        Menggeser seluruh (count - 1) elemen ke kiri satu petak. O(n).
        """
        if self.count == 0:
            return None
        item = self.data[0]
        shifts = 0
        for i in range(1, self.count):
            self.data[i - 1] = self.data[i]
            shifts += 1
        self.data[self.count - 1] = None
        self.count -= 1
        self.total_geseran += shifts
        self.last_shift_count = shifts
        return item

    def dequeue_banyak(self, k):
        """Melayani k pesanan sekaligus, mengembalikan (list_pesanan, total_shifts)."""
        hasil = []
        total_shifts = 0
        batas = min(k, self.count)
        for _ in range(batas):
            p = self.dequeue()
            if p is not None:
                hasil.append(p)
                total_shifts += self.last_shift_count
        return (hasil, total_shifts)

    def enqueue_depan(self, x):
        """Untuk keperluan UNDO dequeue: mengembalikan elemen ke depan antrean naif."""
        if self.count == self.capacity:
            self._resize(self.capacity * 2)
        for i in range(self.count, 0, -1):
            self.data[i] = self.data[i - 1]
        self.data[0] = x
        self.count += 1

    def pop_belakang(self):
        """Untuk keperluan UNDO enqueue: mencabut elemen dari belakang antrean naif."""
        if self.count == 0:
            return None
        self.count -= 1
        val = self.data[self.count]
        self.data[self.count] = None
        return val

    def get(self, i):
        """Mengambil elemen pada indeks ke-i dari depan antrean (0 = depan). O(1)."""
        if i < 0 or i >= self.count:
            return None
        return self.data[i]

    def peek(self):
        if self.count == 0:
            return None
        return self.data[0]

    def is_empty(self):
        return self.count == 0

    def clear(self):
        self.capacity = 16
        self.data = [None] * self.capacity
        self.count = 0
        self.total_geseran = 0
        self.last_shift_count = 0

    def __len__(self):
        return self.count


class AntreanMelingkar:
    """
    Antrean Melingkar (Circular Queue) berbasis penunjuk front, rear, dan count.
    - enqueue: data[rear] = x; rear = (rear + 1) % K; count += 1 (O(1)).
    - dequeue: x = data[front]; front = (front + 1) % K; count -= 1 (O(1)).
    Tidak ada satu pun elemen yang digeser (0 elemen digeser).
    Alasan adanya variabel 'count':
    Jika hanya menyimpan front dan rear, kondisi kosong dan kondisi penuh sama-sama
    menghasilkan (front == rear) sehingga ambigu dan tidak dapat dibedakan.
    Dengan variabel count, kosong (count == 0) dan penuh (count == capacity) teridentifikasi pasti.
    """
    def __init__(self, capacity=16):
        init_cap = capacity if capacity > 0 else 16
        self.capacity = init_cap
        self.data = [None] * self.capacity
        self.front = 0
        self.rear = 0
        self.count = 0
        self.last_shift_count = 0

    def _resize(self, new_capacity):
        """Alokasi petak baru dan menata ulang dari urutan front melingkar ke linier baru."""
        new_data = [None] * new_capacity
        for i in range(self.count):
            idx = (self.front + i) % self.capacity
            new_data[i] = self.data[idx]
        self.data = new_data
        self.front = 0
        self.rear = self.count
        self.capacity = new_capacity

    def enqueue(self, x):
        """Menambah pesanan di belakang antrean melingkar. O(1). 0 elemen digeser."""
        if self.count == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.capacity
        self.count += 1
        self.last_shift_count = 0
        return 0

    def dequeue(self):
        """Mengambil pesanan dari depan antrean melingkar. O(1). 0 elemen digeser."""
        if self.count == 0:
            return None
        item = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        self.last_shift_count = 0
        return item

    def dequeue_banyak(self, k):
        """Melayani k pesanan sekaligus, mengembalikan (list_pesanan, total_shifts=0)."""
        hasil = []
        batas = min(k, self.count)
        for _ in range(batas):
            p = self.dequeue()
            if p is not None:
                hasil.append(p)
        return (hasil, 0)

    def enqueue_depan(self, x):
        """Untuk keperluan UNDO dequeue: mengembalikan elemen ke depan antrean melingkar. O(1)."""
        if self.count == self.capacity:
            self._resize(self.capacity * 2)
        self.front = (self.front - 1 + self.capacity) % self.capacity
        self.data[self.front] = x
        self.count += 1

    def pop_belakang(self):
        """Untuk keperluan UNDO enqueue: mencabut elemen paling belakang antrean melingkar. O(1)."""
        if self.count == 0:
            return None
        self.rear = (self.rear - 1 + self.capacity) % self.capacity
        item = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return item

    def get(self, i):
        """Mengambil elemen pada urutan ke-i relatif terhadap front (0 = front). O(1)."""
        if i < 0 or i >= self.count:
            return None
        idx = (self.front + i) % self.capacity
        return self.data[idx]

    def peek(self):
        if self.count == 0:
            return None
        return self.data[self.front]

    def is_empty(self):
        return self.count == 0

    def clear(self):
        self.capacity = 16
        self.data = [None] * self.capacity
        self.front = 0
        self.rear = 0
        self.count = 0
        self.last_shift_count = 0

    def __len__(self):
        return self.count


class CatatanAksi:
    """
    Menyimpan rekaman aksi antrean untuk keperluan tumpukan Undo dan Redo.
    Aturan: Simpan daftar pesanan, bukan hanya hitungannya saja.
    """
    __slots__ = ('tipe', 'pesanan_list')

    def __init__(self, tipe, pesanan_list):
        self.tipe = tipe              # 'ENQUEUE' atau 'DEQUEUE'
        self.pesanan_list = pesanan_list


class SistemAntreanM2:
    """
    Pengelola Backend Milestone 2.
    Mengelola dua struktur antrean sekaligus:
    1. AntreanNaif (Larik + pop(0))
    2. AntreanMelingkar (Circular Queue berpenunjuk)
    Serta dua tumpukan:
    1. Undo Stack
    2. Redo Stack
    """
    def __init__(self):
        self.antrean_naif = AntreanNaif(32768)
        self.antrean_circular = AntreanMelingkar(32768)
        self.undo_stack = Stack(16)
        self.redo_stack = Stack(16)
        self.max_id_num = 200000
        self.is_loaded = False

    def muat_dari_csv(self, filepath):
        """
        Membaca hanya pesanan yang berstatus 'ANTRE' dari CSV (19.850 data),
        dan memuatnya ke KEDUA antrean secara bersamaan agar perbandingan jujur.
        """
        self.antrean_naif.clear()
        self.antrean_circular.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()

        t0 = time.perf_counter()
        count = 0
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # lewati header
            for row in reader:
                if len(row) < 9:
                    continue
                status = row[8].strip()
                if status == "ANTRE":
                    p = Pesanan(row[0], row[1], row[2], row[3], row[4],
                                row[5], row[6], row[7], row[8])
                    self.antrean_naif.enqueue(p)
                    self.antrean_circular.enqueue(p)
                    count += 1
                    oid_str = row[0]
                    if oid_str.startswith("O-"):
                        try:
                            num = int(oid_str[2:])
                            if num > self.max_id_num:
                                self.max_id_num = num
                        except ValueError:
                            pass
        t1 = time.perf_counter()
        self.is_loaded = True
        durasi_ms = (t1 - t0) * 1000.0
        return (count, durasi_ms)

    def generate_oid(self):
        self.max_id_num += 1
        return "O-%06d" % self.max_id_num

    def enqueue_kedua(self, p):
        """
        Menambahkan pesanan baru ke belakang KEDUA antrean sekaligus.
        Mendorong aksi ke tumpukan undo dan MENGOSONGKAN tumpukan redo.
        """
        t0 = time.perf_counter()
        self.antrean_naif.enqueue(p)
        self.antrean_circular.enqueue(p)
        t1 = time.perf_counter()
        durasi_ms = (t1 - t0) * 1000.0

        # Catat ke Undo dan kosongkan Redo
        aksi = CatatanAksi("ENQUEUE", [p])
        self.undo_stack.push(aksi)
        self.redo_stack.clear()

        return (p, durasi_ms)

    def dequeue_naif(self, k=1):
        """
        Melayani k pesanan dari Antrean Naif.
        Mencatat durasi dan jumlah pergeseran elemen.
        """
        t0 = time.perf_counter()
        hasil, shifts = self.antrean_naif.dequeue_banyak(k)
        t1 = time.perf_counter()
        durasi_ms = (t1 - t0) * 1000.0
        return (hasil, shifts, durasi_ms)

    def dequeue_circular(self, k=1, catat_undo=True):
        """
        Melayani k pesanan dari Antrean Melingkar.
        Durasi konstan O(1) per pesanan, 0 elemen digeser.
        """
        t0 = time.perf_counter()
        hasil, shifts = self.antrean_circular.dequeue_banyak(k)
        t1 = time.perf_counter()
        durasi_ms = (t1 - t0) * 1000.0
        if catat_undo and len(hasil) > 0:
            self.catat_dequeue_ke_undo(hasil)
        return (hasil, shifts, durasi_ms)

    def catat_dequeue_ke_undo(self, daftar_pesanan):
        """Mencatat aksi dequeue ke Undo dan mengosongkan Redo."""
        if len(daftar_pesanan) > 0:
            aksi = CatatanAksi("DEQUEUE", daftar_pesanan)
            self.undo_stack.push(aksi)
            self.redo_stack.clear()

    def undo_last(self):
        """
        Membatalkan efek aksi terakhir.
        Pop dari undo -> jalankan kebalikannya -> push ke redo.
        Mengembalikan tuple: (aksi_dibatalkan, durasi_ms, pesan_penjelasan).
        """
        if self.undo_stack.is_empty():
            return (None, 0.0, "Tumpukan undo kosong, tidak ada yang bisa dibatalkan.")

        t0 = time.perf_counter()
        aksi = self.undo_stack.pop()

        if aksi.tipe == "ENQUEUE":
            # Kebalikan enqueue: keluarkan lagi pesanan dari belakang kedua antrean
            p_naif = self.antrean_naif.pop_belakang()
            p_circ = self.antrean_circular.pop_belakang()
            p_target = p_circ if p_circ is not None else p_naif
            pesan = "%s dikeluarkan lagi dari belakang antrean" % (
                p_target.oid if p_target else "Pesanan"
            )

        elif aksi.tipe == "DEQUEUE":
            # Kebalikan dequeue: kembalikan seluruh pesanan ke DEPAN antrean circular (O(1))
            n_items = len(aksi.pesanan_list)
            for i in range(n_items - 1, -1, -1):
                p = aksi.pesanan_list[i]
                self.antrean_circular.enqueue_depan(p)
            pesan = "%d pesanan dikembalikan ke DEPAN antrean circular" % n_items
        else:
            pesan = "Aksi tidak dikenali."

        t1 = time.perf_counter()
        durasi_ms = (t1 - t0) * 1000.0

        # Masukkan aksi ke tumpukan Redo
        self.redo_stack.push(aksi)
        return (aksi, durasi_ms, pesan)

    def redo_last(self):
        """
        Mengerjakan ulang aksi yang baru saja dibatalkan.
        Pop dari redo -> kerjakan lagi aksi aslinya -> push kembali ke undo.
        Mengembalikan tuple: (aksi_diulang, durasi_ms, pesan_penjelasan).
        """
        if self.redo_stack.is_empty():
            return (None, 0.0, "Tumpukan redo kosong, tidak ada yang bisa diulang.")

        t0 = time.perf_counter()
        aksi = self.redo_stack.pop()

        if aksi.tipe == "ENQUEUE":
            # Kerjakan lagi aksi aslinya: masukkan kembali ke belakang kedua antrean
            for p in aksi.pesanan_list:
                self.antrean_naif.enqueue(p)
                self.antrean_circular.enqueue(p)
            pesan = "%s masuk kembali ke belakang antrean" % aksi.pesanan_list[0].oid

        elif aksi.tipe == "DEQUEUE":
            # Kerjakan lagi aksi aslinya: keluarkan lagi pesanan dari depan antrean circular
            n_items = len(aksi.pesanan_list)
            self.antrean_circular.dequeue_banyak(n_items)
            pesan = "%d pesanan keluar lagi dari antrean circular" % n_items
        else:
            pesan = "Aksi tidak dikenali."

        t1 = time.perf_counter()
        durasi_ms = (t1 - t0) * 1000.0

        # Masukkan kembali ke tumpukan Undo
        self.undo_stack.push(aksi)
        return (aksi, durasi_ms, pesan)

    def sinkronkan_antrean(self):
        """
        Menyinkronkan isi antrean naif agar sama persis dengan antrean circular saat ini.
        Sangat berguna setelah demonstrasi pergeseran naif untuk menguji kembali adu performa.
        """
        self.antrean_naif.clear()
        if self.antrean_naif.capacity < self.antrean_circular.capacity:
            self.antrean_naif._resize(self.antrean_circular.capacity)
        for i in range(self.antrean_circular.count):
            p = self.antrean_circular.get(i)
            self.antrean_naif.enqueue(p)
        self.antrean_naif.total_geseran = 0
        self.antrean_naif.last_shift_count = 0

    def stats(self):
        """Statistik antrean lengkap sesuai poin 9 panduan M2."""
        return (
            len(self.antrean_naif),
            len(self.antrean_circular),
            self.antrean_circular.capacity,
            self.antrean_naif.total_geseran,
            len(self.undo_stack),
            len(self.redo_stack)
        )
