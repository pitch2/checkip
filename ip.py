import subprocess
import concurrent.futures
import socket

ip_dep = input("Début de la plage à analyser : ")
ip_fin = input("Fin de la plage à analyser : ")


def get_hostname(ip_address):
    hostname = socket.gethostbyaddr(ip_address)
    return hostname[0]

def requete(ip):
    try:
        result = subprocess.run(["ping", ip], capture_output=True, text=True)
        if "TTL=" in result.stdout:
            hostname = get_hostname(ip)
            return f"{ip} -> {hostname}"
        else:
            return f"{ip} -> X"

    except subprocess.CalledProcessError:
        return f"{ip} -> X"

def multi_requete(liste):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requete, ip) for ip in liste]
        
        for future, ip in zip(futures, liste):
            result = future.result()
            print(result)


result_ip_dep = requete(ip_dep)
print(result_ip_dep)

ip = ip_dep
while ip != ip_fin:
    listeip = []
    for _ in range(255):
        ip_parts = list(map(int, ip.split('.')))
        if ip_parts[3] < 255 and ip_fin != f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{ip_parts[3]+1}":
            ip_parts[3] += 1
        else:
            ip_parts[3] = 0
            ip_parts[2] += 1

        ip = ".".join(map(str, ip_parts))

        listeip.append(ip)
    

    multi_requete(listeip)
