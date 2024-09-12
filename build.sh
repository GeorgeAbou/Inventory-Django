# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input #para que se menera la carpeta de archivos estaticos

# Apply any outstanding database migrations
python manage.py migrate