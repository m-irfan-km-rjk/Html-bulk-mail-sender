import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# --- Email sending function ---
def send_email(data, smtp_server, smtp_port, sender_email, app_password, html_content, attachments, placeholders, subject):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = data['Email']
        msg["Subject"] = subject

        # Replace placeholders dynamically
        personalized_html = html_content
        for key, column_name in placeholders.items():
            if column_name in data:
                personalized_html = personalized_html.replace(f"{{{key}}}", str(data[column_name]))
            else:
                personalized_html = personalized_html.replace(f"{{{key}}}", "")

        msg.attach(MIMEText(personalized_html, "html"))

        # Attach files
        for file_path in attachments:
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    file_attachment = MIMEApplication(f.read())
                    file_attachment.add_header(
                        "Content-Disposition",
                        f"attachment; filename={os.path.basename(file_path)}"
                    )
                    msg.attach(file_attachment)

        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {data['Email']}")
    except Exception as e:
        print(f"Failed to send email to {data['Email']}. Error: {e}")


# --- GUI ---
class EmailGUI:
    def __init__(self, master):
        self.master = master
        master.title("Email Sender")

        # Email and password
        tk.Label(master, text="Your Email:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = tk.Entry(master, width=40)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="App Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.pass_entry = tk.Entry(master, width=40, show="*")
        self.pass_entry.grid(row=1, column=1, padx=5, pady=5)

        # Subject
        tk.Label(master, text="Email Subject:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.subject_entry = tk.Entry(master, width=40)
        self.subject_entry.grid(row=2, column=1, padx=5, pady=5)

        # CSV file
        tk.Label(master, text="CSV File:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.csv_entry = tk.Entry(master, width=40)
        self.csv_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_csv).grid(row=3, column=2, padx=5, pady=5)

        # HTML template
        tk.Label(master, text="HTML Template:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.html_entry = tk.Entry(master, width=40)
        self.html_entry.grid(row=4, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_html).grid(row=4, column=2, padx=5, pady=5)

        # Attachments
        tk.Label(master, text="Attachments:").grid(row=5, column=0, sticky="ne", padx=5, pady=5)
        self.attachments_list = tk.Listbox(master, width=40, height=5)
        self.attachments_list.grid(row=5, column=1, padx=5, pady=5)
        tk.Button(master, text="Add File", command=self.add_attachment).grid(row=5, column=2, padx=5, pady=5)

        # Placeholders control buttons
        placeholder_frame = tk.Frame(master)
        placeholder_frame.grid(row=6, column=1, pady=10)

        tk.Button(placeholder_frame, text="Set Placeholders", command=self.set_placeholders).grid(row=0, column=0, padx=5)
        tk.Button(placeholder_frame, text="Show Placeholders", command=self.show_placeholders).grid(row=0, column=1, padx=5)
        tk.Button(placeholder_frame, text="Reset Placeholders", command=self.reset_placeholders).grid(row=0, column=2, padx=5)

        # Send button
        tk.Button(master, text="Send Emails", command=self.send_emails).grid(row=7, column=1, pady=10)

        # Placeholder dictionary
        self.placeholders = {}

    def browse_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_entry.delete(0, tk.END)
            self.csv_entry.insert(0, file_path)

    def browse_html(self):
        file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
        if file_path:
            self.html_entry.delete(0, tk.END)
            self.html_entry.insert(0, file_path)

    def add_attachment(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.attachments_list.insert(tk.END, file_path)

    def set_placeholders(self):
        csv_file = self.csv_entry.get()
        if not csv_file or not os.path.exists(csv_file):
            messagebox.showerror("Error", "Please select a valid CSV file first.")
            return

        df = pd.read_csv(csv_file)
        self.placeholders = {}

        while True:
            placeholder = simpledialog.askstring("Placeholder", "Enter placeholder in HTML (without braces), e.g., 'name':")
            if not placeholder:
                break
            column = simpledialog.askstring("CSV Column", f"Which CSV column should replace {{{placeholder}}}?")
            if column not in df.columns:
                messagebox.showerror("Error", f"Column '{column}' not found in CSV.")
            else:
                self.placeholders[placeholder] = column

        messagebox.showinfo("Success", f"{len(self.placeholders)} placeholders set successfully!")

    def show_placeholders(self):
        """Displays current placeholder mappings in a popup window"""
        if not self.placeholders:
            messagebox.showinfo("Placeholders", "No placeholders set.")
            return

        top = tk.Toplevel(self.master)
        top.title("Current Placeholders")

        tk.Label(top, text="HTML Placeholder → CSV Column", font=("Arial", 10, "bold")).pack(pady=5)

        text_box = tk.Text(top, width=50, height=10, wrap="word")
        text_box.pack(padx=10, pady=5)
        text_box.insert(tk.END, "\n".join([f"{{{ph}}} → {col}" for ph, col in self.placeholders.items()]))
        text_box.config(state="disabled")

        tk.Button(top, text="Close", command=top.destroy).pack(pady=5)

    def reset_placeholders(self):
        """Clears all saved placeholders"""
        if not self.placeholders:
            messagebox.showinfo("Info", "No placeholders to reset.")
            return

        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to clear all placeholders?")
        if confirm:
            self.placeholders.clear()
            messagebox.showinfo("Reset", "All placeholders have been cleared.")

    def send_emails(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        csv_file = self.csv_entry.get()
        html_file = self.html_entry.get()
        subject = self.subject_entry.get()
        attachments = list(self.attachments_list.get(0, tk.END))

        if not all([email, password, csv_file, html_file, subject]):
            messagebox.showerror("Error", "Please fill all fields and select files.")
            return

        try:
            items = pd.read_csv(csv_file).to_dict(orient='records')
            with open(html_file, "r") as f:
                html_content = f.read()

            for data in items:
                send_email(data, "smtp.gmail.com", 587, email, password, html_content, attachments, self.placeholders, subject)
            
            messagebox.showinfo("Success", "All emails sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send emails: {e}")


# --- Run GUI ---
root = tk.Tk()
app = EmailGUI(root)
root.mainloop()