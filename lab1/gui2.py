import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from continuous_processor import ContinuousProcessor

class GUI2:
    def __init__(self, root):
        self.processor = None
        self.root = root
        self.root.title("Дискретний розподіл")
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
        self.label.pack(pady=5)

        self.entry = tk.Entry(self.scrollable_frame)
        self.entry.pack(pady=5)

        self.ok_button = tk.Button(self.scrollable_frame, text="Показати згенеровану вибірку", command=self.__get_number)
        self.ok_button.pack(pady=5, anchor="center")   

        self.sample_label = tk.Label(self.scrollable_frame, text="")
        self.sample_label.pack()  


        self.interval_destribution_button = tk.Button(self.scrollable_frame, text="Показати інтервальний статистичний розподіл", command=self.__show_interval_destribution, state="disabled")
        self.interval_destribution_button.pack(pady=5)

        self.interval_destribution_frame = tk.Frame(self.scrollable_frame)
        self.interval_destribution_frame.pack()

        self.interval_destribution_histogram_button = tk.Button(self.scrollable_frame, text="Показати гістограму розподілу", command=self.__show_interval_destribution_histogram, state="disabled")
        self.interval_destribution_histogram_button.pack()

        self.interval_destribution_empirical_button = tk.Button(self.scrollable_frame, text="Показати емпіричну функцію розподілу", command=self.__show_interval_destribution_empirical_func, state="disabled")
        self.interval_destribution_empirical_button.pack()

        self.numeric_characteristics_interval_destribution_button = tk.Button(self.scrollable_frame, text="Показати числові характеристики згрупованих даних", command=self.__show_characteristics_interval_destribution, state="disabled")
        self.numeric_characteristics_interval_destribution_button.pack(pady=5)

        self.numeric_characteristics_interval_destribution_frame = tk.Frame(self.scrollable_frame)
        self.numeric_characteristics_interval_destribution_frame.pack()


    def __get_number(self):
        value = self.entry.get()
        try:
            num = int(value)
            if num < 50:
                raise ValueError("Значення має бути більше ніж 50")
           
            self.processor = ContinuousProcessor(num)
            sample = self.processor.sample.tolist()
            sample_str = ", ".join(map(str, sample))
            
            self.sample_label.config(
                text=f"{sample_str}",
                wraplength=400  
            )
            
            self.entry.delete(0, tk.END)
            self.interval_destribution_button.configure(state="active")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.entry.delete(0, tk.END) 

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
    app = GUI2(root)
    root.mainloop()   