import base64
import json
import requests
import datetime
import personal_data

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.', '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..', 
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
}

def cipher_decode(e):
    t = e[:3] + e[4:]
    decoded_bytes = base64.b64decode(t)
    decoded_str = decoded_bytes.decode('utf-8')
    return(decoded_str)

def text_to_morse(text):
    morse_code = ''
    for char in text.upper():
        if char != ' ':
            morse_code += MORSE_CODE_DICT[char] + ' '
        else:
            morse_code += ' '
    return morse_code.strip()

def morse_to_text(morse):
    morse += ' '
    deciphered_text = ''
    citext = ''
    for letter in morse:
        if letter != ' ':
            citext += letter
            space_found = 0
        else:
            space_found += 1
            if space_found == 2:
                deciphered_text += ' '
            else:
                deciphered_text += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = ''
    return deciphered_text

def clame(cipher):
    flag = True

    url = "https://api.hamsterkombatgame.io/clicker/claim-daily-cipher"
    headers = {
        "User-Agent": personal_data.user_agent,
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "authorization": personal_data.aut,
        "content-type": "application/json",
        "Sec-GPC": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
    body = {
        "cipher": cipher
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        with open('cipher_resp.json', 'w') as f:
            json.dump(response.json(), f, indent = 4)


    except Exception as e:
        flag = False

    finally:
        return flag

def req1():
    url = "https://api.hamsterkombatgame.io/clicker/config"

    headers = {
        "User-Agent": personal_data.user_agent,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Authorization": personal_data.aut,
        "Sec-GPC": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=4",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
    flag = True
    cipher = ''
    is_clamed = ''

    try:
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            if 'dailyCipher' in data and 'cipher' in data['dailyCipher']:
                cipher = data['dailyCipher']['cipher']
                is_clamed = data['dailyCipher']['isClaimed']
                with open('c.json', 'w') as f:
                    json.dump(data, f, indent=4)

            else:
                print("dailyCipher or cipher not found in the response")
                flag = False

        else:
            print("Failed to fetch data:", response.status_code)
            flag = False

    except Exception as E:
        print('Request ERROR!')
        with open('report/ERROR.txt', 'w') as file:
            file.write(str(E))
        flag = False
    
    finally:
        return flag, cipher, is_clamed

flag, cipher, is_clamed = req1()
print(is_clamed)

if flag:
    text = cipher_decode(cipher)
    dt = datetime.datetime.now()
    today = dt.strftime("%B %d")

    morse_code = text_to_morse(text)
    post = f'''🗓 {today}

    String: {text}
    Morse: {morse_code}'''

    print('\n----------------------')
    print(post)

    with open('today.txt', 'w') as f:
        f.write(post)

    print('----------------------\n')

    if not is_clamed:
        flag = clame(text)
        if flag:
            print('\ndaily morse is clamed now.')
        else:
            print('Error in clame daily morse, try again.')


    print('daily morse is clamed.\ndone.')
