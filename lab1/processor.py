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

        plt.xticks(x)

        plt.show()

    def show_freq_polygon(self):
        x = self.freq_table["Значення"]
        y = self.freq_table["Частота"]

        plt.figure(figsize=(8,6), num="Полігон Частот")
        plt.plot(x, y, marker="o", linestyle="-", color="red")

        plt.title("Полігон частот статистичного матеріалу")
        plt.xlabel("Значення")
        plt.ylabel("Частота")

        plt.xticks(x)

        plt.show()

    


