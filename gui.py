import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from processor import Processor

class GUI:
    
    def __init__(self, root):
        self.processor = None
        self.root = root
        self.root.title("Індивідуальне завдання №1")
        self.root.geometry("1000x1000")

        # === ГОЛОВНИЙ КОНТЕЙНЕР З ПРОКРУТКОЮ ===
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Налаштування області прокрутки
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Додаємо обробник зміни розміру Canvas
        def on_canvas_configure(event):
            self.canvas.itemconfig(window, width=event.width)  # Розтягуємо scrollable_frame

        self.canvas.bind("<Configure>", on_canvas_configure)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # === ВІДЖЕТИ ===
        self.label = tk.Label(self.scrollable_frame, text="Введіть об'єм вибірки (щонайменше 50):")
        self.label.pack(pady=5)

        self.entry = tk.Entry(self.scrollable_frame)
        self.entry.pack(pady=5)

        self.ok_button = tk.Button(self.scrollable_frame, text="Показати згенеровану вибірку", command=self.__get_number)
        self.ok_button.pack(pady=5, anchor="center")   

        self.sample_label = tk.Label(self.scrollable_frame, text="")
        self.sample_label.pack()  

        self.variation_button = tk.Button(self.scrollable_frame, text="Показати варіаційний ряд", command=self.__show_variation_range, state="disabled")
        self.variation_button.pack(pady=5)

        self.variation_label = tk.Label(self.scrollable_frame, text="")
        self.variation_label.pack()

        self.freq_table_button = tk.Button(self.scrollable_frame, text="Показати частотну таблицю", command=self.__show_freq_table, state="disabled")
        self.freq_table_button.pack(pady=5)

        self.freq_table_frame = tk.Frame(self.scrollable_frame)
        self.freq_table_frame.pack()

        self.freq_diagram_button = tk.Button(self.scrollable_frame, text="Показати діаграму частот", command=self.__show_freq_diagram, state="disabled")
        self.freq_diagram_button.pack(pady=5)

        self.freq_polygon_button = tk.Button(self.scrollable_frame, text="Показати полігон частот", command=self.__show_freq_polygon, state="disabled")
        self.freq_polygon_button.pack(pady=5)

        self.empirical_func_button = tk.Button(self.scrollable_frame, text="Показати графік емпіричної функції", command=self.__show_empirical_func, state="disabled")
        self.empirical_func_button.pack(pady=5)

        self.freq_table_with_relative_freq_frame = tk.Frame(self.scrollable_frame)
        self.freq_table_with_relative_freq_frame.pack()

    def __get_number(self):
        value = self.entry.get()
        try:
            num = int(value)
            if num < 50:
                raise ValueError("Значення має бути більше ніж 50")
           
            self.processor = Processor(num)
            sample = self.processor.sample.tolist()
            sample_str = ", ".join(map(str, sample))
            
            self.sample_label.config(
                text=f"{sample_str}",
                wraplength=400  
            )
            
            self.entry.delete(0, tk.END)
            self.variation_button.config(state="normal")  # Активуємо кнопку варіаційного ряду
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.entry.delete(0, tk.END)

    def __show_variation_range(self):
        if self.processor is not None:
            variation = self.processor.variation_range.tolist()
            variation_str = ", ".join(map(str, variation))
            self.variation_label.config(
                text=f"{variation_str}",
                wraplength=400
            )

            self.freq_table_button.config(state="normal")

    def __show_freq_table(self):
        '''style = ttk.Style()
        style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid")  
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), relief="solid")  '''

        table = self.processor.freq_table

        tree = ttk.Treeview(self.freq_table_frame, columns=list(table.columns), show="headings", height=5)

        for col in table.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for i, row in table.iterrows():
            tree.insert("", "end", values=list(row))

        scrollbar = ttk.Scrollbar(self.freq_table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.freq_diagram_button.configure(state="active")
        self.freq_polygon_button.configure(state="active")
        self.empirical_func_button.configure(state="active")

    def __show_freq_diagram(self):
        self.processor.show_freq_diagram()

    def __show_freq_polygon(self):
        self.processor.show_freq_polygon()

    def __show_empirical_func(self):
        table = self.processor.freq_table_with_relative_freq

        tree = ttk.Treeview(self.freq_table_with_relative_freq_frame, columns=list(table.columns), show="headings", height=5)

        for col in table.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        for i, row in table.iterrows():
            tree.insert("", "end", values=list(row))

        scrollbar = ttk.Scrollbar(self.freq_table_with_relative_freq_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns")


def run():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()    
