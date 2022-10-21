import requests, colorama, os, sys, time, random, json
from colorama import Fore, Back, Style
def get_domains():
    headers={"Content-Type": "application/json"}
    x = requests.get("https://api.mail.tm/domains", headers=headers).json()
    domain = x["hydra:member"][0]["domain"]
    return domain


def create_account(domain):
    rand = random.randint(10000, 999999999)
    #create a random password
    password = str(rand)
    addr = str(rand) + "@" + domain
    body = {
      "address": addr,
      "password": password
    }
    headers={"Content-Type": "application/json"}
    createacc = requests.post("https://api.mail.tm/accounts", headers=headers, json=body).status_code
    if createacc == 201:
        print(f"{Fore.BLUE}[INFO]{Fore.RESET} Email "+ addr + " created.")
        return addr, password
    
def get_jwt(addr, password):
    body = {
      "address": addr,
      "password": password
    }
    headers={"Content-Type": "application/json"}
    getjwt = requests.post("https://api.mail.tm/token", headers=headers, json=body)
    print(getjwt.status_code)
    getjwt = getjwt.json()
    authheaders = {"Authorization": "Bearer " + getjwt["token"], "Content-Type": "application/json"}
    return authheaders



def check_mail(authheaders):
    emails = True
    checkmail = requests.get("https://api.mail.tm/messages", headers=authheaders).json()
    timer = 0
    while True:
        if checkmail["hydra:member"] == []:
            print(f"{Fore.YELLOW}[WARN]{Fore.RESET} NO EMAILS DETECTED YET.")
            time.sleep(3)
            checkmail = requests.get("https://api.mail.tm/messages", headers=authheaders).json()
            # if there is no email within 20 seconds of the function being called, return false
            timer += 1
            if timer == 4:
                return False
                break
            # this is to prevent the program from getting stuck in an infinite loop
        else:
            print(f"{Fore.GREEN}[+]{Fore.RESET} Email Found")
            #get the content of the email
            email_id = checkmail["hydra:member"][0]["id"]
            email = requests.get("https://api.mail.tm/messages/" + email_id, headers=authheaders).json()
            print(f"{Fore.GREEN}[+]{Fore.RESET} DETECTED EMAIL")
            text = email["text"]
            text = str(text)
            link = text.split("https://ravelry.com/invite/")[1].split(" ")[0]
            #remove the last 4 characters of the list
            link = link[:-4]
            link = link.strip('"')
            link = link.replace("\n", "")
            link = "https://ravelry.com/invite/" + link
            #get the code from the ?code=part of the link
            code = link.split("?code=")[1]
            print(code)
            return code
            break
