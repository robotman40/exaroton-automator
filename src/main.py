# Required modules
import exaroton_expanded as ee
import configparser as cfgp
import os
import time
import ast

# Associated Modules
import exat_functions
import exat_data
import exat_class

# Global variables
parentdir = os.path.abspath(os.path.dirname(__file__))
config = cfgp.ConfigParser()
server = None

if __name__ == "__main__":
    # If the config file exist, read it. Otherwise, create one
    if not os.path.exists(f"{parentdir}/config.ini"):
        exat_functions.create_config(config)
        print(f"A configuration file has been created at '{parentdir}'. Please adjust it before continuing")
        input() # Wait for user to confirm
        exit()
    else:
        config.read(f"{parentdir}/config.ini")

    # Run this loop until it connects to the Exaroton API:
    while True:
        try:
            print("Connecting (make sure you have modified the config values)...")
            server = ee.ServerInstance(config["GENERAL"]["API Token"], config["GENERAL"]["SERVER ID"])
            break
        except:
            print("Retrying...")
            continue
        
    print("Connected")
    
    # Main program loop
    while True:
        # Time data
        time_data = time.localtime()
        # Variable that ensures the server does not start up again during the day
        ran_today = False
        
        if exat_functions.time_in_minutes() >= int(config[exat_data.day_index[time_data.tm_wday]]["Start Minute"]) and ran_today == False:
            exat_functions.execute_startup(server)
            
            # variables to ensure actions are not repeated
            last_action_check = -1
            last_shutdown_notice = -1
            
            # Wait for the server to start
            while exat_functions.get_server_status(server) != "Online":
                pass
            
            # Time Tracker
            time_tracker = exat_class.TimeTracker()
            
            while time_tracker.get_time_elapsed() < int(config[exat_data.day_index[time_data.tm_wday]]["Uptime"]):
                # Do periodic actions
                print(f"Server uptime: {time_tracker.get_time_elapsed()}")
                if exat_functions.time_in_minutes() != last_action_check:
                    for action in ast.literal_eval(config["GENERAL"]["Periodic Actions"]):
                        action = tuple(action)
                        if exat_functions.time_in_minutes() % int(action[0]) == 0:
                            exat_functions.send_server_command(server, str(action[1]))
                    last_action_check = exat_functions.time_in_minutes()
                # Shutdown notices
                if time_tracker.get_time_elapsed() >= (int(config[exat_data.day_index[time_data.tm_wday]]["Uptime"]) - int(config["GENERAL"]["Shutdown Notice Time"])) and exat_functions.time_in_minutes() != last_shutdown_notice:
                    if exat_functions.time_in_minutes() % int(config["GENERAL"]["Notify Shutdown Every"]) == 0:
                        exat_functions.send_server_command(
                            server, 
                            exat_functions.parse_string(
                                "/say " + str(config["GENERAL"]["Shutdown Warning"]), 
                                "{time}", 
                                str(int(config[exat_data.day_index[time_data.tm_wday]]["Uptime"]) - int(time_tracker.get_time_elapsed()))
                            )
                        )
                    last_shutdown_notice = exat_functions.time_in_minutes()
                    
            exat_functions.execute_shutdown(server)
            
            # Wait for the server to fully shut down to collect logs if configured to
            while exat_functions.get_server_status(server) != "Offline":
                pass
            
            ran_today = True
            # More to come
