# My-Budget-Tracker
En simpel budget-app skrevet i Python
## 🔧 Troubleshooting  
- If graphs fail:  
  ```bash
  python -m pip install --prefer-binary matplotlib

# 💰 Budget Tracker  

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A simple Python app to track income/expenses with SQLite database and visual reports.  

---

## ✨ Features  
- ✅ Add/edit/delete transactions  
- 📊 Generate expense graphs (Matplotlib)  
- 📅 Filter by date or category  
- 💾 Automatic local storage (SQLite)  

---

## 🚀 Quick Start  

### Windows Users:  
1. Download the [latest release](https://github.com/yourusername/My-Budget-Tracker/releases)  
2. **Double-click `install.bat`**  
3. Use the app!  

### Mac/Linux/Python Users:  
```bash
# Clone the repo
git clone https://github.com/yourusername/My-Budget-Tracker.git
cd My-Budget-Tracker

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py


❓ FAQ
Q: How do I reset my data?
→ Delete the data/budget.db file.

Q: Graphs won't show?
→ Run: python -m pip install --upgrade --prefer-binary matplotlib
