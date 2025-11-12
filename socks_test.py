import requests
import socks
import socket
import time

# Configure SOCKS proxy for requests
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket
url = "https://check.torproject.org/"
while True:
    try:
        response = requests.get(url)
        print(response.text)
        if "Congratulations" in response.text:
            print("Tor is working!")
        else:
            print("Tor is not working.")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(3)