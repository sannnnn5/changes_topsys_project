import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class CarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Comparison App")
        self.create_widgets()
        self.style_widgets()

    def create_widgets(self):
        self.entries = {
            'Model': [],
            'Price': [],
            'Range (miles)': [],
            'Power': [],
            '0-100 km/h (seconds)': [],
            'Top Speed (mph)': []
        }

        self.labels = ['Model', 'Price', 'Range (miles)', 'Power', '0-100 km/h (seconds)', 'Top Speed (mph)']
        for i, label in enumerate(self.labels):
            lbl = ttk.Label(self.root, text=label)
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky='W')

            entry = ttk.Entry(self.root)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='W')
            self.entries[label] = entry

        self.add_button = ttk.Button(self.root, text="Add Car", command=self.add_car, style="Custom.TButton")
        self.add_button.grid(row=len(self.labels), column=0, columnspan=2, pady=10)

        self.submit_button = ttk.Button(self.root, text="Submit", command=self.calculate, style="Custom.TButton")
        self.submit_button.grid(row=len(self.labels) + 1, column=0, columnspan=2, pady=10)

        self.edit_button = ttk.Button(self.root, text="Edit Car", command=self.edit_car, style="Custom.TButton")
        self.edit_button.grid(row=len(self.labels) + 2, column=0, columnspan=2, pady=10)

        self.reset_button = ttk.Button(self.root, text="Reset", command=self.reset, style="Custom.TButton")
        self.reset_button.grid(row=len(self.labels) + 3, column=0, columnspan=2, pady=10)

        # Add a frame to contain the Listbox and Scrollbar
        self.listbox_frame = ttk.Frame(self.root)
        self.listbox_frame.grid(row=len(self.labels) + 4, column=0, columnspan=2, pady=10)

        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.car_list = tk.Listbox(self.listbox_frame, height=10, width=50, yscrollcommand=self.scrollbar.set)
        self.car_list.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar.config(command=self.car_list.yview)

        self.car_data = {label: [] for label in self.labels}

    def style_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", background="#f0f0f0", foreground="#333333", font=("Helvetica", 12))
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("Custom.TButton", background="#007acc", foreground="#ffffff", font=("Helvetica", 12), padding=6)
        style.map("Custom.TButton",
                  background=[('active', '#005f9e'), ('disabled', '#a9a9a9')],
                  foreground=[('disabled', '#ffffff')])

        self.root.configure(bg="#f0f0f0")

    def add_car(self):
        car_details = []
        for label in self.labels:
            value = self.entries[label].get()
            if value:
                if label in ['Price', 'Range (miles)', 'Power', '0-100 km/h (seconds)', 'Top Speed (mph)']:
                    try:
                        value = float(value)
                    except ValueError:
                        messagebox.showerror("Invalid Input", f"Please enter a valid number for {label}.")
                        return
                self.car_data[label].append(value)
                self.entries[label].delete(0, tk.END)
                car_details.append(value)
            else:
                messagebox.showerror("Missing Data", f"Please enter a value for {label}.")
                return
        car_display = f"{car_details[0]} - Price: {car_details[1]}, Range: {car_details[2]}, Power: {car_details[3]}, 0-100 km/h: {car_details[4]}, Top Speed: {car_details[5]}"
        self.car_list.insert(tk.END, car_display)
        messagebox.showinfo("Car Added", "Car data added successfully!")

    def edit_car(self):
        selected_index = self.car_list.curselection()
        if not selected_index:
            messagebox.showerror("No Selection", "Please select a car to edit.")
            return

        selected_car = self.car_list.get(selected_index)
        car_details = selected_car.split(' - ')

        # Populate the entries with the selected car's details
        for label, value in zip(self.labels, car_details[1].split(', ')):
            entry_value = value.split(': ')[1]
            self.entries[label].delete(0, tk.END)
            self.entries[label].insert(0, entry_value)

        # Remove the selected car from the list and car_data
        for label in self.labels:
            self.car_data[label].pop(selected_index[0])
        self.car_list.delete(selected_index)

    def reset(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.car_list.delete(0, tk.END)
        self.car_data = {label: [] for label in self.labels}
        messagebox.showinfo("Reset", "All data has been reset.")

    def calculate(self):
        if not self.car_data['Model']:
            messagebox.showerror("No Data", "Please add at least one car.")
            return

        car_price, car_range, car_power, car_100, car_top_spd = self.main(self.car_data)
        cp_p, cr_p, cpp_p, c1_p, t_p = self.wight_inp()
        cp, cr, cpp, c1, t = self.calculate_input(cp_p, cr_p, cpp_p, c1_p, t_p, car_price, car_range, car_power, car_100, car_top_spd)
        qm, qx = self.shed(cp, cr, cpp, c1, t)
        bed = self.step4bad(qx, cp, cr, cpp, c1, t)
        good = self.step4good(qm, cp, cr, cpp, c1, t)
        fin = self.fin_num(good, bed)

        self.show_results(fin)

    def show_results(self, fin):
        result_window = tk.Toplevel(self.root)
        result_window.title("Car Comparison Results")
        result_text = tk.Text(result_window, height=20, width=50, bg="#f5f5f5", fg="#333333", font=("Helvetica", 12))
        result_text.pack(pady=10)

        # Add the calculated results, numbered
        for index, car in enumerate(fin, start=1):
            result_text.insert(tk.END, f"{index}. {car[0]}: {car[1]:.2f}\n")

    def main(self, data):
        car_price = {}
        car_range = {}
        car_power = {}
        car_100 = {}
        car_top_spd = {}

        prc_sum = sum(data['Price'])
        for car, coast in zip(data['Model'], data['Price']):
            car_price[car] = coast / (prc_sum * 2) * 0.5

        range_sum = sum(data['Range (miles)'])
        for car, range in zip(data['Model'], data['Range (miles)']):
            car_range[car] = range / (range_sum * 2) * 0.5

        power_sum = sum(data['Power'])
        for car, power in zip(data['Model'], data['Power']):
            car_power[car] = power / (power_sum * 2) * 0.5

        to_100_sum = sum(data['0-100 km/h (seconds)'])
        for car, c100 in zip(data['Model'], data['0-100 km/h (seconds)']):
            car_100[car] = c100 / (to_100_sum * 2) * 0.5

        top_speed_sum = sum(data['Top Speed (mph)'])
        for car, top_spd in zip(data['Model'], data['Top Speed (mph)']):
            car_top_spd[car] = top_spd / (top_speed_sum * 2) * 0.5

        return car_price, car_range, car_power, car_100, car_top_spd

    def wight_inp(self):
        while True:
            user = messagebox.askquestion("Weight Input", "If you want to change the percentage, click Yes. If not, click No.")
            if user == "no":
                return 20, 20, 20, 20, 20
            elif user == "yes":
                result = []
                total = 100
                while True:
                    ask = simpledialog.askfloat("Enter percentage", f"Enter percentage (Remaining: {total}%):")
                    if ask is None:
                        continue
                    if ask < 0 or ask > 100:
                        messagebox.showerror("Invalid Input", "Percentage must be between 0 and 100.")
                        continue
                    if sum(result) + ask > 100:
                        messagebox.showerror("Exceeded Percentage", "You have exceeded the total percentage. Please re-enter.")
                        total = 100
                        result = []
                        continue
                        
                    result.append(ask)
                    total -= ask
                    if len(result) == 5 and total == 0:
                        return tuple(result)

    def calculate_input(self, cp_p, cr_p, cpp_p, c1_p, t_p, car_price, car_range, car_power, car_100, car_top_spd):
        cp = {k: (v * cp_p) / 100 for k, v in car_price.items()}
        cr = {k: (v * cr_p) / 100 for k, v in car_range.items()}
        cpp = {k: (v * cpp_p) / 100 for k, v in car_power.items()}
        c1 = {k: (v * c1_p) / 100 for k, v in car_100.items()}
        t = {k: (v * t_p) / 100 for k, v in car_top_spd.items()}
        return cp, cr, cpp, c1, t

    def shed(self, cp, cr, cpp, c1, t):
        q_min = {
            "price": min(cp.values()),
            "range": min(cr.values()),
            "power": min(cpp.values()),
            "acceleration": min(c1.values()),
            "speed": min(t.values())
        }

        q_max = {
            "price": max(cp.values()),
            "range": max(cr.values()),
            "power": max(cpp.values()),
            "acceleration": max(c1.values()),
            "speed": max(t.values())
        }

        bed_result = {}
        good_res = {}

        us_price = "<" if simpledialog.askstring("Preference", "> price <") == "<" else ">"
        us_range = "<" if simpledialog.askstring("Preference", "> range <") == "<" else ">"
        us_power = "<" if simpledialog.askstring("Preference", "> power <") == "<" else ">"
        us_acceleration = "<" if simpledialog.askstring("Preference", "> acceleration <") == "<" else ">"
        us_speed = "<" if simpledialog.askstring("Preference", "> top_speed <") == "<" else ">"

        if us_price == "<":
            good_res["price"] = q_min["price"]
            bed_result["price"] = q_max["price"]
        elif us_price == ">":
            good_res["price"] = q_max["price"]
            bed_result["price"] = q_min["price"]

        if us_range == "<":
            good_res["range"] = q_min["range"]
            bed_result["range"] = q_max["range"]
        elif us_range == ">":
            good_res["range"] = q_max["range"]
            bed_result["range"] = q_min["range"]

        if us_power == "<":
            good_res["power"] = q_min["power"]
            bed_result["power"] = q_max["power"]
        elif us_power == ">":
            good_res["power"] = q_max["power"]
            bed_result["power"] = q_min["power"]

        if us_acceleration == "<":
            good_res["acceleration"] = q_min["acceleration"]
            bed_result["acceleration"] = q_max["acceleration"]
        elif us_acceleration == ">":
            good_res["acceleration"] = q_max["acceleration"]
            bed_result["acceleration"] = q_min["acceleration"]

        if us_speed == "<":
            good_res["speed"] = q_min["speed"]
            bed_result["speed"] = q_max["speed"]
        elif us_speed == ">":
            good_res["speed"] = q_max["speed"]
            bed_result["speed"] = q_min["speed"]

        return good_res, bed_result

    def step4bad(self, bed_result, car_price, car_range, car_power, car_100, car_top_spd):
        cars = {}
        for pr in car_price:
            all_sum = 0
            if car_price[pr] > bed_result["price"]:
                all_sum = ((car_price[pr] - bed_result["price"]) * 2)   
            else:
                all_sum = ((bed_result["price"] - car_price[pr]) * 2)

            if car_range[pr] > bed_result["range"]:
                all_sum += ((car_range[pr] - bed_result["range"]) * 2)
            else:
                all_sum += ((bed_result["range"] - car_range[pr]) * 2)

            if car_power[pr] > bed_result["power"]:
                all_sum += ((car_power[pr] - bed_result["power"]) * 2)
            else:
                all_sum += ((bed_result["power"] - car_power[pr]) * 2)

            if car_100[pr] > bed_result["acceleration"]:
                all_sum += ((car_100[pr] - bed_result["acceleration"]) * 2)
            else:
                all_sum += ((bed_result["acceleration"] - car_100[pr]) * 2)

            if car_top_spd[pr] > bed_result["speed"]:
                all_sum += ((car_top_spd[pr] - bed_result["speed"]) * 2)
            else:
                all_sum += ((bed_result["speed"] - car_top_spd[pr]) * 2)

            cars[pr] = all_sum * 0.5
        return cars

    def step4good(self, good_res, car_price, car_range, car_power, car_100, car_top_spd):
        cars = {}
        for pr in car_price:
            all_sum = 0
            if car_price[pr] > good_res["price"]:
                all_sum = ((car_price[pr] - good_res["price"]) * 2)
            else:
                all_sum = ((good_res["price"] - car_price[pr]) * 2)

            if car_range[pr] > good_res["range"]:
                all_sum += ((car_range[pr] - good_res["range"]) * 2)
            else:
                all_sum += ((good_res["range"] - car_range[pr]) * 2)

            if car_power[pr] > good_res["power"]:
                all_sum += ((car_power[pr] - good_res["power"]) * 2)
            else:
                all_sum += ((good_res["power"] - car_power[pr]) * 2)

            if car_100[pr] > good_res["acceleration"]:
                all_sum += ((car_100[pr] - good_res["acceleration"]) * 2)
            else:
                all_sum += ((good_res["acceleration"] - car_100[pr]) * 2)

            if car_top_spd[pr] > good_res["speed"]:
                all_sum += ((car_top_spd[pr] - good_res["speed"]) * 2)
            else:
                all_sum += ((good_res["speed"] - car_top_spd[pr]) * 2)

            cars[pr] = all_sum * 0.5
        return cars

    def fin_num(self, min_num, max_num):
        fin = {}
        for mi in min_num:
            fin_sum = max_num[mi] / (min_num[mi] + max_num[mi])
            fin[mi] = fin_sum
        sorted_values_desc = sorted(fin.items(), key=lambda x: x[1], reverse=True)
        return sorted_values_desc

if __name__ == "__main__":
    root = tk.Tk()
    app = CarApp(root)
    root.mainloop()
