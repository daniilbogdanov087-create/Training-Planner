import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data = []

        # Создание формы для ввода
        self.create_form()

        # Создание таблицы для отображения
        self.create_table()

        # Создание кнопок
        self.create_buttons()

        # Загруженные данные
        self.load_data()

    def create_form(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill='x')

        # Дата
        ttk.Label(frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky='w')
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1, sticky='ew')

        # Тип тренировки
        ttk.Label(frame, text="Тип тренировки:").grid(row=0, column=2, sticky='w')
        self.type_var = tk.StringVar()
        self.type_combobox = ttk.Combobox(frame, textvariable=self.type_var)
        self.type_combobox['values'] = ("Кардио", "Силовая", "Растяжка", "Йога")
        self.type_combobox.grid(row=0, column=3, sticky='ew')

        # Длительность
        ttk.Label(frame, text="Длительность (мин):").grid(row=0, column=4, sticky='w')
        self.duration_entry = ttk.Entry(frame)
        self.duration_entry.grid(row=0, column=5, sticky='ew')

        # Настройка колонок
        for i in range(6):
            frame.columnconfigure(i, weight=1)

    def create_table(self):
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Тип", "Длительность"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип тренировки")
        self.tree.heading("Длительность", text="Длительность (мин)")
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

    def create_buttons(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill='x')

        add_button = ttk.Button(frame, text="Добавить тренировку", command=self.add_training)
        add_button.pack(side='left', padx=5)

        save_button = ttk.Button(frame, text="Сохранить в JSON", command=self.save_to_json)
        save_button.pack(side='left', padx=5)

        load_button = ttk.Button(frame, text="Загрузить из JSON", command=self.load_from_json)
        load_button.pack(side='left', padx=5)

        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(filter_frame, text="Фильтр по типу:").pack(side='left')
        self.filter_type_var = tk.StringVar()
        self.filter_type_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_type_var)
        self.filter_type_combobox['values'] = ("Все", "Кардио", "Силовая", "Растяжка", "Йога")
        self.filter_type_combobox.current(0)
        self.filter_type_combobox.pack(side='left', padx=5)

        ttk.Label(filter_frame, text="Фильтр по дате:").pack(side='left')
        self.filter_date_entry = ttk.Entry(filter_frame)
        self.filter_date_entry.pack(side='left', padx=5)

        filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_button.pack(side='left', padx=5)

        reset_button = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.load_data)
        reset_button.pack(side='left', padx=5)

    def add_training(self):
        date_str = self.date_entry.get()
        training_type = self.type_var.get()
        duration_str = self.duration_entry.get()

        # Проверка данных
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return
        if not duration_str.isdigit() or int(duration_str) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        entry = {
            "date": date_str,
            "type": training_type,
            "duration": int(duration_str)
        }
        self.data.append(entry)
        self.update_table()
        self.clear_form()

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def clear_form(self):
        self.date_entry.delete(0, tk.END)
        self.type_combobox.set('')
        self.duration_entry.delete(0, tk.END)

    def update_table(self, filtered_data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data_to_show = filtered_data if filtered_data is not None else self.data
        for entry in data_to_show:
            self.tree.insert('', 'end', values=(entry["date"], entry["type"], entry["duration"]))

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.update_table()

    def load_data(self):
        # Можно реализовать загрузку из файла по умолчанию, пока оставим пустым
        self.data = []
        self.update_table()

    def apply_filter(self):
        filter_type = self.filter_type_var.get()
        filter_date = self.filter_date_entry.get()

        filtered = self.data

        if filter_type != "Все":
            filtered = [d for d in filtered if d["type"] == filter_type]
        if filter_date:
            if self.validate_date(filter_date):
                filtered = [d for d in filtered if d["date"] == filter_date]
            else:
                messagebox.showerror("Ошибка", "Некорректный формат даты для фильтра.")
                return
        self.update_table(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()