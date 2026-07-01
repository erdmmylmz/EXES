import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class CampbellApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campbell Diagram Generator")
        self.root.geometry("1200x700")
        
        # Ana Grid Düzeni
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.columnconfigure(2, weight=2)
        self.root.rowconfigure(1, weight=1)
        
        self.create_widgets()

    def create_widgets(self):
        # --- SOL PANEL: Mode & Sol Butonlar ---
        left_frame = ttk.LabelFrame(self.root, text="Data Source / Modes")
        left_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        
        tk.Label(left_frame, text="Mode (Hz):").pack(anchor="w", padx=5, pady=2)
        self.mode_text = tk.Text(left_frame, width=15, height=15)
        self.mode_text.pack(padx=5, pady=5, fill="both", expand=True)
        self.mode_text.insert("1.0", "35\n68\n75") # Örnek veriler
        
        self.btn_create = ttk.Button(left_frame, text="Create")
        self.btn_create.pack(fill="x", padx=5, pady=2)
        
        self.btn_load = ttk.Button(left_frame, text="Load")
        self.btn_load.pack(fill="x", padx=5, pady=2)

        # --- ORTA PANEL: Engine Speed & EO ---
        mid_frame = ttk.LabelFrame(self.root, text="Engine Speed & Margin Definition")
        mid_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        tk.Label(mid_frame, text="EO (Engine Orders - virgülle ayırın):").grid(row=0, column=0, columnspan=3, anchor="w", padx=5, pady=2)
        self.eo_entry = ttk.Entry(mid_frame)
        self.eo_entry.grid(row=1, column=0, columnspan=3, fill="x", padx=5, pady=2)
        self.eo_entry.insert(0, "1, 2, 3, 4")

        # Hız ve Margin Girişleri (3 adet dinamik satır)
        self.speed_inputs = []
        for i in range(3):
            row_idx = i * 3 + 2
            tk.Label(mid_frame, text=f"Engine Speed {i+1} (RPM):").grid(row=row_idx, column=0, anchor="w", padx=5, pady=2)
            spd = ttk.Entry(mid_frame, width=10)
            spd.grid(row=row_idx, column=1, padx=5, pady=2)
            spd.insert(0, "0")
            
            tk.Label(mid_frame, text="Margin (%):").grid(row=row_idx+1, column=0, anchor="w", padx=5, pady=2)
            mrgn = ttk.Entry(mid_frame, width=10)
            mrgn.grid(row=row_idx+1, column=1, padx=5, pady=2)
            mrgn.insert(0, "0")
            
            low_var = tk.BooleanVar()
            upp_var = tk.BooleanVar()
            ttk.Checkbutton(mid_frame, text="Lower", variable=low_var).grid(row=row_idx+1, column=2, padx=2)
            ttk.Checkbutton(mid_frame, text="Upper", variable=upp_var).grid(row=row_idx+1, column=3, padx=2)
            
            self.speed_inputs.append({"speed": spd, "margin": mrgn, "lower": low_var, "upper": upp_var})

        # --- SAĞ PANEL: Info Box ---
        right_frame = ttk.LabelFrame(self.root, text="Information")
        right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        info_text = (
            "Program Name: Campbell Diagram Generator\n"
            "Version: 1.0.0\n"
            "Description: This tool allows users to draw campbell diagram\n\n"
            "Instructions:\n"
            "1. Enter mode frequencies (Hz) into the left box.\n"
            "2. Enter Engine Orders (separated by commas).\n"
            "3. Click 'Run' to generate plot."
        )
        info_box = tk.Text(right_frame, width=35, height=12, wrap="word")
        info_box.insert("1.0", info_text)
        info_box.config(state="disabled")
        info_box.pack(padx=5, pady=5, fill="both", expand=True)

        # --- BÜYÜK RUN BUTONU ---
        self.btn_run = tk.Button(self.root, text="Run", bg="green", fg="white", font=("Arial", 14, "bold"), command=self.generate_plot)
        self.btn_run.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # --- ALT PANEL: Grafik Çizim Alanı ---
        self.plot_frame = ttk.LabelFrame(self.root, text="Campbell Diagram Plot")
        self.plot_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.root.rowconfigure(2, weight=3)

        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_widget().pack(fill="both", expand=True)

    def generate_plot(self):
        self.ax.clear()
        
        # Modları çek
        try:
            modes = [float(x) for x in self.mode_text.get("1.0", "end").split() if x.strip()]
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli mod frekansları (Hz) girin.")
            return

        # EO verilerini çek
        try:
            eo_list = [float(x.strip()) for x in self.eo_entry.get().split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("Hata", "Engine Orders formatı hatalı. Örn: 1, 2, 3")
            return

        max_rpm = 4000
        rpms = np.linspace(0, max_rpm, 100)

        # Doğrusal EO çizgilerini çiz (Hz = RPM * EO / 60)
        for eo in eo_list:
            freqs = (rpms * eo) / 60.0
            self.ax.plot(rpms, freqs, label=f"Order {eo}")

        # Yatay Mod Çizgilerini Çiz
        for idx, mode in enumerate(modes):
            self.ax.axhline(y=mode, color='black', linestyle='--', alpha=0.7)
            self.ax.text(100, mode + 2, f"Mode {idx+1} ({mode} Hz)", fontsize=9)

        # Arayüz ayarları
        self.ax.set_xlim(0, max_rpm)
        self.ax.set_ylim(0, max(modes + [100]) * 1.3)
        self.ax.set_xlabel("Engine Speed (RPM)")
        self.ax.set_ylabel("Frequency (Hz)")
        self.ax.grid(True, which='both', linestyle=':', alpha=0.5)
        self.ax.legend(loc="upper left")
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = CampbellApp(root)
    root.mainloop()
