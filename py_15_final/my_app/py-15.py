import sys
import time
from my_functions import *

logging.info("Program Started")
currnet_ip = get_current_ip()
server_status = check_if_server_already_exist(currnet_ip)

if server_status != "server_already_exist":
    metadata = get_metadata()
    print(f"metadata is {metadata}")
    register_server(metadata["currnet_ip"], metadata["hostname"], metadata["description"])
else:
    print(f"{server_status}")

try:
    print("Press CTRL+C to stop programm")
    while True:
        send_totalinfo(get_totalinfo())
        time.sleep(60)
except KeyboardInterrupt:
    print('interrupted!')
    sys.exit(0)
    