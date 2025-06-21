import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from algorithms import first_fit, best_fit, worst_fit, brute_force
import random
from utils import validate_input

class PackingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("1D Packing Problem Solver")
        self.geometry("900x700")
        self.configure(bg="#f0f0f0")
        
        self.create_widgets()
        self.style_ui()
    
    def style_ui(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10), padding=5)
        self.style.configure("TEntry", padding=5)
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        
        self.primary_color = "#4a6fa5"
        self.secondary_color = "#166088"
        self.accent_color = "#4fc3f7"
        
        self.style.configure("Primary.TButton", background=self.primary_color, foreground="white")
        self.style.configure("Secondary.TButton", background=self.secondary_color, foreground="white")
    
    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="1D Bin Packing Problem", style="Header.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding=10)
        config_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        ttk.Label(config_frame, text="Bin Capacity:").grid(row=0, column=0, sticky="w")
        self.bin_capacity_entry = ttk.Entry(config_frame)
        self.bin_capacity_entry.grid(row=0, column=1, pady=5)
        self.bin_capacity_entry.insert(0, "10")
        
        ttk.Label(config_frame, text="Items (comma separated):").grid(row=1, column=0, sticky="w")
        self.items_entry = ttk.Entry(config_frame, width=30)
        self.items_entry.grid(row=1, column=1, pady=5)
        self.items_entry.insert(0, "4, 5, 6, 3, 2, 1, 7")
        
        ttk.Button(config_frame, text="Generate Random", command=self.generate_random).grid(row=2, column=0, columnspan=2, pady=10, sticky="we")
        ttk.Button(config_frame, text="Clear", command=self.clear_inputs).grid(row=3, column=0, columnspan=2, pady=5, sticky="we")
        
        algo_frame = ttk.LabelFrame(main_frame, text="Algorithms", padding=10)
        algo_frame.grid(row=1, column=1, sticky="nsew")
        
        ttk.Button(algo_frame, text="First Fit", command=lambda: self.run_algorithm("First Fit"), style="Primary.TButton").grid(row=0, column=0, pady=5, sticky="we")
        ttk.Button(algo_frame, text="Best Fit", command=lambda: self.run_algorithm("Best Fit"), style="Primary.TButton").grid(row=1, column=0, pady=5, sticky="we")
        ttk.Button(algo_frame, text="Worst Fit", command=lambda: self.run_algorithm("Worst Fit"), style="Primary.TButton").grid(row=2, column=0, pady=5, sticky="we")
        ttk.Button(algo_frame, text="Brute Force", command=lambda: self.run_algorithm("Brute Force"), style="Secondary.TButton").grid(row=3, column=0, pady=5, sticky="we")
        
        result_frame = ttk.LabelFrame(main_frame, text="Results", padding=10)
        result_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=80, height=15, font=("Consolas", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def generate_random(self):
        bin_capacity = random.randint(10, 20)
        num_items = random.randint(5, 15)
        items = [random.randint(1, bin_capacity) for _ in range(num_items)]
        
        self.bin_capacity_entry.delete(0, tk.END)
        self.bin_capacity_entry.insert(0, str(bin_capacity))
        
        self.items_entry.delete(0, tk.END)
        self.items_entry.insert(0, ", ".join(map(str, items)))
    
    def clear_inputs(self):
        self.bin_capacity_entry.delete(0, tk.END)
        self.items_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
    
    def run_algorithm(self, algorithm_name):
        try:
            bin_capacity = validate_input(self.bin_capacity_entry.get(), "Bin capacity")
            items_str = self.items_entry.get()
            
            if not items_str:
                raise ValueError("Items list cannot be empty")
            
            items = [validate_input(item.strip(), f"Item {i+1}") for i, item in enumerate(items_str.split(","))]
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Running {algorithm_name} algorithm...\n")
            self.result_text.insert(tk.END, f"Bin capacity: {bin_capacity}\n")
            self.result_text.insert(tk.END, f"Items: {items}\n\n")
            
            if algorithm_name == "First Fit":
                bins = first_fit(items, bin_capacity)
            elif algorithm_name == "Best Fit":
                bins = best_fit(items, bin_capacity)
            elif algorithm_name == "Worst Fit":
                bins = worst_fit(items, bin_capacity)
            elif algorithm_name == "Brute Force":
                min_bins = brute_force(items, bin_capacity)
                self.result_text.insert(tk.END, f"Minimum number of bins needed: {min_bins}\n")
                return
            
            self.result_text.insert(tk.END, f"Number of bins used: {len(bins)}\n")
            for i, bin in enumerate(bins, 1):
                self.result_text.insert(tk.END, f"Bin {i}: {bin} (Total: {sum(bin)})\n")
            
            total_space = len(bins) * bin_capacity
            used_space = sum(sum(bin) for bin in bins)
            efficiency = (used_space / total_space) * 100 if total_space > 0 else 0
            self.result_text.insert(tk.END, f"\nEfficiency: {efficiency:.2f}%")
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))