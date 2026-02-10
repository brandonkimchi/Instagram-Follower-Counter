import os, requests, csv, time, pickle, sys
from fake_useragent import UserAgent
from colorama import init, Fore

init(autoreset=True)

# colors
G, R, C, W = Fore.GREEN, Fore.RED, Fore.CYAN, Fore.WHITE
INFO, PLUS, ERROR = f"{C}[i]{W}", f"{G}[+]{W}", f"{R}[!]{W}"

def load_session():
    if not os.path.exists('session_file.txt'):
        print(f"{ERROR} session_file.txt not found! Please create it first.")
        sys.exit(1)
    with open('session_file.txt', 'rb') as f:
        return pickle.load(f)

def get_total_count(username):
    """Hits the profile API and returns only the total follower number"""
    headers = {
        "user-agent": UserAgent().random,
        "x-ig-app-id": "936619743392459",
        "referer": f"https://www.instagram.com/{username}/",
        "x-requested-with": "XMLHttpRequest"
    }
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        # Pulls the exact count from the profile header
        count = resp.json()['data']['user']['edge_followed_by']['count']
        return count
    except Exception as e:
        return "Error/Private"

def main():
    load_session()
    
    if not os.path.exists('accounts.csv'):
        print(f"{ERROR} accounts.csv not found!")
        return

    # Read targets from your input file
    with open('accounts.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        targets = [row[0].strip() for row in reader if row and row[0].strip()]

    # We use 'w' to overwrite and clear the old list of thousands of names
    output_file = "followers_total.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for username in targets:
            print(f"{INFO} Fetching total for {username}...")
            total = get_total_count(username)
            
            # Format numbers to "M" (Millions) if they are large
            formatted_total = total
            if isinstance(total, int):
                if total >= 1_000_000:
                    formatted_total = f"{total/1_000_000:.1f}M"
                elif total >= 1_000:
                    formatted_total = f"{total/1_000:.1f}K"
            
            writer.writerow([username, formatted_total])
            print(f"{PLUS} Result: {username}, {formatted_total}")
            time.sleep(2)

    print(f"\n{PLUS} Done! Output saved in {output_file}")

if __name__ == "__main__":
    main()