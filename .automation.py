import requests
import re
import time
import subprocess

checker = "domain1.com"

backend1_address = "127.0.0.1:81"
backend2_address = "127.0.0.1:82"
backend3_address = "127.0.0.1:83"

def requster(url):
    try:
        response = requests.get(url)
        match = re.search(r"<div class=\"fullscreen-text\">\s*(.*?)\s*</div>", response.text)
        return match.group(1)
    except:
        print("\n=========> server changed the IP addresses")

        

def update_haproxy_config(backend1_add, backend2_add, backend3_add):


    config = f'''frontend http_front
   bind *:80
   mode http
   acl domain1 hdr(host) -i domain1.com
   acl domain2 hdr(host) -i domain2.com
   acl domain3 hdr(host) -i domain3.com

   use_backend backend1 if domain1
   use_backend backend2 if domain2
   use_backend backend3 if domain3
   default_backend default_backend

backend backend1
   mode http
   server server1 {backend1_add}

backend backend2
   mode http
   server server2 {backend2_add}

backend backend3
   mode http
   server server3 {backend3_add}

backend default_backend
   mode http
   server default_server 127.0.0.1:81
'''

    with open('haproxy.cfg', 'w') as file:
        file.write(config)


def changeIP():
    #1
    if checker == "domain1.com":
        backend1_address = "127.0.0.1:81"
    elif checker == "domain2.com":#backend2 deer bichegdene
        backend2_address = "127.0.0.1:81"
    elif checker == "domain3.com":
        backend3_address = "127.0.0.1:81"
    
    #2
    req2 = requster("http://127.0.0.1:82")
    if req2 == "domain1.com":
        backend1_address = "127.0.0.1:82"
    elif req2 == "domain2.com":
        backend2_address = "127.0.0.1:82"
    elif req2 == "domain3.com":
        backend3_address = "127.0.0.1:82"

    #3
    req3 = requster("http://127.0.0.1:83")
    if req3 == "domain1.com":
        backend1_address = "127.0.0.1:83"
    elif req3 == "domain2.com":
        backend2_address = "127.0.0.1:83"
    elif req3 == "domain3.com":
        backend3_address = "127.0.0.1:83"

    update_haproxy_config(backend1_address, backend2_address, backend3_address)
    print("\nserver1 ==> ", backend1_address,"\nserver2 ==> ", backend2_address, "\nserver3 ==> ",backend3_address,"\n")

subprocess.Popen(["haproxy", "-f", "haproxy.cfg"])

while True:
    value = requster("http://127.0.0.1:81")
    if value != checker:
        checker = value
        try :
            changeIP()
            subprocess.run(["pkill", "-f", "haproxy"])
            command = ["haproxy", "-f", "haproxy.cfg"]
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("===================================================================")
            print("=       ===> changing servers IP and restart proxy !!! <===       =")
            print("===================================================================")
        except:
            time.sleep(3)
    # time.sleep(1)


#########





