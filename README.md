# django-quizzes
A platform to create quizzes

## How to run the project

1. Clone the repository
```bash
git clone https://github.com/ivteplo/django-quizzes
```

2. Navigate into the cloned folder
```bash
cd django-quizzes
```

3. Initialize a virtual environment
```bash
python -m venv venv
```

4. Activate the virtual environment
```bash
source ./venv/Scripts/activate # bash, zsh, fish, etc.
./venv/Scripts/Activate.ps1 # powershell
```

5. Install dependencies
```bash
pip install -r requirements.txt
```

6. Set up environment variables in `.env` file (you'll most probably have to create the file):
```
SECRET_KEY=your-secret-key-for-django
```

7. Run migrations
```bash
python manage.py migrate
```

7. Start a server
```bash
python manage.py runserver
```

8. Happy hacking! 🎉
