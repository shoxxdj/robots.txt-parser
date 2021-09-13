import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from termcolor import colored
from sys import argv

my_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"

url = argv[1]
headers = {
       'User-Agent': my_user_agent
}

r = requests.get(url+"/robots.txt",verify=False,headers=headers)

toCheck=[]
notChecked=[]
for line in r.text.split('\n'):
    if("Disallow" in line):
        sub=line.split(':')[1].strip()
        if(not "*" in sub):
            toCheck.append(sub)
        else:
            notChecked.append(sub)

for sub in toCheck:
    r = requests.get(url+"/"+sub,verify=False,headers=headers)
    if(r.status_code==200):
        print(colored("[{}] {}".format(r.status_code,sub),'green'))
    if(r.status_code>200 and r.status_code < 500):
        print(colored("[{}] {}".format(r.status_code,sub),'yellow'))
    if(r.status_code>500):
        print(colored("[{}] {}".format(r.status_code,sub),'red'))

print("Verified : {}, not check : {}".format(len(toCheck),len(notChecked)))
