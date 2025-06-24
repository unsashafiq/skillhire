# SkillHire – Connecting Skilled Workers to Employers

**SkillHire** is a Django-based web platform developed as a final year project. It bridges the gap between skilled job seekers and employers, providing a smooth experience for workers to showcase their skills and for employers to easily find and connect with them.

---

## 🚀 Key Features

- 🔐 Worker registration with skills, ID number, photo, and location
- 🔍 Employer dashboard with search and profile view
- 📌 Bookmark system for employers to save favorite workers
- 🛡️ Custom admin panel to manage and verify worker profiles
- ⚡ Session-based access without requiring login for workers
- 💻 Fully responsive layout styled with Tailwind CSS

---

## 📸 Screenshots

| Welcome Page | Worker List | Admin Panel |
|--------------|-------------|-------------|
| ![](images/skillhire%20welcome.PNG) | ![](images/skillhire%20picture%202.PNG) | ![](images/skillhire%20picture%203.PNG) | ![](images/skillhire%20picture%203.PNG) | ![](images/skillhire%20picture%204.PNG)
 | ![](images/skillhire%20picture%205.PNG)  | ![](images/skillhire%20picture%206.PNG)  | ![](images/skillhire%20picture%207.PNG)  | ![](images/skillhire%20picture%208.PNG)  | ![](images/skillhire%20picture%2011.PNG)



---

## 🛠 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Database:** SQLite (default)
- **Version Control:** Git + GitHub

---

## 📁 Project Structure

```plaintext
skillhire/
├── templates/           # HTML templates
├── static/              # CSS/JS files
├── workers/             # Worker-related logic
├── employers/           # Employer dashboard and views
├── admin_panel/         # Custom admin interface
├── db.sqlite3           # Default local database
├── manage.py            # Django project manager
└── README.md


⚙️ Getting Started
To run this project locally:

# Clone the repository
git clone https://github.com/unsashafiq/skillhire.git
cd skillhire

# Create virtual environment
python -m venv env
env\Scripts\activate  # For Windows
# or
source env/bin/activate  # For macOS/Linux

# Install dependencies
pip install -r requirements.txt  # if available

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.

💼 Use Cases
🧑‍🔧 Skilled workers without technical know-how can easily register

🧑‍💼 Employers can find and shortlist talent quickly

👩‍💻 Admins can control fake or spam registrations

📚 Academic Purpose
This project was developed as a Final Year Project under the supervision of Ma'am Kainat at The Islamia University of Bahawalpur for the BS Information Technology program.

👩‍💻 Author
Unsa Shafiq
Full Stack Developer | Django | Shopify | Tailwind CSS

📧 Email: unsashafiq160@gmail.com
🔗 LinkedIn: linkedin.com/in/unsa-shafiq-026018269
📸 Instagram: @unsa_shafiq02

📝 License
This project is for academic and portfolio use only. Not for commercial use without permission.



