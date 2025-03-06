import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from processor import Processor

class GUI:
    
    #Зробити кнопки одного розміру і відступи однакові
    #Зробити так, щоб після введення нових даних всі кнопки ставали неактивними також
    def __init__(self, root):
        self.processor = None
        self.root = root
        self.root.title("Неперервний розподіл")
        self.root.geometry("1000x1000")

        # === ГОЛОВНИЙ КОНТЕЙНЕР З ПРОКРУТКОЮ ===
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def update_scroll_region():
            self.canvas.update_idletasks()  
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: update_scroll_region()
        )

        # Додаємо обробник зміни розміру Canvas
        def on_canvas_configure(event):
            self.canvas.itemconfig(window, width=event.width)  # Розтягуємо scrollable_frame

        self.canvas.bind("<Configure>", on_canvas_configure)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # === ВІДЖЕТИ ===
        self.label = tk.Label(self.scrollable_frame, text="Введіть об'єм вибірки (щонайменше 50):")
        self.label.pack(pady=(50, 0))

        self.entry = tk.Entry(self.scrollable_frame)
        self.entry.pack()

        self.ok_button = tk.Button(self.scrollable_frame, text="Показати згенеровану вибірку", command=self.__get_number)
        self.ok_button.pack(pady=(5,0), anchor="center")   

        self.sample_label = tk.Label(self.scrollable_frame, text="")
        self.sample_label.pack()  

        self.variation_button = tk.Button(self.scrollable_frame, text="Показати варіаційний ряд", command=self.__show_variation_range, state="disabled")
        self.variation_button.pack(pady=5)

        self.variation_label = tk.Label(self.scrollable_frame, text="")
        self.variation_label.pack()

        self.freq_table_button = tk.Button(self.scrollable_frame, text="Показати частотну таблицю", command=self.__show_freq_table, state="disabled")
        self.freq_table_button.pack(pady=(0, 5))

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

        self.ct_numeric_characteristics_button = tk.Button(self.scrollable_frame, text="Показати числові характеристики", command=self.__show_ct_numeric_characteristics, state="disabled")
        self.ct_numeric_characteristics_button.pack(pady=5)

        self.ct_numeric_characteristics_frame = tk.Frame(self.scrollable_frame)
        self.ct_numeric_characteristics_frame.pack()

        self.interval_destribution_button = tk.Button(self.scrollable_frame, text="Показати інтервальний розподіл", command=self.__show_interval_destribution, state="disabled")
        self.interval_destribution_button.pack(pady=5)

        self.interval_destribution_frame = tk.Frame(self.scrollable_frame)
        self.interval_destribution_frame.pack()

        self.interval_destribution_histogram_button = tk.Button(self.scrollable_frame, text="Показати гістограму інетервального розподілу варіанси", command=self.__show_interval_destribution_histogram, state="disabled")
        self.interval_destribution_histogram_button.pack(pady=5)

        self.interval_destribution_empirical_button = tk.Button(self.scrollable_frame, text="Показати емпіричну функцію інтервалного розподілу", command=self.__show_interval_destribution_empirical_func, state="disabled")
        self.interval_destribution_empirical_button.pack()

        self.numeric_characteristics_interval_destribution_button = tk.Button(self.scrollable_frame, text="Показати числові характеристики для інтервального розподілу", command=self.__show_characteristics_interval_destribution, state="disabled")
        self.numeric_characteristics_interval_destribution_button.pack(pady=5)

        self.numeric_characteristics_interval_destribution_frame = tk.Frame(self.scrollable_frame)
        self.numeric_characteristics_interval_destribution_frame.pack(pady=(0, 100))



    #обробка винятку недокінця правильна
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
        self.ct_numeric_characteristics_button.configure(state="active")
        self.interval_destribution_button.configure(state="active")

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

        self.processor.show_empire_function()

    def __show_ct_numeric_characteristics(self):
        table = self.processor.get_ct_characteristics_df()
        interquartile_latitudes_table = self.processor.get_interquartile_latitudes_df()

        combined_table = pd.concat([table, interquartile_latitudes_table], ignore_index=True)

        height = len(combined_table)

        # Стиль для сітки
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)  # Встановлюємо висоту рядків
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))  # Стиль заголовків

        # Увімкнення сітки
        style.layout("Treeview", [
            ("Treeview.treearea", {"sticky": "nswe"})  # Додає сітку
        ])

        tree = ttk.Treeview(self.ct_numeric_characteristics_frame, columns=list(combined_table.columns), show="headings", height=height)

        for col in combined_table.columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")

        for i, row in combined_table.iterrows():
            tree.insert("", "end", values=list(row))

        tree.grid(row=0, column=0)

        tree.configure(style="Treeview")
 

    def __show_interval_destribution(self):
        table = self.processor.get_interval_distribution_df()[0]

        tree = ttk.Treeview(self.interval_destribution_frame, columns=list(table.columns), show="headings", height=5)

        for col in table.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for i, row in table.iterrows():
            tree.insert("", "end", values=list(row))

        scrollbar = ttk.Scrollbar(self.interval_destribution_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns") 

        self.interval_destribution_histogram_button.configure(state="active")   
        self.interval_destribution_empirical_button.configure(state="active")
        self.numeric_characteristics_interval_destribution_button.configure(state="active")

        
    def __show_interval_destribution_histogram(self):
        self.processor.show_interval_destribution_histogram()

    def __show_interval_destribution_empirical_func(self):
        self.processor.show_empirical_function_interval_distribution()

    def __show_characteristics_interval_destribution(self):
        table = self.processor.get_interval_characteristics_df()

        height = len(table)

        # Стиль для сітки
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)  # Встановлюємо висоту рядків
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))  # Стиль заголовків

        # Увімкнення сітки
        style.layout("Treeview", [
            ("Treeview.treearea", {"sticky": "nswe"})  # Додає сітку
        ])

        tree = ttk.Treeview(self.numeric_characteristics_interval_destribution_frame, columns=list(table.columns), show="headings", height=height)

        for col in table.columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")

        for i, row in table.iterrows():
            tree.insert("", "end", values=list(row))

        tree.grid(row=0, column=0)

        tree.configure(style="Treeview")



def run():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()    
