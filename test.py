import matplotlib.pyplot as plt
import numpy as np

# Створення даних для функції
x1 = np.linspace(0, 5, 100)
y1 = np.floor(x1)  # Сходи на першій частині
x2 = np.linspace(6, 10, 100)
y2 = np.floor(x2)  # Сходи на другій частині

# Створення графіка
plt.plot(x1, y1, label="Частина 1", color="blue")
plt.plot(x2, y2, label="Частина 2", color="blue")

# Додавання стрілок
plt.annotate('', xy=(6, np.floor(6)), xytext=(5, np.floor(5)),
             arrowprops=dict(facecolor='red', shrink=0.05))

# Налаштування графіка
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Сходи з розривами і стрілочками')
plt.legend()
plt.grid(True)

# Показати графік
plt.show()
