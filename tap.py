import requests
import personal_data
import time
import json
import random

def sync():
    flag = True
    my = {}

    url = "https://api.hamsterkombat.io/clicker/sync"

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
        "Cache-Control": "no-cache",
        "Referer": "https://hamsterkombat.io/"
    }

    try:
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print("Request successful SYNC")

            data = response.json()
            t = str(int(time.time()))
            with open(f'report/sync_{t}.json', 'w') as file:
                json.dump(data, file)

            my = {
                'availableTaps': data['clickerUser']['availableTaps'],
                'earn_per_tap' : data['clickerUser']['earnPerTap'],
                'max_tap' : data['clickerUser']['maxTaps'],
                'tap_recovery_per_sec' : data['clickerUser']['tapsRecoverPerSec']
            }
            print('sync: ', my)

        else:
            print("\nFailed to fetch data in SYNC:", response.status_code)
            flag = False

    except Exception as e:
        flag = False
        print('Request ERROR! SYNC')
        t = str(int(time.time()))
        with open(f'report/sync_error_{t}.txt', 'w') as f:
            f.write(str(e))
    finally:
        return flag, my

def tap():
    status, d = sync()
    my = {}

    if status:
        url = "https://api.hamsterkombat.io/clicker/tap"
        available = d['availableTaps']
        pertap = d['earn_per_tap']
        recoverpersec = d['tap_recovery_per_sec']

        headers = {
            "User-Agent": personal_data.user_agent,
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Authorization": personal_data.aut,
            "content-type": "application/json",
            "Sec-GPC": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=4",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }

        tap_count = available // pertap
        availabletap = available - (tap_count * pertap)
        stamp = int(time.time())

        body = {
            "count": tap_count,
            "availableTaps": availabletap,
            "timestamp": stamp 
        }
        print('\nTAP request body:')
        for i in body.keys():
            print('\t' + i + ': ' + str(body[i]))

        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))

            if response.status_code == 200:
                print("\nRequest successful TAP:")

                data = response.json()
                t = str(int(time.time()))
                with open(f'report/tap_{t}.json', 'w') as f:
                    json.dump(data, f)

                my = {
                    'earn_per_tap' : data['clickerUser']['earnPerTap'],
                    'max_tap' : data['clickerUser']['maxTaps'],
                    'earn_per_sec' : data['clickerUser']['earnPassivePerSec'],
                    'earn_per_hour' : data['clickerUser']['earnPassivePerHour'],
                    'last_pasive_earn' : data['clickerUser']['lastPassiveEarn'],
                    'tap_recovery_per_sec' : data['clickerUser']['tapsRecoverPerSec'],
                    'total_coin' : data['clickerUser']['totalCoins'],
                    'balance' : data['clickerUser']['balanceCoins']
                }
                print('Tap response:')
                for i in my.keys():
                    print('\t' + i + ': ' + str(my[i]))
 
            else:
                print("\nFailed to fetch data:", response.status_code)

        except Exception as e:
            print('\n\nERROR!')
            t = str(int(time.time()))
            with open(f'report/tap_error_{t}.txt', 'w') as f:
                f.write(str(e))

    else:
        print('\n\nFailed Sync...')

counter = 0
while True:
    wait_time = random.randint(20 * 60, 30 * 60)
    
    t = str(time.time())
    with open(f'report/schedule.txt', 'a') as f:
        f.write(f"#{counter}\t{t}: Waiting for {wait_time // 60} minutes and {wait_time % 60} seconds.\n")

    print(f"#{counter}\t{t}: Waiting for {wait_time // 60} minutes and {wait_time % 60} seconds.")

    counter += 1

    tap()
    time.sleep(wait_time)
