import tkinter as tk
from tkinter import messagebox, scrolledtext
import time

class ParkingSystem:
    def __init__(self):
        """Initialize parking lots, car records, and rates"""
        self.parking_lots = {1: {"Location": "Main Gate", "Capacity": 5, "Available": 5},
                             2: {"Location": "Mall Entrance", "Capacity": 5, "Available": 5}}
        self.parking_records = {}  # Stores {Car_Number: {Entry_Time, Exit_Time, Parking_Lot_ID, Fee}}
        self.car_info = {}  # Stores {Car_Number: {Owner_Name, Car_Model, Phone_Number}}
        self.parking_rate = 5  # Fee per minute

    def add_car_entry(self, car_number, owner_name, car_model, phone_number, lot_id):
        """Register car entry if space is available"""
        if self.parking_lots[lot_id]["Available"] > 0:
            self.car_info[car_number] = {"Owner_Name": owner_name, "Car_Model": car_model, "Phone_Number": phone_number}
            self.parking_records[car_number] = {"Entry_Time": time.time(), "Parking_Lot_ID": lot_id, "Exit_Time": None, "Fee": 0}
            self.parking_lots[lot_id]["Available"] -= 1
            return f"Car {car_number} entered parking lot {lot_id}."
        return "No available slots in this parking lot."

    def add_car_exit(self, car_number):
        """Register car exit, calculate fee, and update lot availability"""
        if car_number in self.parking_records and self.parking_records[car_number]["Exit_Time"] is None:
            exit_time = time.time()
            entry_time = self.parking_records[car_number]["Entry_Time"]
            duration = (exit_time - entry_time) / 60  # Convert to minutes
            fee = round(duration * self.parking_rate, 2)
            lot_id = self.parking_records[car_number]["Parking_Lot_ID"]

            self.parking_records[car_number]["Exit_Time"] = exit_time
            self.parking_records[car_number]["Fee"] = fee
            self.parking_lots[lot_id]["Available"] += 1

            return f"Car {car_number} exited. Fee: ${fee}"
        return "Car not found or already exited."

    def get_parking_status(self):
        """Return current parking lot availability"""
        status = ""
        for lot_id, details in self.parking_lots.items():
            status += f"Lot {lot_id}: {details['Available']} / {details['Capacity']} Available at {details['Location']}\n"
        return status

    def get_all_car_info(self):
        """Return all registered car information"""
        info = ""
        for car_number, details in self.car_info.items():
            info += f"Car Number: {car_number}\n"
            info += f"Owner Name: {details['Owner_Name']}\n"
            info += f"Car Model: {details['Car_Model']}\n"
            info += f"Phone Number: {details['Phone_Number']}\n"
            info += f"Parking Lot ID: {self.parking_records[car_number]['Parking_Lot_ID']}\n"
            info += f"Entry Time: {time.ctime(self.parking_records[car_number]['Entry_Time'])}\n"
            if self.parking_records[car_number]['Exit_Time']:
                info += f"Exit Time: {time.ctime(self.parking_records[car_number]['Exit_Time'])}\n"
                info += f"Fee: ${self.parking_records[car_number]['Fee']}\n"
            info += "\n"
        return info

# Initialize Parking System
parking = ParkingSystem()

# GUI Functions
def register_entry():
    car_num = entry_car_number.get()
    owner = entry_owner.get()
    model = entry_model.get()
    phone = entry_phone.get()
    lot_id = int(entry_lot.get())

    if car_num and owner and model and phone:
        msg = parking.add_car_entry(car_num, owner, model, phone, lot_id)
        messagebox.showinfo("Car Entry", msg)
        update_parking_status()
        clear_entry_fields()
    else:
        messagebox.showerror("Error", "Please fill all fields.")

def register_exit():
    car_num = entry_exit_car.get()
    if car_num:
        msg = parking.add_car_exit(car_num)
        messagebox.showinfo("Car Exit", msg)
        update_parking_status()
        entry_exit_car.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Enter a valid Car Number.")

def update_parking_status():
    status_label.config(text=parking.get_parking_status())

def clear_entry_fields():
    entry_car_number.delete(0, tk.END)
    entry_owner.delete(0, tk.END)
    entry_model.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_lot.delete(0, tk.END)

def show_all_car_info():
    info = parking.get_all_car_info()
    info_window = tk.Toplevel(root)
    info_window.title("Registered Cars Information")
    info_window.geometry("400x400")
    text_area = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, width=50, height=20)
    text_area.insert(tk.INSERT, info)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("Car Parking Management System")
root.geometry("500x600")

tk.Label(root, text="Car Parking Management", font=("Arial", 16, "bold")).pack(pady=10)

# Parking Lot Status
status_label = tk.Label(root, text=parking.get_parking_status(), font=("Arial", 12), fg="blue")
status_label.pack(pady=10)

# Entry Section
tk.Label(root, text="Register Car Entry", font=("Arial", 14, "bold")).pack(pady=5)
tk.Label(root, text="Car Number:").pack()
entry_car_number = tk.Entry(root)
entry_car_number.pack()

tk.Label(root, text="Owner Name:").pack()
entry_owner = tk.Entry(root)
entry_owner.pack()

tk.Label(root, text="Car Model:").pack()
entry_model = tk.Entry(root)
entry_model.pack()

tk.Label(root, text="Phone Number:").pack()
entry_phone = tk.Entry(root)
entry_phone.pack()

tk.Label(root, text="Parking Lot ID (1 or 2):").pack()
entry_lot = tk.Entry(root)
entry_lot.pack()

tk.Button(root, text="Register Entry", command=register_entry, bg="lightgreen").pack(pady=5)

# Exit Section
tk.Label(root, text="Register Car Exit", font=("Arial", 14, "bold")).pack(pady=5)
tk.Label(root, text="Car Number:").pack()
entry_exit_car = tk.Entry(root)
entry_exit_car.pack()

tk.Button(root, text="Register Exit", command=register_exit, bg="orange").pack(pady=5)

# Show All Registered Cars
tk.Button(root, text="Show All Registered Cars", command=show_all_car_info, bg="lightblue").pack(pady=10)

# Start GUI
update_parking_status()
root.mainloop()