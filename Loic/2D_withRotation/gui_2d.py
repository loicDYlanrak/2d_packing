import math
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from algorithms_2d import nfdh, ffdh, best_fit, brute_force_2d
from visualization import draw_packing
import random
from shapes import Circle, Rectangle, IsoscelesTriangle

class Packing2DApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("2D Rectangle Packing Problem Solver")
        self.geometry("1100x800")
        self.configure(bg="#f0f0f0")
        
        self.rectangles = []
        self.container_size = (0, 0)
        
        self.create_widgets()
        self.style_ui()
    
    def style_ui(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configuration des styles
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10), padding=5)
        self.style.configure("TEntry", padding=5)
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        
        # Couleurs
        self.primary_color = "#4a6fa5"
        self.secondary_color = "#166088"
        self.accent_color = "#4fc3f7"
        
        self.style.configure("Primary.TButton", background=self.primary_color, foreground="white")
        self.style.configure("Secondary.TButton", background=self.secondary_color, foreground="white")
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="2D Rectangle Packing Problem", style="Header.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de configuration du conteneur
        container_frame = ttk.LabelFrame(main_frame, text="Container Configuration", padding=10)
        container_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
        
        
        
        ttk.Label(container_frame, text="Width:").grid(row=0, column=0, sticky="w")
        self.container_width_entry = ttk.Entry(container_frame)
        self.container_width_entry.grid(row=0, column=1, pady=5)
        self.container_width_entry.insert(0, "30")
        
        ttk.Label(container_frame, text="Height:").grid(row=1, column=0, sticky="w")
        self.container_height_entry = ttk.Entry(container_frame)
        self.container_height_entry.grid(row=1, column=1, pady=5)
        self.container_height_entry.insert(0, "20")
        
        # Frame d'ajout de rectangles
        rect_frame = ttk.LabelFrame(main_frame, text="Add Rectangles", padding=10)
        rect_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 10))
        
        # Dans la frame rect_frame
        ttk.Label(rect_frame, text="Type:").grid(row=2, column=0, sticky="w")
        self.shape_type = ttk.Combobox(rect_frame, values=["Rectangle", "Circle", "Triangle"])
        self.shape_type.grid(row=2, column=1, pady=5)
        self.shape_type.current(0)

        ttk.Label(rect_frame, text="Dimension 1:").grid(row=0, column=0, sticky="w")
        self.dim1_entry = ttk.Entry(rect_frame)
        self.dim1_entry.grid(row=0, column=1, pady=5)

        ttk.Label(rect_frame, text="Dimension 2:").grid(row=1, column=0, sticky="w")
        self.dim2_entry = ttk.Entry(rect_frame)
        self.dim2_entry.grid(row=1, column=1, pady=5)
        
        ttk.Button(rect_frame, text="Add Rectangle", command=self.add_shape, style="Primary.TButton").grid(row=2, column=0, columnspan=2, pady=5, sticky="we")
        
        # Frame des rectangles ajoutés
        list_frame = ttk.LabelFrame(main_frame, text="Rectangles List", padding=10)
        list_frame.grid(row=3, column=0, sticky="nsew", padx=(0, 10))

        self.rect_listbox = tk.Listbox(list_frame, height=8, font=("Courier", 10))
        self.rect_listbox.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="Remove Selected", command=self.remove_rectangle).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(button_frame, text="Clear All", command=self.clear_rectangles).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        # Frame des algorithmes
        algo_frame = ttk.LabelFrame(main_frame, text="Algorithms", padding=10)
        algo_frame.grid(row=1, column=1, rowspan=3, sticky="nsew")
        
        ttk.Button(algo_frame, text="NFDH", command=lambda: self.run_algorithm("NFDH"), style="Primary.TButton").grid(row=0, column=0, pady=5, sticky="we")
        ttk.Button(algo_frame, text="FFDH", command=lambda: self.run_algorithm("FFDH"), style="Primary.TButton").grid(row=1, column=0, pady=5, sticky="we")
        ttk.Button(algo_frame, text="Best-Fit", command=lambda: self.run_algorithm("Best-Fit"), style="Primary.TButton").grid(row=2, column=0, pady=5, sticky="we")
        ttk.Button(algo_frame, text="Brute-Force", command=lambda: self.run_algorithm("Brute-Force"), style="Secondary.TButton").grid(row=3, column=0, pady=5, sticky="we")
        
        ttk.Button(algo_frame, text="Generate Random", command=self.generate_random).grid(row=4, column=0, pady=10, sticky="we")
        
        # Zone de résultats et visualisation
        result_frame = ttk.LabelFrame(main_frame, text="Results & Visualization", padding=10)
        result_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=60, height=10, font=("Consolas", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        self.canvas_frame = ttk.Frame(result_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Configuration du redimensionnement
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def add_shape(self):
        try:
            shape_type = self.shape_type.get()
            
            if shape_type == "Rectangle":
                w = int(self.dim1_entry.get())
                h = int(self.dim2_entry.get())
                if w <= 0 or h <= 0:
                    raise ValueError("Dimensions must be positive")
                shape = Rectangle(w, h)
                
            elif shape_type == "Circle":
                r = int(self.dim1_entry.get())
                if r <= 0:
                    raise ValueError("Radius must be positive")
                shape = Circle(r)
                self.dim2_entry.delete(0, tk.END)
                self.dim2_entry.insert(0, str(r))
                
            elif shape_type == "Triangle":
                base = int(self.dim1_entry.get())
                height = self.dim2_entry.get()
                if base <= 0:
                    raise ValueError("Base must be positive")
                if height:
                    shape = IsoscelesTriangle(base, int(height))
                else:
                    shape = IsoscelesTriangle(base)
            
            self.rectangles.append(shape)
            self.update_rect_list()
            
            self.dim1_entry.delete(0, tk.END)
            self.dim2_entry.delete(0, tk.END)
        
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
    
    def remove_rectangle(self):
        selection = self.rect_listbox.curselection()
        if selection:
            index = selection[0]
            self.rectangles.pop(index)
            self.update_rect_list()
    
    def clear_rectangles(self):
        self.rectangles = []
        self.update_rect_list()
    
    def update_rect_list(self):
        self.rect_listbox.delete(0, tk.END)
        for i, shape in enumerate(self.rectangles, 1):
            if isinstance(shape, Rectangle):
                w, h = shape.width, shape.height
                self.rect_listbox.insert(tk.END, f"Rectangle {i}: {w}x{h}")
            elif isinstance(shape, Circle):
                r = shape.radius
                self.rect_listbox.insert(tk.END, f"Circle {i}: r={r}")
            elif isinstance(shape, IsoscelesTriangle):
                b, h = shape.base, shape.height
                self.rect_listbox.insert(tk.END, f"Triangle {i}: base={b}, height={h:.1f}")
    def generate_random(self):
        container_w = random.randint(20, 40)
        container_h = random.randint(15, 30)
        
        self.container_width_entry.delete(0, tk.END)
        self.container_width_entry.insert(0, str(container_w))
        
        self.container_height_entry.delete(0, tk.END)
        self.container_height_entry.insert(0, str(container_h))
        
        self.rectangles = []
        num_shapes = random.randint(5, 15)
        
        for _ in range(num_shapes):
            shape_type = random.choice(["Rectangle", "Circle", "Triangle"])
            
            if shape_type == "Rectangle":
                w = random.randint(2, container_w // 2)
                h = random.randint(2, container_h // 2)
                self.rectangles.append(Rectangle(w, h))
                
            elif shape_type == "Circle":
                r = random.randint(1, min(container_w, container_h) // 3)
                self.rectangles.append(Circle(r))
                
            elif shape_type == "Triangle":
                base = random.randint(2, container_w // 2)
                height = random.randint(2, container_h // 2)
                self.rectangles.append(IsoscelesTriangle(base, height))
        
        self.update_rect_list()
    
    def run_algorithm(self, algorithm_name):
        try:
            container_w = int(self.container_width_entry.get())
            container_h = int(self.container_height_entry.get())
            
            if not self.rectangles:
                raise ValueError("Please add at least one rectangle")
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Running {algorithm_name} algorithm...\n")
            self.result_text.insert(tk.END, f"Container size: {container_w}x{container_h}\n")
            self.result_text.insert(tk.END, f"Rectangles to pack: {len(self.rectangles)}\n\n")
            
            if algorithm_name == "NFDH":
                shelves = nfdh(self.rectangles, container_w, container_h)
            elif algorithm_name == "FFDH":
                shelves = ffdh(self.rectangles, container_w, container_h)
            elif algorithm_name == "Best-Fit":
                shelves = best_fit(self.rectangles, container_w, container_h)
            elif algorithm_name == "Brute-Force":
                shelves = brute_force_2d(self.rectangles, container_w, container_h)
            
            # Calcul des statistiques
            total_area = container_w * container_h
            packed_rects = [rect for shelf in shelves for rect in shelf]
            used_area = 0
            for shelf in shelves:
                for (w, h, shape) in shelf:
                    if isinstance(shape, Circle):
                        used_area += math.pi * shape.radius ** 2
                    else:  # Rectangle or Triangle
                        used_area += w * h
            efficiency = (used_area / total_area) * 100
            
            self.result_text.insert(tk.END, f"\nResults:\n")
            self.result_text.insert(tk.END, f"- Packed rectangles: {len(packed_rects)}/{len(self.rectangles)}\n")
            self.result_text.insert(tk.END, f"- Space utilization: {efficiency:.2f}%\n")
            
            # Visualisation
            self.canvas.delete("all")
            draw_packing(self.canvas, shelves, container_w, container_h)
        
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))