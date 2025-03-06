import tkinter as tk
import gui 
import gui2 

class GUI3:
    def __init__(self, root):
        self.root = root
        self.root.title("Індивідуальне завдання №1")
        self.root.geometry("400x400")

        # Текстове поле для інструкцій
        label = tk.Label(self.root, text="Оберіть тип розподілу:")
        label.pack(pady=20)

        # Кнопка для дискретного розподілу
        self.button1 = tk.Button(self.root, text="Дискретний розподіл", command=self.select_discrete)
        self.button1.pack(pady=10)

        # Кнопка для неперервного розподілу
        self.button2 = tk.Button(self.root, text="Неперервний розподіл", command=self.select_continuous)
        self.button2.pack(pady=10)

    def select_discrete(self):
        # Якщо вибрано дискретний розподіл, закриваємо поточне вікно та відкриваємо нове для дискретного розподілу
        self.root.destroy()  # Закриваємо головне вікно
        gui.run() # Запуск відповідного вікна для дискретного розподілу

    def select_continuous(self):
        # Якщо вибрано неперервний розподіл, закриваємо поточне вікно та відкриваємо нове для неперервного розподілу
        self.root.destroy()  # Закриваємо головне вікно
        gui2.run() # Запуск відповідного вікна для неперервного розподілу

# Головна функція для запуску GUI3
if __name__ == "__main__":
    root = tk.Tk()
    app = GUI3(root)
    root.mainloop()
