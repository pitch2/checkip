import subprocess
import concurrent.futures
import socket

f = open("scanip.txt", "w")
f.close()

ip_dep = input("Début de la plage à analyser : ")
ip_fin = input("Fin de la plage à analyser : ")

def get_hostname(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)
        return hostname[0]
    except socket.herror as err:
        return f"Erreur: Impossible de résoudre le nom pour {ip_address} -> {err}"

def requete(ip):
    try:
        result = subprocess.run(["ping", ip], capture_output=True, text=True)
        if "TTL=" in result.stdout:
            hostname = get_hostname(ip)
            with open("scanip.txt", "a") as f:
                f.write(f"{ip} -> {hostname}\n")
            return f"{ip} -> {hostname}"
        else:
            with open("scanip.txt", "a") as f:
                f.write(f"{ip} -> X\n")
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
ip_fin_parts = list(map(int, ip_fin.split('.')))

while ip != ip_fin:
    listeip = []
    ip_parts = list(map(int, ip.split('.')))

    while ip_parts[2] <= ip_fin_parts[2] and ip != ip_fin:
        for _ in range(255):
            if ip_parts[3] >= ip_fin_parts[3] or ip == f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{ip_parts[3] + 1}":
                break
            else:
                ip_parts[3] += 1

            ip = ".".join(map(str, ip_parts))
            listeip.append(ip)

    multi_requete(listeip)
