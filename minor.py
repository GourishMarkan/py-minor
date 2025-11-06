import tkinter as tk
import random
import time

# ---------------- Sorting Algorithms ----------------
def bubble_sort(data, draw_data, speed):
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                draw_data(data, ['red' if x == j or x == j+1 else 'blue' for x in range(len(data))])
                time.sleep(speed)
    draw_data(data, ['green' for _ in range(len(data))])

def insertion_sort(data, draw_data, speed):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j+1] = data[j]
            j -= 1
            draw_data(data, ['red' if x == j or x == j+1 else 'blue' for x in range(len(data))])
            time.sleep(speed)
        data[j+1] = key
    draw_data(data, ['green' for _ in range(len(data))])

def merge_sort(data, draw_data, speed):
    merge_sort_alg(data, 0, len(data)-1, draw_data, speed)
    draw_data(data, ['green' for _ in range(len(data))])

def merge_sort_alg(data, left, right, draw_data, speed):
    if left < right:
        mid = (left + right) // 2
        merge_sort_alg(data, left, mid, draw_data, speed)
        merge_sort_alg(data, mid + 1, right, draw_data, speed)
        merge(data, left, mid, right, draw_data, speed)

def merge(data, left, mid, right, draw_data, speed):
    left_part = data[left:mid+1]
    right_part = data[mid+1:right+1]
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            data[k] = left_part[i]
            i += 1
        else:
            data[k] = right_part[j]
            j += 1
        k += 1
        draw_data(data, ['red' if x == k else 'blue' for x in range(len(data))])
        time.sleep(speed)
    while i < len(left_part):
        data[k] = left_part[i]
        i += 1
        k += 1
        draw_data(data, ['blue' for _ in range(len(data))])
        time.sleep(speed)
    while j < len(right_part):
        data[k] = right_part[j]
        j += 1
        k += 1
        draw_data(data, ['blue' for _ in range(len(data))])
        time.sleep(speed)

def quick_sort(data, low, high, draw_data, speed):
    if low < high:
        pi = partition(data, low, high, draw_data, speed)
        quick_sort(data, low, pi - 1, draw_data, speed)
        quick_sort(data, pi + 1, high, draw_data, speed)

def partition(data, low, high, draw_data, speed):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
        draw_data(data, ['red' if x == j or x == i else 'blue' for x in range(len(data))])
        time.sleep(speed)
    data[i+1], data[high] = data[high], data[i+1]
    return i + 1

# ---------------- Rule-Based AI ----------------
def recommend_algorithm(data):
    n = len(data)
    sortedness = sum(data[i] <= data[i+1] for i in range(n-1)) / (n-1)
    duplicates = 1 - len(set(data)) / n

    if n <= 20:
        return "Insertion Sort"
    elif sortedness > 0.8:
        return "Insertion Sort"
    elif duplicates > 0.4:
        return "Quick Sort"
    elif n > 50:
        return "Merge Sort"
    else:
        return "Bubble Sort"

# ---------------- GUI Class ----------------
class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title('AI-Based Sorting Visualizer')
        self.root.config(bg='black')
        self.data = []
        self.speed = 0.1
        self.algorithm = None

        # UI Frame
        ui = tk.Frame(root, width=900, height=200, bg='grey')
        ui.grid(row=0, column=0, padx=10, pady=5)

        tk.Button(ui, text='Generate Array', command=self.generate).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(ui, text='AI Recommend', command=self.ai_recommend).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(ui, text='Start Sorting', command=self.start_sorting).grid(row=0, column=2, padx=5, pady=5)

        self.label = tk.Label(ui, text='', bg='grey', font=('Arial', 12, 'bold'))
        self.label.grid(row=1, column=1, padx=5, pady=5)

        self.canvas = tk.Canvas(root, width=870, height=380, bg='white')
        self.canvas.grid(row=1, column=0, padx=10, pady=5)

    def generate(self):
        self.data = [random.randint(10, 150) for _ in range(random.randint(15, 60))]
        self.draw_data(self.data, ['blue' for _ in range(len(self.data))])
        self.label.config(text="Array Generated")

    def ai_recommend(self):
        if not self.data:
            self.label.config(text="Generate data first!")
            return
        algo = recommend_algorithm(self.data)
        self.algorithm = algo
        self.label.config(text=f"AI Recommendation: {algo}")

    def start_sorting(self):
        if not self.algorithm or not self.data:
            self.label.config(text="Generate & Recommend first!")
            return
        if self.algorithm == "Bubble Sort":
            bubble_sort(self.data, self.draw_data, self.speed)
        elif self.algorithm == "Insertion Sort":
            insertion_sort(self.data, self.draw_data, self.speed)
        elif self.algorithm == "Merge Sort":
            merge_sort(self.data, self.draw_data, self.speed)
        elif self.algorithm == "Quick Sort":
            quick_sort(self.data, 0, len(self.data)-1, self.draw_data, self.speed)
            self.draw_data(self.data, ['green' for _ in range(len(self.data))])
        self.label.config(text=f"{self.algorithm} Completed!")

    def draw_data(self, data, color_array):
        self.canvas.delete("all")
        c_height, c_width = 380, 870
        x_width = c_width / (len(data) + 1)
        offset, spacing = 10, 5
        normalized = [i / max(data) for i in data]
        for i, height in enumerate(normalized):
            x0 = i * x_width + offset + spacing
            y0 = c_height - height * 340
            x1 = (i + 1) * x_width + offset
            y1 = c_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
        self.root.update_idletasks()

root = tk.Tk()
app = SortingVisualizer(root)
root.mainloop()
