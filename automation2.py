import requests
import re
import time
import subprocess

subprocess.Popen(["haproxy", "-f", "haproxy.cfg"])

checker, ip = "domain1.com", "http://192.168.0."

def requster(url):
    try:
        response = requests.get(url)
        match = re.search(r"<div class=\"fullscreen-text\">\s*(.*?)\s*</div>", response.text)
        return match.group(1)
    except:
        print("server changed the IP addresses")

def changeIP():
    for i in range(2,5,1):
        domain = requster(ip + str(i)) #domain1, domain2, domain3
        print(domain)
        command = "echo 'set server backend" + domain[-5] + "/server" + domain[-5] + " addr " + (ip + str(i))[7:] + "' | nc localhost 9999"
        output = subprocess.check_output(command, shell=True, text=True)
        # print("commmand ====> " + command)
        print("changed ====> server" + domain[-5] + " ==> " + ip + str(i))



while True:
    value = requster(ip + "2")
    if value != checker:
        checker = value
        try :
            changeIP()
            print("===================================================================")
            print("=                  ===> changing servers IP  <===                 =")
            print("===================================================================")
        except:
            time.sleep(3)
    # time.sleep(1)








