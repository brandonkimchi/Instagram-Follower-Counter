# 📸 Instagram Follower Counter

A lightweight, efficient Python tool to fetch real-time follower counts for Instagram profiles. It processes targets in bulk from a CSV and outputs clean, human-readable data (e.g., `642.4M`).

---

## 🚀 Quick Start Guide

### 1. Environment Setup
Navigate to your project folder and run the commands for your operating system:

**Mac / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your Instagram Session ID
The script requires a `sessionid` cookie to authenticate requests without needing your password.

1. Log in to [Instagram.com](https://www.instagram.com) on your desktop.
2. Press `F12` to open **Developer Tools**.
3. Navigate to the cookie storage:
   - **Chrome / Edge / Brave**: `Application` tab → `Cookies` → `https://www.instagram.com`
   - **Firefox**: `Storage` tab → `Cookies` → `https://www.instagram.com`
4. Locate the **`sessionid`** row and copy the **Value**.

### 4. Prepare Targets
Edit `accounts.csv` in the root directory. Add one username per line (no headers or @ symbols needed):
```csv
cristiano
leomessi
therock
```

### 5. Run the Tool
```bash
python main.py
```
* **First Run:** You will be prompted to enter your IG Username and the Session ID you copied earlier. This creates a `session_file.txt`.
* **Subsequent Runs:** The script will automatically log in using your saved session.

### 6. View Results
Results are saved to `followers_total.csv`.
```text
cristiano, 642.4M
leomessi, 504.1M
therock, 395.2M
```

---

## ⚠️ Important Notes

> [!CAUTION]
> **SECURITY:** `session_file.txt` contains your active login session. **Never** upload this file to GitHub or share it. Treat it as a password.

* **Rate Limiting:** The script waits 2–4 seconds between accounts to mimic human behavior and avoid being flagged.
* **Verified Accounts:** Works perfectly on all public profiles, including high-profile verified accounts.
* **Session Expiry:** If you see "Error," your session ID has likely expired. Delete `session_file.txt` and restart the script with a fresh ID.


---
**Disclaimer:** *This tool is for educational purposes only. Use responsibly and respect Instagram's Terms of Service.*
