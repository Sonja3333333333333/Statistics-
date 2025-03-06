import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ContinuousProcessor:
    def __init__(self, n: int):
        self.n= n
        self.sample = self.generte_random_sample()
        self.variation_range = self.get_variation_range()
        '''self.freq_table = self.get_freq_table()
        self.freq_table_with_relative_freq = self.get_freq_table_with_relative_freq()'''
    
    def generte_random_sample(self):
        low = 2
        high = 12

        return np.round(np.random.uniform( low, high, self.n), 4)
    
    #дописати власне сортування
    def get_variation_range(self):
        return np.sort(self.sample) 
    
    def get_freq_table(self):
        return pd.Series(self.variation_range).value_counts().sort_index().reset_index(name="Частота").rename(columns={"index": "Значення"})
    
    
    def get_freq_table_with_relative_freq(self):
        to_return = self.freq_table[["Частота", "Значення"]].copy()
        to_return["Відносна частота"] =  to_return["Частота"] / self.n
        to_return["Відносна частота"] = to_return["Відносна частота"].round(6)
        return to_return
    
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
        intervals = [f"[{round(bins[i], 4)} - {round(bins[i+1], 4)})" for i in range(len(bins) - 1)]
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

    def mode(self):

        # Get the frequency and bins
        df, bins, freq = self.get_interval_distribution_df()

        # Find the index of the modal class (the class with the highest frequency)
        max_index = np.argmax(freq) # Index of the modal class

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
    
    def median(self):
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
    
    def mean(self):
        freq = self.get_interval_distribution_df()[2]
        middle_values = self.get_interval_destribution_middle_values()

        total = 0
        for i in range(len(middle_values)):  # Використовуємо наявні індекси таблиці
            total += middle_values[i] * freq[i]

        return total/self.n

    def deviation(self):
        freq = self.get_interval_distribution_df()[2]
        middle_values = self.get_interval_destribution_middle_values()

        sum = 0
        mean_value = self.mean()

        for i in range(len(freq)):
            sum += (middle_values[i] - mean_value )**2 * freq[i]

        return sum

    def range(self):
        middle_values = self.get_interval_destribution_middle_values()
        return middle_values[-1] - middle_values[0]
    
    def variance(self):
        return self.deviation()/(self.n - 1)
    
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
        freq = self.get_interval_distribution_df()[2]
        middle_values = self.get_interval_destribution_middle_values()

        total = 0
        mean_value = self.mean()

        for i in range(len(freq)):
            total += (( middle_values[i] - mean_value)**k)*freq[i]
            
        return total/self.n
    
    def asymmetry(self):
        return self.calculate_moment(3)/self.calculate_moment(2)**1.5 
    
    def excess(self):
        return self.calculate_moment(4)/self.calculate_moment(2)**2 - 3
    
    def get_interval_characteristics_df(self):
        data = {
            "Характеристика": ["Мода", "Медіана", "Середнє значення", "Розмах", "Варіанса", 
                            "Стандарт", "Варіація", "Дисперсія", "Середнє квадратичне відхилення", "Асиметрія", "Ексцес"],
            "Значення": [
                self.mode().round(4),  # Мода може мати кілька значень
                self.median().round(4),
                self.mean().round(4),
                self.range().round(4),
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
    

    

