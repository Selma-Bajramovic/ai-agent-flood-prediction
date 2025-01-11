from tkinter import ttk
import requests
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

def send_data():
    try:
        city = city_entry.get()
        days = int(days_entry.get())
        
        if not city or not days:
            messagebox.showerror("Error", "Molimo unesite sve podatke.")
            return
        
        data = {
            "city": city,
            "days": days
        }

        response = requests.post("http://127.0.0.1:5000/predict_flood", json=data)
        
        if response.status_code == 200:
            predictions = response.json()
            print(f"API Response: {predictions}")

            for row in table.get_children():
                table.delete(row)

            today = datetime.today()

            for prediction in predictions:
                day_value = prediction['day']
                try:
                    date_obj = today + timedelta(days=day_value)
                    formatted_date = date_obj.strftime('%d.%m.%Y.')
                except ValueError:
                    formatted_date = str(day_value)

                table.insert('', 'end', values=(formatted_date, prediction['predicted_flood_risk'], 
                                                prediction['precip'], prediction['humidity'], prediction['precipprob']))

        else:
            messagebox.showerror("Error", "Greška pri dohvatu podataka.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Greška: {str(e)}")

root = tk.Tk()
root.title("Flood Prediction")

style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", font=("Arial", 14), foreground="#2f4f4f", background="#f0f8ff")
style.configure("TEntry", font=("Arial", 14), foreground="#2f4f4f", padding=5, relief="solid")
style.configure("TButton", background="#6c8ea1", foreground="white", font=("Arial", 14, "bold"))
style.map("TButton", background=[("active", "#4a6b7d")])

city_label = ttk.Label(root, text="Grad:")
city_label.grid(row=0, column=0, padx=10, pady=10)
city_entry = ttk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=10)

days_label = ttk.Label(root, text="Broj dana:")
days_label.grid(row=1, column=0, padx=10, pady=10)
days_entry = ttk.Entry(root)
days_entry.grid(row=1, column=1, padx=10, pady=10)

predict_button = ttk.Button(root, text="Predvidi Poplavu", command=send_data)
predict_button.grid(row=2, columnspan=2, pady=20)

table = ttk.Treeview(root, columns=("Date", "Risk", "Precip", "Humidity", "Precip Prob"), show="headings", style="Treeview")
table.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

table.heading("Date", text="Datum")
table.heading("Risk", text="Rizik")
table.heading("Precip", text="Padavine (mm)")
table.heading("Humidity", text="Vlaga (%)")
table.heading("Precip Prob", text="Vjerojatnost padavina (%)")

style.configure("Treeview", font=("Arial", 12), rowheight=30, fieldbackground="#f0f8ff", height=10)
style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#6c8ea1", foreground="white")

table.column("Date", anchor="w", width=200)
table.column("Risk", anchor="center", width=150)
table.column("Precip", anchor="center", width=150)
table.column("Humidity", anchor="center", width=150)
table.column("Precip Prob", anchor="center", width=200)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
scrollbar.grid(row=3, column=3, sticky="ns", padx=10)
table.configure(yscrollcommand=scrollbar.set)

root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
