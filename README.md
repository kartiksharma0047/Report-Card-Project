# 📚 Report Card Django

Report Card Django is an open-source Django web application for generating student report cards as downloadable PDFs with advanced features.

## 🚀 Features

✅ Email integration (Gmail SMTP)  
✅ PDF report card generation with xhtml2pdf  
✅ Clean and user-friendly HTML templates  
✅ Advanced Django ORM queries  
✅ Django URL routing and views structure  
✅ Environment variables with python-decouple  
✅ Whitenoise for serving static files in production  
✅ Ready for deployment on Render or any cloud server  

## 🛠️ Tech Stack

- Backend: Django 3.2+
- PDF Generation: xhtml2pdf
- Email: Gmail SMTP integration
- Env Variables: python-decouple
- Static Files: Whitenoise
- Production Server: Gunicorn

## 📦 Project Structure

```plaintext
REPORT_CARD_DJANGO/
├── core/           # Django project folder
│   ├── core/       # Settings, URLs, WSGI
│   ├── Report/     # Custom Django app
│   ├── Student_Result_pdfs/ # Generated PDFs
│   ├── manage.py
│   ├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
```

## ⚡ Getting Started

### 📂 1️⃣ Clone the Repository
git clone :- https://github.com/kartiksharma0047/Report-Card-Project  
cd report-card-django/core

### 🐍 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
```

### 👉 For Windows
```bash
venv\Scripts\activate
```

### 👉 For Linux/Mac
```bash
source venv/bin/activate
```

### 📦 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔑 4️⃣ Add .env file
```plaintext
Inside core/ directory, create a .env file with:
---------------------------------------------
EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SECRET_KEY=your_secret_key
---------------------------------------------
```

### 📜 5️⃣ Run Migrations
```bash
python manage.py migrate
```

### ▶️ 6️⃣ Run the Project Locally
```bash
python manage.py runserver
```

### 📍 The app will be live at:
```bash
http://127.0.0.1:8000
```
