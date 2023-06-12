import subprocess
import sys
import time

timeOut = 10


dockers = ["docker1", "docker2", "docker3"]


def shuffle(my_list):
    first_element = my_list.pop(0)
    my_list.append(first_element)




for i in range(1, 100, 1):
    shuffle(dockers)
    print("\ndocker up ====>", dockers,"<====\n")
    for i in range(3):
        try:
            # docker run --rm -d --name docker2 --network my_docker_network --ip 192.168.0.2 docker2
            command = "docker run --rm -d --name " + dockers[i] + " --network my_docker_network --ip 192.168.0." + str(i + 2) + " " + dockers[i]
            print("==> 192.168.0." + str(i + 2) + " <==")
            output = subprocess.check_output(command, shell=True, text=True)
        except:
            print("failed to run docker : ", dockers[i])
    print("\nsuccessfully run dockers....")
    time.sleep(timeOut) 

    print("\n")
    for i in range(3):
        try:
            command = "docker ps --filter ancestor=" + dockers[i] + " --format '{{.ID}}'"
            print("                     stop ==> " + dockers[i])
            container_id = subprocess.check_output(command, shell=True, text=True)
            command = "docker stop " + container_id
            container_id = subprocess.check_output(command, shell=True, text=True)
        except:
            print("failed to stop docker : ", dockers[i])
    

