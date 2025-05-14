import pandas as pd
import numpy as np
from scipy.stats import t
from scipy.stats import f

class Processor:
    def __init__(self):
        self.corerlation_table = self.get_data()
        self.k = 7
        self.l = 6

    def get_data(self):
        data = {
            2:  [0,0,0,0,3,23],   # частоти для x=5, y=100,200,300
            3:  [0,0,0,7,18,0],
            5:  [0,0,0,13,4,0],
            7:  [0,1,24,2,0,0],
            9:  [0,21,3,0,0,0],
            12: [13,2,0,0,0,0],
            13: [4,0,0,0,0,0]
        }

        df = pd.DataFrame(data, index=[3,5,6,7,10,12])  # y на рядках
        df.index.name = 'y'
        df.columns.name = 'x'

        return df
    
    def add_ni_and_mj(self):
        df = self.corerlation_table.copy()
        df['mj'] = df.sum(axis=1)      # сума по рядках
        ni_row = df.sum(axis=0)        # тепер врахує і mj
        df.loc['ni'] = ni_row
        return df

    
    def get_conditional_means_table(self):
        df = self.corerlation_table
        conditional_means = {}

        for x in df.columns:
            numerator = 0
            denominator = 0
            for y in df.index:
                freq = df.at[y, x]
                numerator += y * freq
                denominator += freq

            if denominator != 0:
                conditional_mean = numerator / denominator
            else:
                conditional_mean = None  # або np.nan, або 0 — як тобі зручно

            conditional_means[x] = conditional_mean

        # Приводимо ключі до float, щоб уникнути KeyError
        return {float(x): y for x, y in conditional_means.items()}

    
    def get_ni_list(self):
        df = self.add_ni_and_mj()
        ni_row = df.loc['ni']          # витягуємо рядок ni
        ni_values = ni_row.drop('mj')  # прибираємо mj, якщо він не потрібен
        return ni_values.tolist()      # повертаємо як список

    
    #--------------------------------- Коефіцієнти ----------------------------------

    def find_coefficients_liner_regresion(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по стовпцях
        conditional_means = self.get_conditional_means_table()

        # Формуємо елементи системи
        x_values = df.columns
        n_values = ni.values
        y_conditional = [conditional_means[x] for x in x_values]

        sum_x2n = np.sum([x**2 * n for x, n in zip(x_values, n_values)])
        sum_xn = np.sum([x * n for x, n in zip(x_values, n_values)])
        sum_n = np.sum(n_values)
        sum_xn_y = np.sum([x * n * y for x, n, y in zip(x_values, n_values, y_conditional)])
        sum_n_y = np.sum([n * y for n, y in zip(n_values, y_conditional)])

        # Система
        A = np.array([
            [sum_x2n, sum_xn],
            [sum_xn,  sum_n]
        ])
        B = np.array([
            sum_xn_y,
            sum_n_y
        ])

        coeffs = np.linalg.solve(A, B)
        a, b = coeffs

        return a, b
    
    def find_coefficients_parabolic_regresion(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по стовпцях
        conditional_means = self.get_conditional_means_table()

        # Формуємо елементи системи
        x_values = df.columns
        n_values = ni.values
        y_conditional = [conditional_means[x] for x in x_values]

        n = sum(n_values)
        sum_x4n = np.sum([x**4 * n for x, n in zip(x_values, n_values)])
        sum_x3n = np.sum([x**3 * n for x, n in zip(x_values, n_values)])
        sum_x2n = np.sum([x**2 * n for x, n in zip(x_values, n_values)])
        sum_xn = np.sum([x * n for x, n in zip(x_values, n_values)])

        sum_x2n_y = np.sum([x**2 * n * y for x, n, y in zip(x_values, n_values, y_conditional)])
        sum_xn_y = np.sum([x * n * y for x, n, y in zip(x_values, n_values, y_conditional)])
        sum_n_y = np.sum([n * y for n, y in zip(n_values, y_conditional)])

        A = np.array([
            [sum_x4n, sum_x3n, sum_x2n],
            [sum_x3n,  sum_x2n, sum_xn],
            [sum_x2n, sum_xn, n]
        ])
        B = np.array([
            sum_x2n_y,
            sum_xn_y,
            sum_n_y
        ])

        coeffs = np.linalg.solve(A, B)
        a, b, c = coeffs

        return a, b, c
    
    def find_coefficients_giperbolic_regresion(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по стовпцях
        conditional_means = self.get_conditional_means_table()

        # Формуємо елементи системи
        x_values = df.columns
        n_values = ni.values
        y_conditional = [conditional_means[x] for x in x_values]

        n = sum(n_values)
        sum_xn = np.sum([(1/x) * n for x, n in zip(x_values, n_values)])
        sum_x2n = np.sum([(1/x**2) * n for x, n in zip(x_values, n_values)])

        sum_xn_y = np.sum([(1/x )* n * y for x, n, y in zip(x_values, n_values, y_conditional)])
        sum_n_y = np.sum([n * y for n, y in zip(n_values, y_conditional)])

        A = np.array([
            [sum_xn, n],
            [sum_x2n, sum_xn],
        ])

        B = np.array([
            sum_n_y,
            sum_xn_y
        ])

        coeffs = np.linalg.solve(A, B)
        a, b = coeffs

        return a, b
    
    def find_coefficients_exponential_regresion(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по стовпцях
        conditional_means = self.get_conditional_means_table()

        x_values = df.columns
        n_values = ni.values
        y_values = [conditional_means[x] for x in x_values]

        # Перевірка, щоб y > 0 (інакше логарифм не існує)
        if any(y <= 0 for y in y_values):
            raise ValueError("Усі значення y повинні бути додатніми для логарифмування")

        ln_y = [np.log(y) for y in y_values]
        n = sum(n_values)

        sum_xn = np.sum([x * n for x, n in zip(x_values, n_values)])
        sum_x2n = np.sum([x**2 * n for x, n in zip(x_values, n_values)])
        sum_ln_y = np.sum([n * y for n, y in zip(n_values, ln_y)])
        sum_xn_ln_y = np.sum([x * n * y for x, n, y in zip(x_values, n_values, ln_y)])

        A = np.array([
            [sum_xn, n],
            [sum_x2n, sum_xn]
        ])

        B = np.array([
            sum_ln_y,
            sum_xn_ln_y
        ])

        ln_b, ln_a = np.linalg.solve(A, B)

        a = np.exp(ln_a)
        b = np.exp(ln_b)

        return b, a  # бо y = b * a^x
    
    def find_coefficients_root_regresion(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по стовпцях
        conditional_means = self.get_conditional_means_table()

        x_values = df.columns
        n_values = ni.values
        y_conditional = [conditional_means[x] for x in x_values]

        n = sum(n_values)
        sum_sqrt_xn = np.sum([(np.sqrt(x)) * n for x, n in zip(x_values, n_values)])
        sum_xn = np.sum([(x) * n for x, n in zip(x_values, n_values)])

        sum_sqrt_xn_y = np.sum([(np.sqrt(x))* n * y for x, n, y in zip(x_values, n_values, y_conditional)])
        sum_n_y = np.sum([n * y for n, y in zip(n_values, y_conditional)])

        A = np.array([
            [sum_sqrt_xn, n],
            [sum_xn, sum_sqrt_xn],
        ])

        B = np.array([
            sum_n_y,
            sum_sqrt_xn_y
        ])

        coeffs = np.linalg.solve(A, B)
        a, b = coeffs

        return a, b



    # ------------------- Тест за статистикою Фішера -------------------
    def F_criteria_adequacy_test(self, type, alpha):
        df = self.corerlation_table

        m = None
        n = sum(df.sum(axis=0))
        F_emperical = None
        F_critical = None
        Q = None
        Qp = None
        Qo = None

        if type == "parabolic":
            m = 3
            Q, Qp, Qo = self.get_variations_parabolic_correlation()
            

        if type == "giperbolic":
            m = 2
            Q, Qp, Qo = self.get_variations_giperbolic_correlation()

        if type == "exponential":
            m = 2
            Q, Qp, Qo = self.get_variations_exponential_correlation()
        
        if type == "root":
            m = 2
            Q, Qp, Qo = self.get_variations_root_correlation()


        F_emperical = (Qp*(n - m))/(Qo*(m - 1))
        F_critical = f.ppf(1 - alpha, m-1, n-m)

        is_accepted = F_emperical < F_critical

        return Q, Qp, Qo, F_emperical, F_critical, is_accepted


    # -------------------- Варіації ------------------------------------
    def get_variations(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по x
        conditional_means = self.get_conditional_means_table()
        x_values = df.columns

        # Загальне середнє значення y
        total_y_sum = sum([conditional_means[x] * ni[x] for x in x_values])
        total_n = sum(ni)
        y_mean = total_y_sum / total_n

        # Коефіцієнти регресії
        a, b = self.find_coefficients_liner_regresion()

        # Обчислення варіацій
        general_variation = sum([ni[x] * (conditional_means[x] - y_mean) ** 2 for x in x_values])
        regression_variation = sum([ni[x] * ((a * x + b) - y_mean) ** 2 for x in x_values])
        residuals_variation = sum([ni[x] * (conditional_means[x] - (a * x + b)) ** 2 for x in x_values])

        return general_variation, regression_variation, residuals_variation
    
    def get_variations_parabolic_correlation(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по x
        conditional_means = self.get_conditional_means_table()
        x_values = df.columns

        # Загальне середнє значення y
        total_y_sum = sum([conditional_means[x] * ni[x] for x in x_values])
        total_n = sum(ni)
        y_mean = total_y_sum / total_n

        # Коефіцієнти регресії
        a, b, c = self.find_coefficients_parabolic_regresion()

        # Обчислення варіацій
        general_variation = sum([ni[x] * (conditional_means[x] - y_mean) ** 2 for x in x_values])
        regression_variation = sum([ni[x] * ((a * x**2 + b * x + c) - y_mean) ** 2 for x in x_values])
        residuals_variation = sum([ni[x] * (conditional_means[x] - (a * x**2 + b * x + c)) ** 2 for x in x_values])

        return general_variation, regression_variation, residuals_variation
    
    def get_variations_giperbolic_correlation(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по x
        conditional_means = self.get_conditional_means_table()
        x_values = df.columns

        # Загальне середнє значення y
        total_y_sum = sum([conditional_means[x] * ni[x] for x in x_values])
        total_n = sum(ni)
        y_mean = total_y_sum / total_n

        # Коефіцієнти регресії
        a, b = self.find_coefficients_giperbolic_regresion()

        # Обчислення варіацій
        general_variation = sum([ni[x] * (conditional_means[x] - y_mean) ** 2 for x in x_values])
        regression_variation = sum([ni[x] * (((a/x) + b) - y_mean) ** 2 for x in x_values])
        residuals_variation = sum([ni[x] * (conditional_means[x] - ((a/x) + b)) ** 2 for x in x_values])

        return general_variation, regression_variation, residuals_variation

    def get_variations_exponential_correlation(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по x
        conditional_means = self.get_conditional_means_table()
        x_values = df.columns

        # Загальне середнє значення y
        total_y_sum = sum([conditional_means[x] * ni[x] for x in x_values])
        total_n = sum(ni)
        y_mean = total_y_sum / total_n

        # Коефіцієнти регресії
        a, b = self.find_coefficients_exponential_regresion()

        # Обчислення варіацій
        general_variation = sum([ni[x] * (conditional_means[x] - y_mean) ** 2 for x in x_values])
        regression_variation = sum([ni[x] * ((b*(a**x)) - y_mean) ** 2 for x in x_values])
        residuals_variation = sum([ni[x] * (conditional_means[x] - (b*(a**x))) ** 2 for x in x_values])

        return general_variation, regression_variation, residuals_variation
    
    def get_variations_root_correlation(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по x
        conditional_means = self.get_conditional_means_table()
        x_values = df.columns

        # Загальне середнє значення y
        total_y_sum = sum([conditional_means[x] * ni[x] for x in x_values])
        total_n = sum(ni)
        y_mean = total_y_sum / total_n

        # Коефіцієнти регресії
        a, b = self.find_coefficients_root_regresion()

        # Обчислення варіацій
        general_variation = sum([ni[x] * (conditional_means[x] - y_mean) ** 2 for x in x_values])
        regression_variation = sum([ni[x] * ((a * np.sqrt(x) + b) - y_mean) ** 2 for x in x_values])
        residuals_variation = sum([ni[x] * (conditional_means[x] - (a * np.sqrt(x) + b)) ** 2 for x in x_values])

        return general_variation, regression_variation, residuals_variation

    def calculate_determination_coefficient(self):
        Q, Qp, Qo = self.get_variations()
        return Qp/Q
    
    # 5. Обчислити вибірковий лінійний коефіцієнт кореляції.
    def calculate_sample_linear_correlation_coefficient(self):
        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по x
        conditional_means = self.get_conditional_means_table()
        x_values = df.columns

        # Загальне середнє значення y
        total_y_sum = sum([conditional_means[x] * ni[x] for x in x_values])
        total_n = sum(ni)
        y_mean = total_y_sum / total_n

        # Обчислення середнього значення x
        x_mean = sum([x * ni[x] for x in x_values]) / total_n

        # Чисельник: сума добутків різниць від середніх
        numerator = np.sum([(x - x_mean) * (conditional_means[x] - y_mean) * ni[x] for x in x_values])

        # Знаменник: корінь добутку варіацій x та y, зважених по частотах
        denominator = np.sqrt(np.sum([(x - x_mean)**2 * ni[x] for x in x_values]) *
                            np.sum([(conditional_means[x] - y_mean)**2 * ni[x] for x in x_values]))

        # Обчислюємо коефіцієнт кореляції
        r = numerator / denominator

        return r
    
    def check_correlation_coefficient_statistical_significance(self, alpha):
        r = self.calculate_sample_linear_correlation_coefficient()

        df = self.corerlation_table
        ni = df.sum(axis=0)  # суми по x
        n = sum(ni)

        df = n - 2

        t_emperical =  r*np.sqrt(n - 2)/np.sqrt(1 - r**2)

        t_critical = t.ppf(1 - alpha/2, df) 

        if_accepted = abs(t_emperical) < t_critical

        return t_emperical, t_critical, if_accepted
    
    def get_forecasted_value(self, x):
        a, b = self.find_coefficients_exponential_regresion()
        return b * a ** x
    
    

    














        
    

    
    