# Meal Planner

Jednostavna aplikacija za planiranje obroka (FastAPI + Angular).  
Omogućuje registraciju/prijavu, te dodavanje, uređivanje, brisanje i filtriranje obroka po datumu.

## Tehnologije

- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Pydantic, Passlib (bcrypt), python-jose (JWT), Uvicorn, SQLite
- **Frontend:** Angular 16+ (standalone), TypeScript, SCSS
- **Baza:** SQLite (`backend/app.db` — automatski se kreira)

---

## Brzi start

### 1) Backend

```bash
cd backend

# (preporučeno) virtualno okruženje
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# PowerShell ponekad traži:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# ovisnosti (ako postoji requirements.txt):
pip install -r requirements.txt
# ili ručno:
pip install "fastapi>=0.111" "uvicorn[standard]" sqlalchemy "passlib[bcrypt]" "python-jose[cryptography]" python-multipart pydantic "pydantic[email]"
Pokretanje:

bash
Kopiraj kod
uvicorn app.main:app --reload --port 8000
API dokumentacija: http://localhost:8000/docs

Health check: GET /healthz → {"ok": true}

Baza: backend/app.db se automatski stvara prvi put (u kodu je Base.metadata.create_all(bind=engine)).

Napomena: CORS je podešen za http://localhost:4200.

2) Frontend
bash
Kopiraj kod
cd frontend
npm i
ng serve --open
Aplikacija: http://localhost:4200

Funkcionalnosti
Auth:

POST /auth/register — registracija ({ "email": "...", "password": "..." })

POST /auth/login — login (form-data username, password) → JWT token

GET /me — trenutačni korisnik (Authorization: Bearer <token>)

Meals (zahtijeva Authorization):

GET /meals?from_={YYYY-MM-DD}&to={YYYY-MM-DD}

POST /meals — { "date": "YYYY-MM-DD", "title": "string", "calories": int }

GET /meals/{id}

PUT /meals/{id}

DELETE /meals/{id}

Kako testirati (ručno)
POST /auth/register (npr. email: test@example.com, lozinka npr. lozinka123).

POST /auth/login → preuzmi access_token.

U Swaggeru klikni Authorize i zalijepi Bearer <access_token>.

Kreiraj obrok preko POST /meals ili kroz UI na /dashboard.

Konfiguracija/napomene
SQLite je lokalna datoteka backend/app.db. Ne treba je slati; kreira se automatski.

JWT i hashing lozinki (bcrypt) već su konfigurirani u app/auth.py.

CORS: dopušten http://localhost:4200.

Frontend environment.ts koristi apiUrl = 'http://localhost:8000'.

Struktura projekta
bash
Kopiraj kod
meal-planner/
├─ backend/
│  ├─ app/
│  │  ├─ main.py         # FastAPI rute
│  │  ├─ db.py           # engine, Base, get_db()
│  │  ├─ models.py       # SQLAlchemy modeli
│  │  ├─ schemas.py      # Pydantic modeli
│  │  ├─ auth.py         # auth, JWT, hash/verify
│  │  └─ __init__.py
│  ├─ app.db             # (auto-kreira se, ignorira u git-u)
│  └─ requirements.txt   # (preporučeno dodati)
├─ frontend/
│  ├─ src/...
│  └─ angular.json, package.json, ...
└─ README.md
