import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Processor:

    def __init__(self, n: int):
        self.n= n
        self.sample = self.generte_random_sample(self.n)
        self.variation_range = self.get_variation_range()
        self.freq_table = self.get_freq_table()
        self.freq_table_with_relative_freq = self.get_freq_table_with_relative_freq()

    def generte_random_sample(self, n: int):
        low = 2
        high = 12

        return np.random.randint(low, high, self.n)
 

    def get_freq_table(self):
        return pd.Series(self.variation_range).value_counts().sort_index().reset_index(name="Частота").rename(columns={"index": "Значення"})
    
    
    def get_freq_table_with_relative_freq(self):
        to_return = self.freq_table[["Частота", "Значення"]].copy()
        to_return["Відносна частота"] =  to_return["Частота"] / self.n
        to_return["Відносна частота"] = to_return["Відносна частота"].round(6)
        return to_return

    #дописати власне сортування
    def get_variation_range(self):
        return np.sort(self.sample) 
    
    def show_freq_diagram(self):
        x = self.freq_table["Значення"]
        y = self.freq_table["Частота"]

        plt.figure(figsize=(8,6), num="Діаграма Частот")
        plt.bar(x, y, color="red")

        plt.title("Діаграма частот статистичного матеріалу")
        plt.xlabel("Значення")
        plt.ylabel("Частота")
        plt.legend()

        plt.xticks(x)

        plt.show()

    def show_freq_polygon(self):
        plt.close("all")


        x = self.freq_table["Значення"]
        y = self.freq_table["Частота"]

        plt.figure(figsize=(8,6), num="Полігон Частот")
        plt.plot(x, y, marker="o", linestyle="-", color="red")

        plt.title("Полігон частот статистичного матеріалу")
        plt.xlabel("Значення")
        plt.ylabel("Частота")
        plt.legend()

        plt.xticks(x)

        plt.show()

    def show_empire_function(self):
        plt.close("all")  # Закриває всі попередні графіки

        x = self.freq_table_with_relative_freq["Значення"]
        w = self.freq_table_with_relative_freq["Відносна частота"]

        y = [0]
        for i in range(len(w)):  # Використовуємо len(w), а не self.n
            y.append(y[i] + w[i])

        plt.figure(figsize=(8,6), num="Графік Емпіричної Функції")

        plt.step(x, y[1:], where="post", alpha = 0,color="black", label="Empire function", zorder=1)

        for i in range(len(w) - 1):
            plt.arrow(x.iloc[i], y[i + 1], x.iloc[i + 1] - x.iloc[i], 0, 
                    head_width=0.03, head_length=0.5, length_includes_head=True, 
                    color="black", linewidth=1, zorder=2)
        
        last_x = x.iloc[-1]
        last_y = y[-1]
        plt.arrow(last_x, last_y, 1, 0, head_width=0.03, head_length=0.5, 
                length_includes_head=True, color="black", linewidth=1, zorder=2)

        plt.xlabel("Значення")
        plt.ylabel("Значення емпіричної функції")
        plt.title("Графік емпіричної функції розподілу")
        plt.yticks(y)
        plt.xticks(x)
        plt.legend()
        plt.grid()
        plt.show()

    #статистики центральної тенденції
    def mode(self):
        max_freq = self.freq_table["Частота"].max()
        return self.freq_table[self.freq_table["Частота"] == max_freq]["Значення"]
    
    def median(self):
        half = self.n//2
        if self.n % 2 == 0:
            return (self.variation_range[half - 1] + self.variation_range[half])/2
        
        return self.variation_range[half]
 
    def mean(self):
        total = 0
        for i in range(len(self.freq_table["Значення"])):  # Використовуємо наявні індекси таблиці
            total += self.freq_table.loc[i, "Значення"] * self.freq_table.loc[i, "Частота"]

        return total / self.n  # Ділимо на загальну кількість елементів у вибірці

    import pandas as pd

    def get_interquartile_latitudes_df(self):
        Q = self.get_Qs()
        O = self.get_Os()
        D = self.get_Ds()
        C = self.get_Cs()
        M = self.get_Ms()

        quantile_types = {
            "Характеристика": [
                "Інтерквартильна широта", "Інтероктильна широта", 
                "Інтердецильна широта", "Інтерцентильна широта", "Інтермілільна широта"
            ],
            "Значення": [
                self.calculate_range(Q),
                self.calculate_range(O),
                self.calculate_range(D),
                self.calculate_range(C),
                self.calculate_range(M)
            ]
        }

        return pd.DataFrame(quantile_types)


    def calculate_range(self, quantiles):
        """Обчислює широту, якщо значення знайдено"""
        if quantiles is None:
            return None
        return quantiles[-1] - quantiles[0]


    def get_Qs(self):
        return self.get_quantiles(4)

    def get_Os(self):
        return self.get_quantiles(8)

    def get_Ds(self):
        return self.get_quantiles(10)

    def get_Cs(self):
        return self.get_quantiles(100)

    def get_Ms(self):
        return self.get_quantiles(1000)


    def get_quantiles(self, k):
        """Універсальний метод для знаходження квантилів"""
        if self.n % k != 0:
            return None  # Якщо n не ділиться на k, квантилі не можна знайти

        x = self.freq_table["Значення"]
        cum_sum = self.freq_table["Частота"].cumsum()  # Кумулятивна сума частот

        quantile_positions = [(self.n * i) // k for i in range(1, k)]  # Цілі позиції квантилів

        quantiles = []
        for pos in quantile_positions:
            quantile_value = x.loc[cum_sum >= pos].iloc[0]  # Перше значення, де сума частот ≥ pos
            quantiles.append(quantile_value)

        return quantiles


    def get_ct_characteristics_df(self):
        data = {
            "Характеристика": ["Мода", "Медіана", "Середнє значення", "Розмах", "Варіанса", 
                            "Стандарт", "Варіація", "Дисперсія", "Середнє квадратичне відхилення", "Асиметрія", "Ексцес"],
            "Значення": [
                ", ".join(map(str, self.mode())),  # Мода може мати кілька значень
                self.median().round(),
                self.mean().round(),
                self.range(),
                self.variance().round(4),
                self.standart().round(4),
                self.variation().round(4),
                self.dispersion().round(4),
                self.quadratic_deviation().round(4),
                self.asymmetry().round(4),
                self.excess().round(4)
            ]
        }

        return pd.DataFrame(data)

    
    #статистики розсіяння   

    def deviation(self):
        sum = 0
        mean_value = self.mean()

        for i in range(len(self.freq_table["Значення"])):
            sum += (self.freq_table.loc[i, "Значення"] - mean_value )**2 * self.freq_table.loc[i, "Частота"]

        return sum

    def range(self):
        return self.variation_range[-1] - self.variation_range[0]
    
    def variance(self):
        return self.deviation()/self.n - 1
    
    def standart(self):
        return self.variance()**0.5
    
    def variation(self):
        return self.standart()/self.mean()
    
    def dispersion(self):
        return self.deviation()/self.n
    
    def quadratic_deviation(self):
        return self.dispersion()**0.5
    
    #статистики форми

    def calculate_moment(self, k):
        total = 0
        mean_value = self.mean()

        for i in range(len(self.freq_table)):
            total += ((self.freq_table.loc[i, "Значення"] - mean_value)**k)*self.freq_table.loc[i, "Частота"]
            
        return total/self.n
    
    def asymmetry(self):
        return self.calculate_moment(3)/self.calculate_moment(2)**1.5 
    
    def excess(self):
        return self.calculate_moment(4)/self.calculate_moment(2)**2 - 3
    
    # інтервальний стат розподіл

    def calculate_k(self):
        return 1 + 3.322*np.log(self.n)
    
    def calculate_h(self):
        return (self.variation_range[-1]  - self.variation_range[0])/self.calculate_k()
    
    def get_interval_distribution_df(self):
        #формуємо межі іетервалів
        h = self.calculate_h()
        k = self.calculate_k()
        var_range = self.variation_range

        bins = np.arange(var_range[0], var_range[-1] + h, h)

        freq, _ = np.histogram(var_range, bins=bins)

        # Формуємо таблицю
        intervals = [f"[{round(bins[i], 2)} - {round(bins[i+1], 2)})" for i in range(len(bins) - 1)]
        df = pd.DataFrame({"Інтервал": intervals, "Частота": freq})
        
        return df, bins, freq
    
    def show_interval_destribution_histogram(self):
        df, bins, freq = self.get_interval_distribution_df()

        h = self.calculate_h()

        ni_over_h = [f / h for f in freq]

        plt.figure(figsize=(8,6), num="Графік гістограми інетервального розподілу варіанси")

        plt.bar(bins[:-1], ni_over_h, width=np.diff(bins), align='edge', edgecolor='black', color="red")
        plt.xlabel('Значення')
        plt.ylabel('ni / h')
        plt.title('Гістограма інтервального розподілу')
        plt.xticks(bins, rotation=45)
        plt.yticks(ni_over_h)
        plt.show()

    
    def show_empirical_function_interval_distribution(self):
        df, bins, freq = self.get_interval_distribution_df()

        total_count = self.n  # Загальна кількість елементів
        relative_freq = [f / total_count for f in freq]  # Відносні частоти

        cumulative_freq = [sum(relative_freq[:i+1]) for i in range(len(relative_freq))]  # Накопичена частота

        x_values = []
        y_values = []

        for i in range(1, len(bins)):  # Iterate until len(bins) - 1
            x_i = bins[i - 1]
            y_i = (relative_freq[i - 1] / (bins[i] - bins[i - 1])) * (x_i - bins[i-1]) + cumulative_freq[i-1]
            
            x_values.append(x_i)
            y_values.append(y_i)
        
        plt.close("all") 

        # Побудова графіка
        plt.plot(x_values, y_values, label="Емпірична функція розподілу", color="blue")
        plt.scatter(bins[:-1], cumulative_freq, color="red", zorder=3)  # Точки на графіку
        plt.xlabel("x")
        plt.ylabel("F(x)")
        plt.xticks(x_values,  rotation=45)
        plt.yticks(y_values, rotation=45)
        plt.title("Графік емпіричної функції неперервного розподілу")
        plt.grid(True)
        plt.legend()
        plt.show()

    # числові характеристики для інтервального розподілу
    
    """def get_interval_mode(self):
        df, bins, freq = self.get_interval_distribution_df()

        # Initialize variables to track the maximum frequency and its index
        max_freq = freq[0]
        max_freq_index = 0

        # Loop through the frequencies to find the maximum
        for i in range(1, len(freq)):
            if freq[i] > max_freq:
                max_freq = freq[i]
                max_freq_index = i

        # Get the interval with the maximum frequency
        mode_interval = f"[{round(bins[max_freq_index], 2)} - {round(bins[max_freq_index + 1], 2)})"
        
        # Return the mode interval and the frequency
        return mode_interval, max_freq
    """
    def mode_for_interval_destribution(self):

        # Get the frequency and bins
        df, bins, freq = self.get_interval_distribution_df()

        # Find the index of the modal class (the class with the highest frequency)
        max_index = np.argmax(freq)  # Index of the modal class

        # Get the boundaries and frequencies for the modal class and its neighbors
        L = bins[max_index]  # Lower boundary of the modal class
        nmo = freq[max_index]  # Frequency of the modal class
        nmo_minus_1 = freq[max_index - 1] if max_index > 0 else 0  # Frequency of the previous class
        nmo_plus_1 = freq[max_index + 1] if max_index < len(freq) - 1 else 0  # Frequency of the next class
        hmo = bins[max_index + 1] - bins[max_index]  # Width of the modal class
        hmo_minus_1 = bins[max_index] - bins[max_index - 1] if max_index > 0 else 0  # Width of the previous class

        # Apply the formula to calculate the mode
        mode = L + ((nmo - nmo_minus_1) / ((nmo - nmo_minus_1) + (nmo - nmo_plus_1))) * (hmo - hmo_minus_1)

        return mode
    
    def median_for_interval_destribution(self):
        # Get the frequency and bins
        df, bins, freq = self.get_interval_distribution_df()
        
        # Total number of data points
        n = self.n

        # Calculate the cumulative frequencies
        cumulative_freq = [sum(freq[:i+1]) for i in range(len(freq))]

        # Find the median class: the class where the cumulative frequency is >= n/2
        half_n = n / 2
        median_class_index = 0
        for i in range(len(cumulative_freq)):
            if cumulative_freq[i] >= half_n:
                median_class_index = i
                break

        # Values for the median formula
        L_me = bins[median_class_index]  # Lower boundary of the median class
        F_m_minus_1 = cumulative_freq[median_class_index - 1] if median_class_index > 0 else 0  # Cumulative frequency before the median class
        f_m = freq[median_class_index]  # Frequency of the median class
        h_m = bins[median_class_index + 1] - bins[median_class_index]  # Width of the median class

        # Apply the formula to calculate the median
        median = L_me + ((half_n - F_m_minus_1) / f_m) * h_m

        return median
    
    def get_interval_destribution_middle_values(self):
        bins = self.get_interval_distribution_df()[1]

        return [(bins[i+1] + bins[i]) / 2 for i in range(len(bins) - 1)]
    
    def mean_for_interval_destribution(self):
        freq = self.get_interval_distribution_df()[2]
        middle_values = self.get_interval_destribution_middle_values()

        total = 0
        for i in range(len(middle_values)):  # Використовуємо наявні індекси таблиці
            total += middle_values[i] * freq[i]

        return total/self.n

    def deviation_for_interval_destribution(self):
        freq = self.get_interval_distribution_df()[2]
        middle_values = self.get_interval_destribution_middle_values()

        sum = 0
        mean_value = self.mean_for_interval_destribution()

        for i in range(len(freq)):
            sum += (middle_values[i] - mean_value )**2 * freq[i]

        return sum

    def range_for_interval_destribution(self):
        middle_values = self.get_interval_destribution_middle_values()
        return middle_values[-1] - middle_values[0]
    
    def variance_for_interval_destribution(self):
        return self.deviation_for_interval_destribution()/(self.n - 1)
    
    def standart_for_interval_destribution(self):
        return self.variance_for_interval_destribution()**0.5
    
    def variation_for_interval_destribution(self):
        return self.standart_for_interval_destribution()/self.mean_for_interval_destribution()
    
    def dispersion_for_interval_destribution(self):
        return self.deviation_for_interval_destribution()/self.n
    
    def quadratic_deviation_for_interval_destribution(self):
        return self.dispersion_for_interval_destribution()**0.5
    
    #статистики форми

    def calculate_moment_for_interval_destribution(self, k):
        freq = self.get_interval_distribution_df()[2]
        middle_values = self.get_interval_destribution_middle_values()

        total = 0
        mean_value = self.mean_for_interval_destribution()

        for i in range(len(freq)):
            total += (( middle_values[i] - mean_value)**k)*freq[i]
            
        return total/self.n
    
    def asymmetry_for_interval_destribution(self):
        return self.calculate_moment_for_interval_destribution(3)/self.calculate_moment_for_interval_destribution(2)**1.5 
    
    def excess_for_interval_destribution(self):
        return self.calculate_moment_for_interval_destribution(4)/self.calculate_moment_for_interval_destribution(2)**2 - 3
    
    def get_interval_characteristics_df(self):
        data = {
            "Характеристика": ["Мода", "Медіана", "Середнє значення", "Розмах", "Варіанса", 
                            "Стандарт", "Варіація", "Дисперсія", "Середнє квадратичне відхилення", "Асиметрія", "Ексцес"],
            "Значення": [
                self.mode_for_interval_destribution().round(4),  # Мода може мати кілька значень
                self.median_for_interval_destribution().round(4),
                self.mean_for_interval_destribution().round(4),
                self.range_for_interval_destribution().round(4),
                self.variance_for_interval_destribution().round(4),
                self.standart_for_interval_destribution().round(4),
                self.variation_for_interval_destribution().round(4),
                self.dispersion_for_interval_destribution().round(4),
                self.quadratic_deviation_for_interval_destribution().round(4),
                self.asymmetry_for_interval_destribution().round(4),
                self.excess_for_interval_destribution().round(4)
            ]
        }

        return pd.DataFrame(data)








    



    





    


