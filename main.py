import os, requests, csv, time, pickle, sys
from fake_useragent import UserAgent
from colorama import init, Fore

init(autoreset=True)

# --- COLORS & UI ---
G, R, C, W = Fore.GREEN, Fore.RED, Fore.CYAN, Fore.WHITE
INFO, PLUS, ERROR = f"{C}[i]{W}", f"{G}[+]{W}", f"{R}[!]{W}"

def load_session():
    """Loads the session from file or prompts to create one"""
    if not os.path.exists('session_file.txt'):
        print(f"{INFO} Setup: Create session_file.txt")
        username = input(f"{PLUS} IG Username: ").strip()
        session_id = input(f"{PLUS} sessionid Cookie: ").strip()
        session_data = [username, session_id, username]
        with open('session_file.txt', 'wb') as f:
            pickle.dump(session_data, f)
        return session_data
    with open('session_file.txt', 'rb') as f:
        return pickle.load(f)

def get_total_count(username):
    """Hits the Instagram API to get the summary follower count"""
    headers = {
        "user-agent": UserAgent().random,
        "x-ig-app-id": "936619743392459",
        "referer": f"https://www.instagram.com/{username}/",
        "x-requested-with": "XMLHttpRequest"
    }
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        # Pulls 'edge_followed_by' which is the total number on the profile
        data = resp.json()['data']['user']
        return data['edge_followed_by']['count']
    except:
        return None

def format_number(num):
    """Converts 6000000 to 6.0M"""
    if num is None: return "Error"
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def main():
    load_session()
    
    if not os.path.exists('accounts.csv'):
        print(f"{ERROR} accounts.csv not found!")
        return

    # Read usernames from input CSV
    with open('accounts.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        targets = [row[0].strip() for row in reader if row and row[0].strip()]

    # 'w' mode deletes the old list of thousands of names
    output_file = "followers_total.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for username in targets:
            print(f"{INFO} Fetching count for: {W}{username}...")
            
            raw_count = get_total_count(username)
            count_text = format_number(raw_count)
            
            # This writes exactly: username, 6.0M
            writer.writerow([username, count_text])
            print(f"{PLUS} {username}, {count_text}")
            
            # Small delay to stay safe
            time.sleep(2)

    print(f"\n{PLUS} Done! View clean totals in {output_file}")

if __name__ == "__main__":
    main()