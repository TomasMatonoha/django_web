# Install virtual environment
py -m venv .venv
# Activate virtual environment
.venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
npm install
# Run website
py manage.py runserver
