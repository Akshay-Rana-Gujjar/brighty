import os
import sys
from bottle import route, run, static_file
import bottle
import subprocess
import socket

display_vendor = subprocess.check_output("ls /sys/class/backlight/", shell=True)
display_vendor = str(display_vendor, "utf-8").replace("\n","")

host = "0.0.0.0"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
s.close()

app = bottle.Bottle()
app.config.load_config('config.cfg')

password = app.config["confidential.password"]

@route('/set/<brightnessPercentage>')
def index(brightnessPercentage):

  command = "echo "+brightnessPercentage+" | sudo tee /sys/class/backlight/"+display_vendor+"/brightness"
  os.system('echo %s|sudo -S %s' % (password, command))
  return "set to "+brightnessPercentage
@route('/')
def start():

  return static_file("index.html", root="./")

print("\n\n", """
open http://{}:{} in your mobile browser 
""".format(local_ip, "8080"))

run(host=host, port=8080)