import requests, random
from colorama import Fore

base = 'https://api.tempmail.lol'


def create_email():
  #if a random.randint is 2
  if random.randint(1, 2) == 2:
    try:
      r = requests.get(base + f'/generate/rush').json()
      print(f"{Fore.BLUE}[INFO]{Fore.RESET} Created email: {r['address']}")
      return r['address'], r['token']
    except:
      return "RateLimit"
  else:
    try:
      r = requests.get(base + f'/generate').json()
      print(f"{Fore.BLUE}[INFO]{Fore.RESET} Created email: {r['address']}")
      return r['address'], r['token']
    except:
      return "RateLimit"


def get_messages(token):
  r = requests.get(base + f'/auth/{token}').json()
  if r['email'] == []:
    return False
  else:
    text = r['email'][0]['body']
    text = str(text)
    link = text.split("https://ravelry.com/invite/")[1].split(" ")[0]
    #remove the last 4 characters of the list
    link = link[:-4]
    link = link.strip('"')
    link = link.replace("\n", "")
    link = "https://ravelry.com/invite/" + link
    #get the code from the ?code=part of the link
    code = link.split("?code=")[1]
    print(f"{Fore.BLUE}[INFO]{Fore.RESET} GOT REGISTER CODE: {code}  |  {link}")
    return code
