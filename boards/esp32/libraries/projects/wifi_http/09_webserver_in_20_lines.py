import socket
import machine
from board import LED


# HTML to send to browsers
html = """<!DOCTYPE html>
<html>
  <head> <title>ESP32 Webserver LED control</title> </head>
  <h2>ESP32 Webserver</h2>
  <form>
    <button name="LED" value="ON" type="submit">LED ON</button>
    <button name="LED" value="OFF" type="submit">LED OFF</button>
  </form>
</html>
"""

# Setup PINS
led = machine.Pin(LED, machine.Pin.OUT)

# Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
print("Server running on port 80")
s.listen(5)
while True:
    print("Waiting for client")
    conn, addr = s.accept()
    print("Got a connection from", str(addr))
    request = str(conn.recv(1024))
    print("Request =", request)
    if request.find('/?LED=ON') == 6:
        led(1)
    if request.find('/?LED=OFF') == 6:
        led(0)
    conn.send(html)
    conn.close()
    print()
