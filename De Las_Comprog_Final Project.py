import tkinter as tk
from tkinter import ttk  
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import threading
import time
from datetime import datetime
import pygame
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk, ImageEnhance


class DoseSyncApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DoseSync - Medication Manager")
        self.geometry("900x600")
        
        image_path = f"C:\\Users\\User\\Documents\\College Era\\Coding\\Codes\\Python\\Wallpaper.png"
        image = Image.open(image_path)
        image = image.resize((1152, 800), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Brightness(image)
        dark_image = enhancer.enhance(0.5)
        bg_image = ImageTk.PhotoImage(dark_image)
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_image
        self.configure(bg="#1e1e2e")
        
        self.data = {"medications": [], "users": {}}
        self.frames = {}

        # Correct instantiation of ttk.Style
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#000000", foreground="white", fieldbackground="#000000", font=("Arial", 12), rowheight=30)
        style.map("Custom.Treeview", background=[('selected', '#41b3a3')], foreground=[('selected', 'white')])

        # Here you would define your frames
        for F in (LoginScreen, CreateAccountScreen, HomeScreen, AddMedicationScreen, ViewMedicationsScreen,):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginScreen)

        threading.Thread(target=self.notification_checker, daemon=True).start()
        pygame.mixer.init()

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def notification_checker(self):
        while True:
            current_time = datetime.now().strftime("%I:%M %p")
            for med in self.data["medications"]:
                if med["time"] == current_time:
                    self.display_notification(med)
            time.sleep(60)

    def display_notification(self, medication):
        """Display a popup notification."""
        def go_back():
            notification_window.destroy()
            self.show_frame(HomeScreen)

        try:
            sound_path = r"C:\Users\i main raiden\Desktop\PYTHON FILE\DE LAS_PYTHON FINAL PROJECT\PYTHON WITHOUT DATABASE\notification_sound.mp3"
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(loops=0)
        except Exception as e:
            print(f"Error playing sound: {e}")

        notification_window = tk.Toplevel(self)
        notification_window.title("Medication Reminder")
        notification_window.geometry("480x360")
        notification_window.configure(bg="#1e1e2e")

        message = f"It's time to take {medication['medication']} - {medication['dose']}!"
        tk.Label(notification_window, text=message, font=("Arial", 14), fg="#ffffff", bg="#1e1e2e").pack(pady=20)

        back_button = tk.Button( notification_window, text="Back", command=go_back, bg="#41b3a3", fg="#ffffff", font=("Arial", 12), relief="flat", padx=20, pady=10)
        back_button.pack(pady=20)

class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#1e1e2e")
        tk.Label(self, text="Login to DoseSync", font=("Arial", 28, "bold"),
         bg="#1e1e2e", fg="#ffffff").pack(pady=40)
        form_frame = tk.Frame(self, bg="#1e1e2e")
        form_frame.pack(pady=20)
        self.username = self.create_form_row(form_frame, "Username:", 0)
        self.password = self.create_form_row(form_frame, "Password:", 1, show="*")
        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack(pady=20)

        login_btn = tk.Button(
            btn_frame, text="Login", bg="#41b3a3", fg="#ffffff", font=("Arial", 14), relief="flat", padx=20, pady=10, command=self.login_user,)
        login_btn.grid(row=0, column=0, padx=10)

        create_account_btn = tk.Button(btn_frame, text="Create Account", bg="#41b3a3", fg="#ffffff", font=("Arial", 14), relief="flat", padx=20, pady=10, command=lambda: master.show_frame(CreateAccountScreen),)
        create_account_btn.grid(row=0, column=1, padx=10)

    def create_form_row(self, parent, label_text, row, show=None):
        tk.Label(parent, text=label_text, font=("Arial", 14), bg="#1e1e2e", fg="#ffffff").grid(row=row, column=0, sticky="w", padx=10, pady=10)
        entry = tk.Entry(parent, font=("Arial", 14), bg="#333333", fg="#ffffff", relief="flat", insertbackground="#ffffff", show=show)
        entry.grid(row=row, column=1, padx=10, pady=10)
        return entry

    def login_user(self):
        username = self.username.get()
        password = self.password.get()

        if validate_login(username, password):
            messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
            self.master.show_frame(HomeScreen)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

class CreateAccountScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#1e1e2e")
        tk.Label(self, text="Create a New Account", font=("Arial", 28, "bold"), bg="#1e1e2e", fg="#ffffff").pack(pady=40)
        form_frame = tk.Frame(self, bg="#1e1e2e")
        form_frame.pack(pady=20)
        self.new_username = self.create_form_row(form_frame, "New Username:", 0)
        self.new_password = self.create_form_row(form_frame, "New Password:", 1, show="*")

        create_btn = tk.Button(self, text="Create Account", bg="#41b3a3", fg="#ffffff", font=("Arial", 14), relief="flat", padx=20, pady=10, command=self.create_account,)
        create_btn.pack(pady=20)

        back_btn = tk.Button(self, text="Back to Login", bg="#999999", fg="#ffffff", font=("Arial", 12), relief="flat", padx=10, pady=5, command=lambda: master.show_frame(LoginScreen),)
        back_btn.pack(pady=10)

    def create_form_row(self, parent, label_text, row, show=None):
        tk.Label(parent, text=label_text, font=("Arial", 14), bg="#1e1e2e", fg="#ffffff").grid(row=row, column=0, sticky="w", padx=10, pady=10)
        entry = tk.Entry(parent, font=("Arial", 14), bg="#333333", fg="#ffffff", relief="flat", insertbackground="#ffffff", show=show)
        entry.grid(row=row, column=1, padx=10, pady=10)
        return entry

    def create_account(self):
        username = self.new_username.get()
        password = self.new_password.get()

        if register_user(username, password):
            messagebox.showinfo("Account Created", "Your account has been created successfully!")
            self.master.show_frame(LoginScreen)
        else:
            messagebox.showerror("Error", "Username already exists. Please try again.")

def validate_login(username, password):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dosesync"
        )
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM users WHERE username = %s AND password = %s""", (username, password))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result is not None
    except Error as e:
        print(f"Error while validating login: {e}")
        return False

def register_user(username, password):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dosesync"
        )
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM users WHERE username = %s""", (username,))
        result = cursor.fetchone()

        if result:
            return False

        cursor.execute("""INSERT INTO users (username, password) VALUES (%s, %s)""", (username, password))
        db.commit()
        cursor.close()
        db.close()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    
class AddMedicationScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#1a1b26") 

        label = tk.Label(self, text="Add Medication", bg="#1a1b26", fg="#ffffff", font=("Arial", 28, "bold"))
        label.pack(pady=20)
        form_frame = tk.Frame(self, bg="#1a1b26")
        form_frame.pack(pady=10)
        self.add_form_row(form_frame, "Medication Name:", 0)
        self.add_form_row(form_frame, "Dose:", 1)
        self.add_form_row(form_frame, "Time (hh:mm AM/PM):", 2)
        button_frame = tk.Frame(self, bg="#1a1b26")
        button_frame.pack(pady=20)
  
        add_btn = tk.Button(button_frame, text="Add Medication", bg="#41b3a3", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat", padx=15, pady=5, command=self.add_medication)
        add_btn.pack(side="top", pady=5)

        back_btn = tk.Button(button_frame, text="Back", bg="#41b3a3", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat", padx=15, pady=5, command=lambda: parent.show_frame(HomeScreen),)
        back_btn.pack(side="top", pady=5)

    def add_form_row(self, parent, label_text, row):
        """Helper to add a form row with aligned label and textbox."""
        label = tk.Label( parent, text=label_text, font=("Arial", 12, "bold"), bg="#1a1b26", fg="#ffffff")
        label.grid(row=row, column=0, sticky="e", padx=10, pady=5)

        entry = tk.Entry(parent, font=("Arial", 12), bg="#333333",   fg="#ffffff",   insertbackground="#ffffff",  relief="flat", width=25)
        entry.grid(row=row, column=1, padx=10, pady=5)

        if label_text == "Medication Name:":
            self.medication_name = entry
        elif label_text == "Dose:":
            self.dose = entry
        elif label_text == "Time (hh:mm AM/PM):":
            self.time = entry

    def add_medication(self):
        """Adds medication to the global data."""
        medication = self.medication_name.get()
        dose = self.dose.get()
        time = self.time.get()

        if medication and dose and time:
            self.master.data["medications"].append({
                "medication": medication, "dose": dose, "time": time})
            messagebox.showinfo("Medication Added", "The medication has been added successfully!")
            self.master.frames[ViewMedicationsScreen].update_medications()
            self.master.show_frame(HomeScreen)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

class ViewMedicationsScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#1e1e2e")  # Set background of the screen
        style = ttk.Style(self)
        style.theme_use("clam")  # Use "clam" theme
        style.configure("Custom.Treeview",
                        background="#000000",  
                        foreground="white",     
                        fieldbackground="#000000",  
                        font=("Arial", 12),
                        rowheight=30)

        style.map("Custom.Treeview",
        background=[('selected', '#41b3a3')],  # Accent color for selected row
        foreground=[('selected', 'white')])

        self.tree = ttk.Treeview(self, style="Custom.Treeview")
        self.tree["columns"] = ("Medication", "Dose", "Time")  # Only three columns
        self.tree.column("Medication", anchor=tk.W, width=200)
        self.tree.column("Dose", anchor=tk.W, width=100)
        self.tree.column("Time", anchor=tk.W, width=150)
        self.tree.heading("Medication", text="Medication", anchor=tk.W)
        self.tree.heading("Dose", text="Dose", anchor=tk.W)
        self.tree.heading("Time", text="Time", anchor=tk.W)
        self.tree.pack(pady=20)

        back_btn = tk.Button(self, text="Back", bg="#999999", fg="#ffffff", font=("Arial", 12), relief="flat", padx=10, pady=5, command=lambda: parent.show_frame(HomeScreen))
        back_btn.pack(pady=20)

        self.delete_btn = tk.Button(self, text="Delete Medication", bg="#e63946", fg="#ffffff", font=("Arial", 12), relief="flat", padx=10, pady=5, command=self.delete_medication,)
        self.delete_btn.pack(pady=20)
    def fetch_medications_from_db(self):
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="",  # Replace with your MySQL password
                database="dosesync"  # Replace with your database name
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT medication, dose, time FROM medications")
            rows = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)
            for row in rows:
                self.tree.insert("", "end", values=(row['medication'], row['dose'], row['time']))
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def update_medications(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for med in self.master.data["medications"]:
            # Only insert the medication, dose, and time
            self.tree.insert("", "end", values=(med['medication'], med['dose'], med['time']))

    def delete_medication(self):
        selected_item = self.tree.selection()

        if selected_item:
            selected_medication = self.tree.item(selected_item, "values")

            confirm = messagebox.askyesno(
                "Delete Medication",
                f"Are you sure you want to delete this medication?"
            )
            if confirm:
                self.master.data["medications"] = [
                    med for med in self.master.data["medications"] 
                    if med['medication'] != selected_medication[0] 
                ]
                self.tree.delete(selected_item)
                messagebox.showinfo("Deleted", "Medication successfully deleted.")
        else:
            messagebox.showwarning("No Selection", "Please select a medication to delete.")
            
class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#1e1e2e")
        tk.Label(self, text="Welcome to DoseSync", font=("Arial", 28, "bold"), bg="#1e1e2e", fg="#ffffff").pack(pady=40)

        add_medication_btn = tk.Button(self, text="Add Medication", bg="#41b3a3", fg="#ffffff", font=("Arial", 14), relief="flat", padx=20, pady=10, command=lambda: master.show_frame(AddMedicationScreen))
        add_medication_btn.pack(pady=20)

        view_medication_btn = tk.Button(self, text="View Medications", bg="#41b3a3", fg="#ffffff", font=("Arial", 14), relief="flat", padx=20, pady=10, command=lambda: master.show_frame(ViewMedicationsScreen))
        view_medication_btn.pack(pady=20)

        exit_btn = tk.Button(self, text="Exit", bg="#ed4319", fg="#ffffff", font=("Arial", 14), relief="flat", padx=20, pady=10, command=self.on_exit)
        exit_btn.pack(pady=20)

    def on_exit(self):
        response = msgbox.askyesno("Confirm Exit", "Are you sure you want to exit?")
        if response:
            self.quit()
if __name__ == "__main__":
    app = DoseSyncApp()
    app.mainloop()
