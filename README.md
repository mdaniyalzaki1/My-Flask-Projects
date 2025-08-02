## My-Flask-Projects

Welcome to my collection of web applications built with **Flask** — a powerful and lightweight Python web framework. This repo showcases my learning journey through hands-on projects, each adding new layers of functionality and depth.

> 🔧 This repo will continue to grow as I build more Flask apps and experiment with new features!

---

## 🚀 Projects So Far

### 1. 📝 Notes App (Collaborative Build)
A secure, multi-user notes manager where users can register, log in, and manage their own personal notes. This project was built with both independent coding and some helpful insights from others to learn clean architecture and security best practices.

#### Features
- User authentication (signup, login, logout)
- Password hashing with Werkzeug
- Per-user note visibility
- Add, edit, delete notes
- Flash messages with Bootstrap styling
- SQLite database integration using SQLAlchemy
- Context processors for cleaner templates
- CLI command to initialize the database

---

### 2. ✅ Todo App (Fully Solo Project)
My first solo Flask app — a simple and focused to-do list manager that I built completely on my own. No tutorials, no AI. Just me figuring it all out, one feature at a time. 😄

#### Features
- Add/delete tasks
- Clean UI with Bootstrap
- Simple, effective structure using Flask fundamentals

---

## 📁 Folder Structure

```
My-Flask-Projects/
│
├── notes-app/          # Notes app with user auth and database
│   ├── templates/
│   ├── static/
│   ├── app.py
│   └── ...
│
├── todo-app/           # Solo-built simple to-do list
│   ├── templates/
│   ├── static/
│   ├── app.py
│   └── ...
│
├── future-projects/    # More Flask apps coming soon!
│   └── ...
│
└── README.md           # You're here!
```

---

## 🛠️ Setup Instructions (for any project)

1. **Clone the repo**
   ```bash
   git clone https://github.com/mdaniyalzaki1/My-Flask-Projects.git
   cd My-Flask-Projects/project-folder-name
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (if needed)
   ```
   SECRET_KEY=your_secret_key
   ```

5. **Initialize the database** (if applicable)
   ```bash
   flask --app app.py init-db
   ```

6. **Run the app**
   ```bash
   flask --app app.py run
   ```

---

## 🙋 About Me

Hi! I'm **Zaki** — a dedicated programmer and eager learner who loves building stuff. This repo is part of my growth as a web developer, and I’ll be adding more projects as I explore new Flask concepts and features.

---

## ⭐ Star the Repo
If you like what you see, drop a ⭐! It means a lot and keeps me motivated to keep building.

---

Thanks for checking it out! Happy coding! 😄
```
