# 📧 Bulk Email Sender (with HTML Templates, Placeholders & Attachments)

A Python-based GUI application for sending personalized bulk emails using **CSV data**, **HTML templates**, and **file attachments**.
Built using **Tkinter**, **pandas**, and **smtplib**.

---

## 🚀 Features

### ✔️ **Simple GUI Interface**

No command-line hassle — everything is done through an easy-to-use Tkinter window.

### ✔️ **CSV-Based Personalization**

Load a CSV file where each row is one recipient.
Use CSV columns to auto-fill placeholders inside your HTML template.

### ✔️ **Dynamic HTML Placeholders**

Define placeholders like:

```
{name}
{course}
{date}
```

And map them to CSV columns using the GUI.

### ✔️ **File Attachments**

Attach multiple files (PDF, images, docs, etc.) that will be sent with every email.

### ✔️ **Gmail App Password Support**

Secure login using **Gmail App Passwords** (recommended).

### ✔️ **Status Reporting**

Displays success/failure logs for each email in the terminal.

---

## 🛠️ Tech Stack

* **Python 3**
* **Tkinter** – GUI
* **pandas** – CSV handling
* **smtplib** – SMTP email sending
* **email.mime** – HTML email formatting

---
## 📦 Installation

### 1️⃣ Clone the repo

```bash
git clone https://github.com/yourusername/email-sender-gui.git
cd email-sender-gui
```

### 2️⃣ Install dependencies

```bash
pip install pandas
```

*(Tkinter is included with Python. No separate install needed.)*

---

## ▶️ Usage

Run the program:

```bash
python main.py
```

### 📝 Fill the required fields in the GUI:

1. **Your Email** – Example: `yourname@gmail.com`
2. **App Password** – Get it from Google Account → Security → App Passwords
3. **Email Subject**
4. **CSV File** – Contains recipient data
5. **HTML Template** – Contains placeholders like `{name}`
6. **Attachments** (optional)
7. **Set Placeholders** – Map `{name}` → `Full_Name`
8. Click **Send Emails**

---

## 📄 CSV Format Example

| Email                                     | name   | course |
| ----------------------------------------- | ------ | ------ |
| [test1@gmail.com](mailto:test1@gmail.com) | Rahul  | AI     |
| [test2@gmail.com](mailto:test2@gmail.com) | Ananya | ML     |

---

## 🧩 HTML Template Example

```html
<html>
<body>
    <h2>Hello {name},</h2>
    <p>Thank you for registering for the {course} workshop!</p>
</body>
</html>
```

---

## 🔧 Project Structure

```
email-sender/
│
├── main.py              # GUI + email logic
├── template.html        # Example email template
├── recipients.csv       # Example CSV
├── README.md            # Project documentation
└── attachments/         # Optional attachment files
```

---

## 🛡️ Gmail App Password Note

Google no longer allows direct password login for SMTP.
You **must** create an **App Password**:

1. Google Account → **Security**
2. Enable **2-Step Verification**
3. Go to **App Passwords**
4. Create new
5. Use the generated key inside the app

---

## ❗ Troubleshooting

### ❌ Error: "SMTPAuthenticationError"

* Ensure you are using **App Password**, NOT Google login password.

### ❌ CSV column not found

* Check for spelling mistakes in column names.

### ❌ HTML placeholders not replaced

* Make sure you removed braces when defining placeholders
  Example: Placeholder: `name` → maps to column `name`.

---

## 🤝 Contributing

Pull requests are welcome!
If you want improvements (logging window, progress bar, CC/BCC support, etc.), feel free to propose.

---

## ⭐ If you like this project…

Consider giving it a **Star** ⭐ on GitHub!
