import requests, json, random, string, time, os, sys
from colorama import Fore, Back, Style
import tempmail

count = 0


def main():
    timerr = 0
    st = time.time()
    mail = tempmail.create_email()
    if mail == "RateLimit":
        print(f"{Fore.RED}[ERROR]{Fore.RESET} RateLimited")
        time.sleep(30)
        main()
    email = mail[0]
    session = requests.Session()
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    ravelpassword = ("").join(random.choices(string.ascii_letters + string.digits, k = 8))
    authenticity_token = session.get("https://www.ravelry.com/invitations", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36", "accept-language": "en-GB,en;q=0.9"}).text
    authenticity_token = authenticity_token.split('<meta content="')[2].split('"')[0]
    payload = {
        "authenticity_token": authenticity_token,
        "invite": "1",
        "guest": "Y",
        "email": email
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "accept-language": "en-GB,en;q=0.9",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-ua": '"Chromium";v="87", " Not A;Brand";v="99", "Google Chrome";v="87"',
        "sec-ua-mobile": "?0"
    }
    x = session.post("https://www.ravelry.com/invitations/ask", headers=headers, data=payload)
    time.sleep(1)
    token = mail[1]
    code = tempmail.get_messages(token)
    if code == False:
        while True:
            code = tempmail.get_messages(token)
            if code != False:
                break
            else:
                time.sleep(3)
                timerr += 1
                print("No code found")
                if timerr == 5:
                    print("No code found")
                    continue
    payload = {
        "authenticity_token": authenticity_token,
        "_method": "put",
        "code": code,
        "user[login]": username,
        "email": email,
        "user[password]": ravelpassword,
        "user[password_confirmation]": ravelpassword,
    }
    verify = session.post(f"https://www.ravelry.com/people/JessicaMF/invite/{email}", headers=headers, data=payload)
    checkuser = session.get(f"https://www.ravelry.com/people/{username}")
    if checkuser.status_code == 404:
        print(f"{Fore.RED}[-] Error creating account{Fore.RESET}")
    else:
        et = time.time()
        print(f"{Fore.GREEN}[+]{Fore.RESET} Account Created - " + email + ":" + ravelpassword + " - " + username + " - Took " + str(et - st) + " seconds\n")
        with open("ravelry.txt", "a") as f:
            f.write(email + ":" + username + ":" + ravelpassword + "\n")



for i in range(10000):
    count+=1
    if count == 15:
        print(f"{Fore.BLUE}[INFO]{Fore.RESET} WAITING 15 SECONDS FOR RATE LIMIT")
        time.sleep(20)
        count = 0
    main()
