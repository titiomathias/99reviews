# 📝 99reviews

## 🎯 Project Goal

Build an API to fetch and expose the reviews from my freelancer profile on [99freelas](https://www.99freelas.com.br/user/tio-mathias).

> ⚠️ The data is updated every 24 hours.

---

## 🛠️ Tech Stack

- ⚡ [FastAPI](https://fastapi.tiangolo.com) — for building the RESTful API
- 🧼 [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/en/latest/) — for HTML parsing
- 🛡️ [cfscrape](https://pypi.org/project/cfscrape/) — to bypass Cloudflare protections

---

## 🐍 A Pythonic Solution to Scrape and Serve Reviews

This project provides a simple and elegant way to programmatically access your public reviews from 99freelas, making it easy to integrate with dashboards, personal websites, or other services.

---

## 🚀 Running the Project (Optional)

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload
