# Flask and MongoDB Atlas – Snehal

## Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env         # Mac/Linux: cp .env.example .env
# edit .env and paste your MongoDB Atlas connection string into MONGO_URI
python app.py
```
Open http://127.0.0.1:5000

## Routes
| Route | Description |
|-------|-------------|
| `/` | Home page with links |
| `/api` | Reads `data.json` and returns the list as JSON |
| `/form` | Form (GET) / insert into MongoDB Atlas (POST) |
| `/success` | Shows "Data submitted successfully" |

GitHub repository: <paste your link here>
