import requests as re
import colorama
from colorama import Fore, Back, Style
import json

colorama.init()
print(f"""{Fore.LIGHTGREEN_EX}
 █     █░ ██▓███       ██████  ▄████▄   ▄▄▄       ███▄    █  ███▄    █ ▓█████  ██▀███  
▓█░ █ ░█░▓██░  ██▒   ▒██    ▒ ▒██▀ ▀█  ▒████▄     ██ ▀█   █  ██ ▀█   █ ▓█   ▀ ▓██ ▒ ██▒
▒█░ █ ░█ ▓██░ ██▓▒   ░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██  ▀█ ██▒▓██  ▀█ ██▒▒███   ▓██ ░▄█ ▒
░█░ █ ░█ ▒██▄█▓▒ ▒     ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▓██▒  ▐▌██▒▓██▒  ▐▌██▒▒▓█  ▄ ▒██▀▀█▄  
░░██▒██▓ ▒██▒ ░  ░   ▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒▒██░   ▓██░▒██░   ▓██░░▒████▒░██▓ ▒██▒
░ ▓░▒ ▒  ▒▓▒░ ░  ░   ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
  ▒ ░ ░  ░▒ ░        ░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░░ ░░   ░ ▒░░ ░░   ░ ▒░ ░ ░  ░  ░▒ ░ ▒░
  ░   ░  ░░          ░  ░  ░  ░          ░   ▒      ░   ░ ░    ░   ░ ░    ░     ░░   ░ 
    ░                      ░  ░ ░            ░  ░         ░          ░    ░  ░   ░     
                              ░                                                        
                                                                        {Fore.LIGHTMAGENTA_EX}by @nb1b3k""")
print(f"{Fore.LIGHTCYAN_EX}Input a wordpress site below: ")
userInput = input("Target: ")
website = userInput.replace("https://", "")
website = website.replace("http://", "")
website = "https://" + website
# add scheme if not present


checks = ['xmlrpc.php', 'wp-cron.php', 'wp-config.php', 'wp-includes/', 'wp-content', 'wp-json', 'robots.txt', 'sitemap.xml', '.htaccess', '.gitignore', '.git', '.log']
ua = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

# GET RESPONSE
for path in checks:
    #Assign URLS to check
    global url
    url = f"{website}/{path}"

    #GET URL
    try:
        getData = re.get(url, headers=ua)
        status_code = getData.status_code
        responseSource = getData.text

        # XML-RPC check
        if "xmlrpc.php" in url and "XML-RPC server accepts POST requests only" in responseSource:
            print(f"{Fore.GREEN} \n[+] XML-RPC is enabled :)\n[+] URL: {Fore.BLUE} {url}")
        elif "xmlrpc.php" in url and "XML-RPC server accepts POST requests only" not in responseSource:
            print(f"{Fore.RED} \n[!] XML-RPC is disabled :(")


        #check for wp-config.php
        elif "wp-config.php" in url and "" in responseSource:
            print(f"{Fore.RED} \n[!] wp-config.php is not accessible :(")
        elif  "wp-config.php" in url and "" not in responseSource:
            print(f"{Fore.GREEN} \n[+] wp-config.php is accessible :)\nURL: {Fore.BLUE} {url}")


        #check for wp-cron.php
        elif "wp-cron.php" in url and "" in responseSource:
            print(f"{Fore.RED} \n[!] wp-cron.php is not accessible :(")
        elif  "wp-cron.php" in url and "" not in responseSource:
            print(f"{Fore.GREEN} \n[+] wp-cron.php is accessible :)\nURL: {Fore.BLUE} {url}")


        #check for wp-includes
        elif "wp-includes" in url and "403 Forbidden" in responseSource:
            print(f"{Fore.RED} \n[!] Directory listing is disabled in /wp-includes/ :(")
        elif  "wp-includes" in url and "Index of" in responseSource:
            print(f"{Fore.GREEN} \n[+] Directory listing is enabled in /wp-includes/ :)\nURL: {Fore.BLUE} {url}")

        #check for wp-content
        elif "wp-content" in url and "403 Forbidden" in responseSource:
            print(f"{Fore.RED} \n[!] Directory listing is disabled in /wp-content/ :(")
        elif  "wp-content" in url and "Index of" in responseSource:
            print(f"{Fore.GREEN} \n[+] Directory listing is enabled in /wp-content/ :)\nURL: {Fore.BLUE} {url}")

        #check for wp-json
        elif "wp-json" in url and ("rest_login_required" in responseSource or "rest_cannot_access" in responseSource):
            print(f"{Fore.RED} \n[!] wp-json is disabled :(")
        elif  "wp-json" in url and ("description" in responseSource or "endpoints" in responseSource):
            print(f"{Fore.GREEN} \n[+] wp-json is enabled! :)\nURL: {Fore.BLUE} {url}")


            print(f"{Fore.GREEN}\nTrying to enumerate users.....")
            url2 =  f'{url}/wp/v2/users'
            print(f'URL: {Fore.BLUE} {url2}\n')
            dataReceived = re.get(url2, headers=ua).json()

            #loop 20 to get admin users
            for nums in range(10):
                try:
                    data = dataReceived[nums]
                    print(f'{Fore.GREEN}AdminUsername(s): {Fore.BLUE} {data["slug"]}')
                except IndexError:
                    pass


        #check for robots.txt file
        elif "robots.txt" in url and "User-agent" not in responseSource:
            print(f"{Fore.RED} \n[!] robots.txt file is not found on the target :(")
        elif  "robots.txt" in url and "User-agent" in responseSource:
            print(f"{Fore.GREEN} \n[+] robots.txt file found! :)\nURL: {Fore.BLUE} {url}\n")
            print(f"{Fore.GREEN} \n[+] Printing its content now...\n")
            print(f"{Fore.BLUE}{responseSource}")


        #check for sitemap.xml
        elif "sitemap.xml" in url and "404" in str(status_code):
            print(f"{Fore.RED} \n[!] Sitemap not found :(")
        elif  "sitemap.xml" in url and "200" in str(status_code):
            print(f"{Fore.GREEN} \n[+] Sitemap found! :)\nURL: {Fore.BLUE} {url}")
        elif "sitemap.xml" in url and "302" in str(status_code):
            print(f"{Fore.GREEN} \n[+] Sitemap found! :)\nURL: {Fore.BLUE} {website}/wp-sitemap.xml")


        #check for .htaccess
        elif ".htaccess" in url and "404" in str(status_code):
            print(f"{Fore.RED} \n[!] .htaccess not found :(")
        elif  ".htaccess" in url and "200" in str(status_code):
            print(f"{Fore.GREEN} \n[+] .htaccess found! :)\nURL: {Fore.BLUE} {url}")
        elif ".htaccess" in url and "403" in str(status_code):
            print(f"{Fore.RED} \n[!] .htaccess found but is forbidden to access :(")


        #check for .gitignore
        elif ".gitignore" in url and "404" in str(status_code):
            print(f"{Fore.RED} \n[!] .gitignore not found :(")
        elif  ".gitignore" in url and "200" in str(status_code):
            print(f"{Fore.GREEN} \n[+] .gitignore found! :)\nURL: {Fore.BLUE} {url}")
        elif ".gitignore" in url and "403" in str(status_code):
            print(f"{Fore.RED} \n[!] .gitignore found but is forbidden to access :(")

        #check for .git
        elif ".git" in url and "404" in str(status_code):
            print(f"{Fore.RED} \n[!] .git not found :(")
        elif  ".git" in url and "200" in str(status_code):
            print(f"{Fore.GREEN} \n[+] .git found! :)\nURL: {Fore.BLUE} {url}")
        elif ".git" in url and "403" in str(status_code):
            print(f"{Fore.RED} \n[!] .git found but is forbidden to access :(")


        #check for .log
        elif ".log" in url and "404" in str(status_code):
            print(f"{Fore.RED} \n[!] .log not found :(")
        elif  ".log" in url and "200" in str(status_code):
            print(f"{Fore.GREEN} \n[+] .log found! :)\nURL: {Fore.BLUE} {url}")
        elif ".log" in url and "403" in str(status_code):
            print(f"{Fore.RED} \n[!] .log found but is forbidden to access :(")
    except:
        print(f"{Fore.RED}Input a valid URL. It should have a domainName and domain extension.")
