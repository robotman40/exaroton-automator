import main
import configparser as cfgp
import time

def create_config(config):
    config["GENERAL"] = {
        "API Token": "None",
        "Server ID": "None",
        "Shutdown Notice Time": 30,
        "Notify Shutdown Every": 5,
        "Shutdown Warning": "THE SERVER WILL BE SHUTTING DOWN IN {time} MINUTES",
        # This allows us to convert the tuple back to its original form when we retrieve it
        "Periodic Actions": repr(((20, "/say Hi there :)"), (60, "/say Hi again")))
    }
    config["MONDAY"] = {
        "Start Minute": 0,
        "Uptime": 1440
    }
    config["TUESDAY"] = {
        "Start Minute": 0,
        "Uptime": 1440
    }
    config["WEDNESDAY"] = {
        "Start Minute": 0,
        "Uptime": 1440
    }
    config["THURSDAY"] = {
        "Start Minute": 0,
        "Uptime": 1440
    }
    config["FRIDAY"] = {
        "Start Minute": 0,
        "Uptime": 1440
    }
    config["SATURDAY"] = {
        "Start Minute": 0,
        "Uptime": 1440
    }
    config["SUNDAY"] = {
        "Start Minute": 0,
        "Uptime": 1440
    }

    with open(f"{main.parentdir}/config.ini", "w") as configfile:
        config.write(configfile)

def execute_startup(server):
    while True:
        if server.get_server().status != "Online":
            try:
                server.start()
                break
            except:
                continue

def execute_shutdown(server):
    while True:
        if server.get_server().status != "Offline":
            try:
                server.stop()
                break
            except:
                continue
        
def send_server_command(server, command):
    while True:
        try:
            server.command(command)
            break
        except:
            continue
        
def get_server_status(server):
    while True:
        try:
            return server.get_server().status
        except:
            continue
        
def time_in_minutes():
    # Make sure the inputted value does not go out of bounds
    return time.localtime().tm_hour * 60 + time.localtime().tm_min
    
def parse_string(string, target, replacement):
    return string.replace(target, replacement)
    
def generate_chat_log(server):
    pass