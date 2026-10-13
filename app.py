# ==============================================================================
# PROYEK "2EZ4U APP" - STRUKTUR DATA & ANALISA ALGORITMA (EC234303)
# Berkas Utama: app.py
# Menjalankan Aplikasi Desktop Tkinter
# ==============================================================================

import tkinter as tk
import sys
from frontend.ui import AppUI


def main():
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
