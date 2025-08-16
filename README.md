# 💸 FinTrack - Personal Finance Tracker

**FinTrack is a personal finance management web application built with Flask.**
**It allows users to track income and expenses, manage categories, and visualize their financial data through interactive dashboards.** 
This project provides an **intuitive dashboard, modern UI, and seamless transaction management** to keep your finances organized.

---

## 🚀 Features

- ✅ Add, edit, and delete transactions (income & expenses)  
- ✅ Categorize transactions for better financial tracking  
- ✅ Clean **Bootstrap 5 UI** with responsive design  
- ✅ **Flash messages** for success/error notifications  
- ✅ **SQLite database** for lightweight storage  
- ✅ Easy-to-deploy **Flask project structure**  

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)  
- **Frontend:** HTML, Jinja2, Bootstrap 5  
- **Database:** SQLite (via SQLAlchemy ORM)  
- **Other Tools:** Flask-Login, Flask-Migrate  

---

### 📂 Project Structure
```
FinTrack/
│── app.py                     # Main Flask app entry point
│── config.py                  # App configurations (DB, secret key, etc.)
│── requirements.txt           # Python dependencies
│── models.py                  # Database models (User, Category, Transaction)
│── extensions.py              # Flask extensions (db, login_manager, migrate, etc.)
│
├── migrations/                # Auto-generated (when using Flask-Migrate)
│
├── routes/                    # Routes organized into Blueprints
│   │── __init__.py
│   │── auth.py                # Login, register, logout
│   │── transactions.py        # Add, edit, delete, list transactions
│   │── categories.py          # Manage categories
│   │── dashboard.py           # Dashboard, reports, charts
│
├── templates/                 # Jinja2 HTML templates
│   │── base.html              # Common layout (navbar, footer, bootstrap)
│   │── index.html             # Homepage / dashboard
│   │── login.html             # User login page
│   │── register.html          # User signup page
│   │── transactions.html      # Transactions list + add/edit form
│   │── categories.html        # Categories management
│   │── dashboard.html         # Income/expense summary view
│
├── static/                    # CSS, JS
│   ├── css/
│   │   └── styles.css         # Custom styles
│   ├── js/
│   │   └── scripts.js         # (Optional) Custom JS
│
└── README.md                  # Project documentation
```
---

## ⚙️ Installation & Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/finance-tracker.git
   cd finance-tracker
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
4. **Run the application**
   ```bash
   python app.py
5. **Open in browser**
   ```bash
   http://127.0.0.1:5000 #open this link

## 🔮 Future Improvements

📊 Add interactive graphs for income/expense trends

👤 Multi-user support with advanced authentication

☁️ Deploy on Heroku / Render / Railway

📱 Add mobile-friendly PWA support

## 🤝 Contributing

Contributions are always welcome! 🎉

 Fork the repository

1. **Create a new branch**
   ```bash
   git checkout -b feature-name
2. **Commit your changes**
   ```bash
   git commit -m "Added new feature"
3. **Push your branch**
   ```bash
   git push origin feature-name
  Open a Pull Request

Developed by **Gautham Ratiraju**

If you like this project, don’t forget to ⭐ it on GitHub!
