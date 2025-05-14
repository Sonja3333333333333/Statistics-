import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logic import Processor
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.express as px
import numpy as np

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.processor = Processor()

        self.title("Лабораторна робота №3")
        self.geometry("1300x800")  # Розмір вікна

        # Панель з кнопками
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side="top", fill="x", pady=10)

        # Кнопки на панелі
        self.btn1 = ttk.Button(self.button_frame, text="Таблиця умовних середніх", command=self.show_conditional_means_table)
        self.btn1.pack(side="left", padx=5)

        self.btn2 = ttk.Button(self.button_frame, text="Кореляційне поле та емпірична лінія регресії", command=self.show_emperical_regresion_line)
        self.btn2.pack(side="left", padx=5)

        self.btn3 = ttk.Button(self.button_frame, text="Лінійна регресія", command=self.show_liner_regresion_line)
        self.btn3.pack(side="left", padx=5)

        self.btn4 = ttk.Button(self.button_frame, text="Перевірити адекватність лінійної моделі", command=self.check_liner_model_adequacy)
        self.btn4.pack(side="left", padx=5)

        self.btn5 = ttk.Button(self.button_frame, text="Обчислити вибірковий лінійний коефіцієнт кореляції та перевірити його значущість", command=self.liner_correlation_analysis)
        self.btn5.pack(side="left", padx=5)

        self.button_frame2 = ttk.Frame(self)
        self.button_frame2.pack(side="top", fill="x", pady=5)

        self.btn6 = ttk.Button(self.button_frame2, text="Припустити параболічну кореляцію та перевірити адекватність моделі", command=self.parabolic_correlation_test)
        self.btn6.pack(side="left", padx=5)

        self.btn7 = ttk.Button(self.button_frame2, text="Припустити гіперболічну кореляцію та перевірити адекватність моделі", command=self.giperbolic_correlation_test)
        self.btn7.pack(side="left", padx=5)

        self.btn8 = ttk.Button(self.button_frame2, text="Припустити показникову кореляцію та перевірити адекватність моделі", command=self.exponential_correlation_test)
        self.btn8.pack(side="left", padx=5)

        self.button_frame3 = ttk.Frame(self)
        self.button_frame3.pack(side="top", fill="x", pady=5)

        self.btn9 = ttk.Button(self.button_frame3, text="Припустити кореневу кореляцію та перевірити адекватність моделі", command=self.root_correlation_test)
        self.btn9.pack(side="left", padx=5)

        self.btn10 = ttk.Button(self.button_frame3, text="За моделлю з найменшою залишковою варіацією 𝑄𝑜 обчислити прогнозоване значення y* при заданому значенні x*", command=self.show_forecasted_value)
        self.btn10.pack(side="left", padx=5)


          # Місце для результатів
        self.result_frame = ttk.Frame(self)
        self.result_frame.pack(side="top", fill="both", expand=True)

        self.result_text = tk.Text(self.result_frame, height=16, width=80, wrap=tk.WORD)
        self.result_text.pack(fill="both", padx=10, pady=10)
        # self.result_text.insert(tk.END, "Тут буде результат.\n")  # Підказка для користувача

        self.result_text.tag_configure("header", font=("Helvetica", 12, "bold"))
        self.result_text.tag_configure("subheader", font=("Helvetica", 10, "bold"))


        # Місце для графіку (буде доповнено пізніше)
        self.graph_frame = ttk.Frame(self)
        self.graph_frame.pack(side="top", fill="both", expand=True)

        # self.graph_placeholder = ttk.Label(self.graph_frame, text="Графік з'явиться тут", anchor="center")
        # self.graph_placeholder.pack(fill="both", padx=10, pady=10)

    def show_conditional_means_table(self):
        data = self.processor.get_conditional_means_table()
        df = pd.DataFrame(list(data.items()), columns=["xi", "умовне середнє"])

        self.result_text.delete(1.0, tk.END)  
        self.result_text.insert(tk.END, "Таблиця умовних середніх:\n", 'header')
        self.result_text.insert(tk.END, df.to_string(index=False))

    def show_emperical_regresion_line(self):
        conditional_means_dict = self.processor.get_conditional_means_table()

        # Сортуємо значення для побудови графіка
        x_vals = sorted(conditional_means_dict.keys())
        y_vals = [conditional_means_dict[x] for x in x_vals]

        # Створюємо нову фігуру
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_vals, y_vals, marker='o', color='orange', label='Емпірична лінія регресії')
        ax.set_xlabel("X")
        ax.set_ylabel("Умовне середнє Y")
        ax.set_title("Емпірична лінія регресії")
        ax.grid(True)
        ax.legend()

        ax.set_facecolor("#f8f8f8")
        fig.tight_layout()

        # Видаляємо попередній графік (якщо є)
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Додаємо новий графік до Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()

        # Пакуємо canvas з фіксованими розмірами, обмежуючи його висоту та ширину
        canvas.get_tk_widget().pack(fill=None, padx=10, pady=10)  # Додаємо падінг для акуратності

    def show_liner_regresion_line(self):
        a,b = self.processor.find_coefficients_liner_regresion()

        x_values = list(self.processor.corerlation_table.columns)
        y_values = [a*x + b for x in x_values]

        self.result_text.delete(1.0, tk.END)  
        self.result_text.insert(tk.END, f"a = {round(a, 6)}\nb = {round(b, 6)}")

        # Створюємо нову фігуру
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_values, y_values, marker='o', color='orange', label='Графік лінійної регресії')
        ax.set_xlabel("X")
        ax.set_ylabel("y = ax + b")
        ax.set_title("Графік лінійної регресії")
        ax.grid(True)
        ax.legend()

        ax.set_facecolor("#f8f8f8")
        fig.tight_layout()

        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Додаємо новий графік до Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()

        # Пакуємо canvas з фіксованими розмірами, обмежуючи його висоту та ширину
        canvas.get_tk_widget().pack(fill=None, padx=10, pady=10)  # Додаємо падінг для акуратності

    def show_forecasted_value(self):
        a, b = self.processor.find_coefficients_exponential_regresion()
        x_values = list(self.processor.corerlation_table.columns)
        x_range = np.linspace(min(x_values) - 1, max(x_values) + 1, 100)
        y_values = [b*a**x for x in x_range]

        self.result_text.delete(1.0, tk.END)  
        self.result_text.insert(tk.END, "Обчислення прогнозованого значення y* при заданому значенні x*", "header")
        self.result_text.insert(tk.END, "\nМоделлю з найменшим значеням залишкової варіації Qo є показникова модель.\n")

        self.result_text.insert(tk.END, "\nВибіркові значення x*: ", "subheader")
        self.result_text.insert(tk.END, ",".join(map(str, x_values)))

        def on_submit():
            try:
                x = float(entry.get())
                y = self.processor.get_forecasted_value(x)

                self.result_text.insert(tk.END, f"\n\nПрогнозоване значення для x = {x}:\ny = {y:.3f}")

                window.destroy()

            except ValueError:
                messagebox.showerror("Помилка", "Будь ласка, введіть числове значення.")


        window = tk.Toplevel()
        window.title("Прогноз значення")
        
        window.geometry("300x150")

        label = tk.Label(window, text="Введіть значення x:")
        label.pack(pady=5)

        entry = tk.Entry(window)
        entry.pack(pady=5)

        submit_button = tk.Button(window, text="Обчислити", command=on_submit)
        submit_button.pack(pady=10)

        window.transient()  
        window.grab_set()   

        



    # ------------------------- F-тест для нелінійних кореляцій -----------------------   
    def ask_alpha_and_run(self, callback):
        def on_submit():
            try:
                alpha = float(entry.get())
                if not (0 < alpha < 1):
                    raise ValueError
                popup.destroy()
                callback(alpha)
            except ValueError:
                messagebox.showerror("Помилка", "Введіть коректне значення α (наприклад, 0.05)")

        popup = tk.Toplevel(self)
        popup.title("Введення рівня значущості α")
        popup.geometry("300x100")
        popup.grab_set()

        label = ttk.Label(popup, text="Введіть рівень значущості α (0 < α < 1):")
        label.pack(pady=5)

        entry = ttk.Entry(popup)
        entry.insert(0, "0.05")
        entry.pack(pady=5)

        submit_btn = ttk.Button(popup, text="OK", command=on_submit)
        submit_btn.pack(pady=5)

    
    def parabolic_correlation_test(self):
        def run_test(alpha):
            a,b,c = self.processor.find_coefficients_parabolic_regresion()
            conditional_means = self.processor.get_conditional_means_table()

            x_values = list(self.processor.corerlation_table.columns)
            y_values = [a*x**2 + b*x + c for x in x_values]
            y_empirical = [conditional_means[x] for x in x_values]

            self.result_text.delete(1.0, tk.END)  
            self.result_text.insert(tk.END, "Припускаємо параболічний вигляд функції нелінійної регресії", "header")
            self.result_text.insert(tk.END, "\nТобто, що рівняння кривої регресії має вигляд y = ax^2 + bx + c")
            self.result_text.insert(tk.END, f"\na = {round(a, 6)}\nb = {round(b, 6)}\nc = {round(c, 6)}")
            self.result_text.insert(tk.END, f"\nРівняння кривої регресії: y = {round(a, 2)}x^2 + {round(b, 2)}x + {round(c, 2)}")

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x_values, y_values, marker='o', color='orange', label='Графік параболічної регресії')
            ax.scatter(x_values, y_empirical, color='green', label='Емпіричні умовні середні')
            ax.set_xlabel("X")
            ax.set_ylabel("y = ax^2 + bx + c")
            ax.set_title("Графік параболічної регресії")
            ax.grid(True)
            ax.legend()

            ax.set_facecolor("#f8f8f8")
            fig.tight_layout()

            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()

            canvas.get_tk_widget().pack(fill=None, padx=10, pady=10) 

            self.result_text.insert(tk.END, f"\nПеревірка адекватності побудованої моделі за F-критерієм", "header")
            self.result_text.insert(tk.END, f"\nН₀ (нульова гіпотеза): модель регресії не є значущою")
            self.result_text.insert(tk.END, f"\nН₁ (альтернативна гіпотеза): модель регресії є значущою.\n")

            Q, Qp, Qo, F_emperical, F_critical, is_accepted = self.processor.F_criteria_adequacy_test(type="parabolic", alpha=alpha)
            self.result_text.insert(tk.END, f"\nQ = {round(Q, 6)}\nQp = {round(Qp, 6)}\nQo = {round(Qo, 6)}")
            self.result_text.insert(tk.END, f"\nЕмпіричне значення статистики F: {round(F_emperical, 6)}")
            self.result_text.insert(tk.END, f"\nКритичне значення статистики F: {round(F_critical, 6)}\n")

            if is_accepted:
                self.result_text.insert(tk.END, "\nОскільки F_емпіричне < F_критичне, приймаємо нульову гіпотезу.")
                self.result_text.insert(tk.END, f"\nМодель не є адекватною при рівні значущості {alpha}.")
            else:
                self.result_text.insert(tk.END, "\nОскільки F_емпіричне > F_критичне, відхиляємо нульову гіпотезу.")
                self.result_text.insert(tk.END, f"\nМодель є адекватною при рівні значущості {alpha}.")

        self.ask_alpha_and_run(run_test)

    def giperbolic_correlation_test(self):
        def run_test(alpha):
            a,b = self.processor.find_coefficients_giperbolic_regresion()
            conditional_means = self.processor.get_conditional_means_table()

            x_values = list(self.processor.corerlation_table.columns)
            y_values = [(a/x )+ b for x in x_values]
            y_empirical = [conditional_means[x] for x in x_values]

            self.result_text.delete(1.0, tk.END)  
            self.result_text.insert(tk.END, "Припускаємо гіперболічний вигляд функції нелінійної регресії", "header")
            self.result_text.insert(tk.END, "\nТобто, що рівняння кривої регресії має вигляд y = a/x + b")
            self.result_text.insert(tk.END, f"\na = {round(a, 6)}\nb = {round(b, 6)}")
            self.result_text.insert(tk.END, f"\nРівняння кривої регресії: y = {round(a, 2)}/x + {round(b, 2)}")

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x_values, y_values, marker='o', color='orange', label='Графік гіперболічної регресії')
            ax.scatter(x_values, y_empirical, color='green', label='Емпіричні умовні середні')
            ax.set_xlabel("X")
            ax.set_ylabel("y = a/x + b")
            ax.set_title("Графік гіперболічної регресії")
            ax.grid(True)
            ax.legend()

            ax.set_facecolor("#f8f8f8")
            fig.tight_layout()

            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()

            canvas.get_tk_widget().pack(fill=None, padx=10, pady=10) 

            self.result_text.insert(tk.END, f"\nПеревірка адекватності побудованої моделі за F-критерієм", "header")
            self.result_text.insert(tk.END, f"\nН₀ (нульова гіпотеза): модель регресії не є значущою")
            self.result_text.insert(tk.END, f"\nН₁ (альтернативна гіпотеза): модель регресії є значущою.\n")

            Q, Qp, Qo, F_emperical, F_critical, is_accepted = self.processor.F_criteria_adequacy_test(type="giperbolic", alpha=alpha)
            self.result_text.insert(tk.END, f"\nQ = {round(Q, 6)}\nQp = {round(Qp, 6)}\nQo = {round(Qo, 6)}")
            self.result_text.insert(tk.END, f"\nЕмпіричне значення статистики F: {round(F_emperical, 6)}")
            self.result_text.insert(tk.END, f"\nКритичне значення статистики F: {round(F_critical, 6)}\n")

            if is_accepted:
                self.result_text.insert(tk.END, "\nОскільки F_емпіричне < F_критичне, приймаємо нульову гіпотезу.")
                self.result_text.insert(tk.END, f"\nМодель не є адекватною при рівні значущості {alpha}.")
            else:
                self.result_text.insert(tk.END, "\nОскільки F_емпіричне > F_критичне, відхиляємо нульову гіпотезу.")
                self.result_text.insert(tk.END, f"\nМодель є адекватною при рівні значущості {alpha}.")

        self.ask_alpha_and_run(run_test)

    def exponential_correlation_test(self):
        def run_test(alpha):
            a,b = self.processor.find_coefficients_exponential_regresion()
            conditional_means = self.processor.get_conditional_means_table()

            x_values = list(self.processor.corerlation_table.columns)
            y_values = [b*a**x for x in x_values]
            y_empirical = [conditional_means[x] for x in x_values]

            self.result_text.delete(1.0, tk.END)  
            self.result_text.insert(tk.END, "Припускаємо показниковий вигляд функції нелінійної регресії", "header")
            self.result_text.insert(tk.END, "\nТобто, що рівняння кривої регресії має вигляд y = ba^x")
            self.result_text.insert(tk.END, f"\na = {round(a, 6)}\nb = {round(b, 6)}")
            self.result_text.insert(tk.END, f"\nРівняння кривої регресії: y =  {round(b, 2)} * {round(a, 2)}^x")

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x_values, y_values, marker='o', color='orange', label='Графік показникової регресії')
            ax.scatter(x_values, y_empirical, color='green', label='Емпіричні умовні середні')
            ax.set_xlabel("X")
            ax.set_ylabel("y = ba^x")
            ax.set_title("Графік показникової регресії")
            ax.grid(True)
            ax.legend()

            ax.set_facecolor("#f8f8f8")
            fig.tight_layout()

            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()

            canvas.get_tk_widget().pack(fill=None, padx=10, pady=10) 

            self.result_text.insert(tk.END, f"\nПеревірка адекватності побудованої моделі за F-критерієм", "header")
            self.result_text.insert(tk.END, f"\nН₀ (нульова гіпотеза): модель регресії не є значущою")
            self.result_text.insert(tk.END, f"\nН₁ (альтернативна гіпотеза): модель регресії є значущою.\n")

            Q, Qp, Qo, F_emperical, F_critical, is_accepted = self.processor.F_criteria_adequacy_test(type="exponential", alpha=alpha)
            self.result_text.insert(tk.END, f"\nQ = {round(Q, 6)}\nQp = {round(Qp, 6)}\nQo = {round(Qo, 6)}")
            self.result_text.insert(tk.END, f"\nЕмпіричне значення статистики F: {round(F_emperical, 6)}")
            self.result_text.insert(tk.END, f"\nКритичне значення статистики F: {round(F_critical, 6)}\n")

            if is_accepted:
                self.result_text.insert(tk.END, "\nОскільки F_емпіричне < F_критичне, приймаємо нульову гіпотезу.")
                self.result_text.insert(tk.END, f"\nМодель не є адекватною при рівні значущості {alpha}.")
            else:
                self.result_text.insert(tk.END, "\nОскільки F_емпіричне > F_критичне, відхиляємо нульову гіпотезу.")
                self.result_text.insert(tk.END, f"\nМодель є адекватною при рівні значущості {alpha}.")

        self.ask_alpha_and_run(run_test)

    def root_correlation_test(self):
        def run_test(alpha):
            a,b = self.processor.find_coefficients_root_regresion()
            conditional_means = self.processor.get_conditional_means_table()

            x_values = list(self.processor.corerlation_table.columns)
            y_values = [a*np.sqrt(x) + b for x in x_values]
            y_empirical = [conditional_means[x] for x in x_values]

            self.result_text.delete(1.0, tk.END)  
            self.result_text.insert(tk.END, "Припускаємо кореневий вигляд функції нелінійної регресії", "header")
            self.result_text.insert(tk.END, "\nТобто, що рівняння кривої регресії має вигляд 𝑦 = 𝑎√𝑥 + 𝑏 ")
            self.result_text.insert(tk.END, f"\na = {round(a, 6)}\nb = {round(b, 6)}")
            self.result_text.insert(tk.END, f"\nРівняння кривої регресії: y =  {round(b, 2)} * {round(a, 2)}^x")

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x_values, y_values, marker='o', color='orange', label='Графік кореневої регресії')
            ax.scatter(x_values, y_empirical, color='green', label='Емпіричні умовні середні')
            ax.set_xlabel("X")
            ax.set_ylabel("y = a√x + b")
            ax.set_title("Графік кореневої регресії")
            ax.grid(True)
            ax.legend()

            ax.set_facecolor("#f8f8f8")
            fig.tight_layout()

            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()

            canvas.get_tk_widget().pack(fill=None, padx=10, pady=10) 

            self.result_text.insert(tk.END, f"\nПеревірка адекватності побудованої моделі за F-критерієм", "header")
            self.result_text.insert(tk.END, f"\nН₀ (нульова гіпотеза): модель регресії не є значущою")
            self.result_text.insert(tk.END, f"\nН₁ (альтернативна гіпотеза): модель регресії є значущою.\n")

            Q, Qp, Qo, F_emperical, F_critical, is_accepted = self.processor.F_criteria_adequacy_test(type="root", alpha=alpha)
            self.result_text.insert(tk.END, f"\nQ = {round(Q, 6)}\nQp = {round(Qp, 6)}\nQo = {round(Qo, 6)}")
            self.result_text.insert(tk.END, f"\nЕмпіричне значення статистики F: {round(F_emperical, 6)}")
            self.result_text.insert(tk.END, f"\nКритичне значення статистики F: {round(F_critical, 6)}\n")

            if is_accepted:
                self.result_text.insert(tk.END, "\nОскільки F_емпіричне < F_критичне, приймаємо нульову гіпотезу.")
                self.result_text.insert(tk.END, f"\nМодель не є адекватною при рівні значущості {alpha}.")
            else:
                self.result_text.insert(tk.END, "\nОскільки F_емпіричне > F_критичне, відхиляємо нульову гіпотезу.")
                self.result_text.insert(tk.END, f"\nМодель є адекватною при рівні значущості {alpha}.")

        self.ask_alpha_and_run(run_test)


    # ------------------------------------------------------------------------------------------------------

    def check_liner_model_adequacy(self):
        Q, Qp, Qo = self.processor.get_variations()
        R2 = self.processor.calculate_determination_coefficient()
        self.result_text.delete(1.0, tk.END)  
        
        self.result_text.insert(tk.END, "Варіаційне рівняння для перевірки правильності побудови моделі:")
        self.result_text.insert(tk.END, "\nQ = Qp + Qo")
        self.result_text.insert(tk.END, f"\nПідставляємо наші значення варіацій:\nQ = {round(Q, 6)}\nQp = {round(Qp, 6)}\nQo = {round(Qo, 6)}")
        self.result_text.insert(tk.END, f"\nПереконуємося, що наша модель побудована правильно: {round(Q, 6)} ≈ {round(Qp + Qo, 6)}")
        self.result_text.insert(tk.END, f"\nРозрахуємо коефіцієнт детермінації: R² ≈ {round(R2, 6)}")
        self.result_text.insert(
            tk.END,
            "\nОскільки значення коефіцієнта детермінації наближене до 1, "
            "робимо висновок, що лінійне рівняння регресії добре пояснює поведінку результативної ознаки."
        )
        
            # === Побудова графіка ===
        conditional_means = self.processor.get_conditional_means_table()
        a, b = self.processor.find_coefficients_liner_regresion()

        x_vals = sorted(conditional_means.keys())
        y_empirical = [conditional_means[x] for x in x_vals]
        y_theoretical = [a * x + b for x in x_vals]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(x_vals, y_empirical, color='green', label='Емпіричні умовні середні')
        ax.plot(x_vals, y_theoretical, color='orange', label='Теоретична лінія регресії')
        ax.set_title("Перевірка адекватності моделі")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        ax.grid(True)

        ax.set_facecolor("#f8f8f8")
        fig.tight_layout()
        
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Додаємо новий графік до Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()

        # Пакуємо canvas з фіксованими розмірами, обмежуючи його висоту та ширину
        canvas.get_tk_widget().pack(fill=None, padx=10, pady=10)  # Додаємо падінг для акуратності

    def open_alpha_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Вибір рівня значущості")
        dialog.geometry("300x150")
        dialog.grab_set()  # робить вікно модальним

        tk.Label(dialog, text="Введіть рівень значущості (наприклад, 0.05):").pack(pady=10)

        alpha_var = tk.StringVar(value="0.05")
        entry = tk.Entry(dialog, textvariable=alpha_var)
        entry.pack()

        def submit_alpha():
            try:
                alpha = float(alpha_var.get())
                if not 0 < alpha < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Помилка", "Введіть число між 0 та 1.")
                return

            dialog.destroy()
            self.run_significance_test(alpha)

        tk.Button(dialog, text="OK", command=submit_alpha).pack(pady=10)

    def run_significance_test(self, alpha):
        t_empirical, t_critical, if_accepted = self.processor.check_correlation_coefficient_statistical_significance(alpha)

        self.result_text.insert(tk.END, f"\nОбраний рівень значущості: {alpha}")
        self.result_text.insert(tk.END, f"\nЕмпіричне значення статистики t: {round(t_empirical, 6)}")
        self.result_text.insert(tk.END, f"\nКритичне значення статистики t: {round(t_critical, 6)}\n")

        if if_accepted:
            self.result_text.insert(tk.END, "\nОскільки |t_емп| ≤ t_крит, немає підстав відхиляти нульову гіпотезу.")
            self.result_text.insert(tk.END, "\nКоефіцієнт кореляції не є статистично значущим на обраному рівні значущості.")
        else:
            self.result_text.insert(tk.END, "\nОскільки |t_емп| > t_крит, нульова гіпотеза відхиляється.")
            self.result_text.insert(tk.END, "\nКоефіцієнт кореляції є статистично значущим, тобто зв’язок між змінними існує на рівні генеральної сукупності.")


    def liner_correlation_analysis(self):
        r = self.processor.calculate_sample_linear_correlation_coefficient()

        self.result_text.delete(1.0, tk.END)  
        self.result_text.insert(tk.END, "Рахуємо вибірковий лінійний коефіцієнт кореляції", "header")
        self.result_text.insert(tk.END, f"\nr = {round(r, 6)}")
        self.result_text.insert(tk.END, "\nАбсолютне значення коефіцієнта вказує на силу зв'язку, а знак на його напрям.")
        self.result_text.insert(tk.END, "\nУ нашому випадку між змінними є дуже сильний зворотний (негативний) лінійний зв'язок: коли одна змінна збільшується, інша, ймовірно, зменшується.\n")

        t_emperical, t_critical, if_accepted = self.processor.check_correlation_coefficient_statistical_significance(alpha=0.05)
        self.result_text.insert(tk.END, "\nПеревіримо статистичну значущість коефіцієнта", 'header')
        self.result_text.insert(tk.END, "\nН₀ (нульова гіпотеза): ρ=0 (у генеральній сукупності немає лінійної залежності).")
        self.result_text.insert(tk.END, "\nН₁ (альтернативна гіпотеза): ρ≠0 (лінійна залежність є)\n")
        # Відкриваємо вікно для вибору alpha
        self.open_alpha_dialog()

    


        


    def run(self):
        self.mainloop()
