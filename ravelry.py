import requests, json, random, string, time, os, sys
from colorama import Fore, Back, Style
import tempmail

def main():
    email, password = tempmail.create_account("karenkey.com")
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
    time.sleep(0.3)
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
    print(x.status_code)
    #check the emails
    authheaders = tempmail.get_jwt(email, password)
    time.sleep(0.2)
    code = tempmail.check_mail(authheaders)
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
    time.sleep(0.3)
    checkuser = session.get(f"https://www.ravelry.com/people/{username}")
    if checkuser.status_code == 404:
        print(f"{Fore.RED}[-] Error creating account{Fore.RESET}")
    else:
        print(f"{Fore.GREEN}[+]{Fore.RESET} Account Created - " + email + ":" + ravelpassword + " - " + username)
        with open("ravelry.txt", "a") as f:
            f.write(email + ":" + ravelpassword + ":" + username + "\n")
        print("sending message")
        x = session.post("https://www.ravelry.com/messages", headers=headers, data={"authenticity_token": authenticity_token, "message[subject]": "test", "message[body]": "test", "message[recipient]": username, "markdown_suggester_activated": "", "_": "", "namespace_login": f"message:{username}"})

for i in range(1000):
    main()
