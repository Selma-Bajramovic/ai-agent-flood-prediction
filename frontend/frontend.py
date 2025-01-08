import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime, timedelta

def send_data():
    city = city_var.get()
    try:
        days = int(days_entry.get())
    except ValueError:
        messagebox.showerror("Upozorenje", "Molimo unesite validan broj.")
        return

    if not city:
        messagebox.showerror("Upozorenje", "Molimo odaberite grad.")
        return

    if days < 1 or days > 10:
        messagebox.showwarning("Upozorenje", "Predikcije se mogu obavljati za narednih 10 dana. Molimo unesite broj između 1 i 10, te pokušajte ponovo.")
        days_entry.delete(0, tk.END)
        return

    data = {
        "city": city,
        "days": days
    }

    try:
        response = requests.post("http://127.0.0.1:5000/predict_flood", json=data)
        if response.status_code == 200:
            predictions = response.json()
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

                risk_level = prediction['risk_level']
                actual_precip = float(prediction['actual_precip'])
                predicted_precip = float(prediction['predicted_precip'])

                difference = "{:.2f}".format(prediction['difference'])

                table.insert("", "end", values=(
                    formatted_date,
                    predicted_precip,
                    actual_precip,
                    difference,
                    risk_level
                ))
        else:
            messagebox.showerror("Greška", "Došlo je do greške prilikom dobavljanja podataka.")
    except Exception as e:
        messagebox.showerror("Greška", f"Došlo je do greške: {str(e)}")

root = tk.Tk()
root.title("Predikcija rizika od poplave")
root.geometry("1000x600")
root.configure(bg="#f3cea9") 

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#ed987c", foreground="#8B4513", font=("Arial", 14, "bold"))
style.configure("TLabel", background="#f3cea9", font=("Arial", 12), foreground="#8B4513")
style.configure("TEntry", font=("Arial", 12), foreground="#8B4513")  
style.configure("Treeview", font=("Arial", 12), rowheight=30, fieldbackground="#f3cea9", height=20)
style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#ed987c", foreground="#8B4513")
style.map("TButton", background=[("active", "#ed8f7c")])

tk.Label(root, text="Izaberite grad za koji želite predikciju:", bg="#f3cea9", font=("Arial", 16), fg="#8B4513").pack(padx=10, pady=5)

city_var = tk.StringVar()
city_menu = ttk.Combobox(root, textvariable=city_var, values=["Mostar", "Jablanica", "Fojnica"], font=("Arial", 12))
city_menu.set("Mostar")
city_menu.pack(padx=10, pady=5)

tk.Label(root, text="Unesite broj dana (1 - 10):", bg="#f3cea9", font=("Arial", 16), fg="#8B4513").pack(padx=10, pady=5)

days_entry = ttk.Entry(root, font=("Arial", 12))
days_entry.pack(padx=10, pady=5)

predict_button = ttk.Button(root, text="Predvidi rizik od poplave", command=send_data)
predict_button.pack(padx=10, pady=20)

table_frame = tk.Frame(root, bg="#edb47c") 
table_frame.pack(padx=10, pady=10, fill="both", expand=True)

columns = ("day", "predicted_precip", "actual_precip", "difference", "risk_level")
table = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")
table.heading("day", text="Dan")
table.heading("predicted_precip", text="Predviđeni padavine (mm)")
table.heading("actual_precip", text="Stvarne padavine (mm)")
table.heading("difference", text="Razlika")
table.heading("risk_level", text="Rizik od poplave")

table.column("day", anchor="center", width=90, minwidth=80)
table.column("predicted_precip", anchor="center", width=150, minwidth=150)
table.column("actual_precip", anchor="center", width=150, minwidth=150)
table.column("difference", anchor="center", width=150, minwidth=150)
table.column("risk_level", anchor="center", width=200, minwidth=200)

table.pack(fill="both", expand=True)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)

root.mainloop()