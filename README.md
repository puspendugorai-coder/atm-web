# 🏧 Global Digital ATM Web App

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Web_App-lightgrey)
![Supabase](https://img.shields.io/badge/Database-Supabase-green)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

## 🔗 Live Demo
## 👉 [Click Here to Open the ATM](https://alphacoder7206-atm-web.hf.space)

---

## ✨ Features
- 💳 Card number verification from database
- 🔐 4-digit PIN authentication with lockout after 3 wrong attempts
- 💸 Withdraw money from account
- 💰 Deposit money to account
- 📊 Check account balance
- ⌨️ Full keyboard shortcuts — W, D, B, E keys
- 🔒 60-second security lockout with live countdown
- 🔗 Connected to same database as Bank Management System

---

## 🛠️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python Flask |
| Database | Supabase (PostgreSQL) |
| Hosting | Hugging Face Spaces (Docker) |

---

## 📁 Project Structure
```
atm_web/
├── app.py              ← Flask backend & ATM logic
├── requirements.txt    ← Python dependencies
├── Dockerfile          ← Container for deployment
└── templates/
    └── atm.html        ← Full ATM interface
```

---

## ⌨️ Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `W` | Withdraw |
| `D` | Deposit |
| `B` | Balance |
| `E` or `Esc` | Exit |
| `Enter` | Confirm any input |
| `Esc` | Go back |

---

## 🔗 Related Project
This ATM is connected to the **Bank Management System**:
- 👉 [Bank Management Web App](https://github.com/puspendugorai-coder/bank-management-web)
- 👉 [Bank Management Live](https://alphacoder7206-bank-management.hf.space)

---

## 🚀 Run Locally
```bash
git clone https://github.com/puspendugorai-coder/atm-web.git
cd atm-web
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

---

## 👨‍💻 Developer
**Puspendu Gorai**
- GitHub: [puspendugorai-coder](https://github.com/puspendugorai-coder)
- Live ATM: [Global Digital ATM](https://alphacoder7206-atm-web.hf.space)
- Bank App: [Bank Management](https://alphacoder7206-bank-management.hf.space)
