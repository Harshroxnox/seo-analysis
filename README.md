# SEO Analysis
## Backend Setup
Make sure you have `python3.10` and `venv` installed.
<br><br>

Clone the project and go inside backend folder
```bash
git clone git@github.com:Harshroxnox/seo-analysis.git
```
```bash
cd seo-analysis/backend
```

First set up the `.env` filling in your API details. Then create virtual env inside backend folder.
```bash
python3 -m venv venv
```

Activate the virtual environment
```bash
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

Download nltk punkt_tab
```bash
python3 download.py
```

Start the backend server
```bash
python3 app.py
```