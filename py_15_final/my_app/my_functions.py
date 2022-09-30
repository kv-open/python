import requests
import os
import logging
import socket
import psutil
import json

logging.basicConfig(filename='./log_file.log', format='%(asctime)s - %(levelname)s - %(message)s - %(funcName)s', datefmt="%Y-%m-%dT%H:%M:%S%z", level=logging.INFO, encoding="UTF-8")
server_address = "http://127.0.0.1:8000"


def get_current_ip():
    try:
        currnet_ip = requests.get('https://ifconfig.me/ip').text
        logging.info("got external ip")
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Failed to establish a new connection. Stack trace is: {e}")
        print("ConnectionError:")
        raise SystemExit()
    except requests.exceptions.Timeout as e:
        print("Timeout Error. Stack trace is: {e}")
        logging.error(f"Timeout Error. Stack trace is: {e}")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Http Error. Stack trace is: {e}")
        print("Http Error:")
    except requests.exceptions.RequestException as e:
        logging.error(f"OOps: Something Else. Stack trace is: {e}")
        print("OOps: Something Else")
    return currnet_ip


def check_if_server_already_exist(currnet_ip):
    try:
        r = requests.get(server_address + "/api/servers/")
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Failed to establish a new connection. Stack trace is: {e}")
        print("ConnectionError:")
        raise SystemExit()
    except requests.exceptions.Timeout as e:
        print("Timeout Error. Stack trace is: {e}")
        logging.error(f"Timeout Error. Stack trace is: {e}")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Http Error. Stack trace is: {e}")
        print("Http Error:")
    except requests.exceptions.RequestException as e:
        logging.error(f"OOps: Something Else. Stack trace is: {e}")
        print("OOps: Something Else")
    list_of_registered_ip_address = [element['ip_address'] for element in r.json()]
    if currnet_ip in list_of_registered_ip_address:
        message = "server_already_exist"
        logging.info("server_already_exist")
    else:
        message = "server_doesnt_exist"
        logging.info("server_doesnt_exist")
    return message


def get_metadata():
    currnet_ip = requests.get('https://ifconfig.me/ip').text
    hostname = os.environ['COMPUTERNAME']
    if "DESC" in os.environ:
        description = os.environ['DESC']
        logging.info("ENV 'DESC' found.")
    else:
        logging.info("ENV 'DESC' doesnt exist. Use default value")
        print("ENV 'DESC' doesnt exist. Use default value")
        description = "no_description"
    metadata = {"currnet_ip": currnet_ip, "hostname": hostname, "description": description}
    logging.info(f"{metadata}")
    return metadata


def register_server(currnet_ip, hostname, description, server_active = False):
    metadata = {
    "ip_address": currnet_ip,
    "description": description,
    "name": hostname,
    "server_active": server_active
    }
    try:
        requests.post(server_address + "/api/servers/add", data = metadata)
        print("server was successful registered")
        logging.info("server was successful registered")
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Failed to establish a new connection. Stack trace is: {e}")
        print("ConnectionError:")
        raise SystemExit()
    except requests.exceptions.Timeout as e:
        print("Timeout Error. Stack trace is: {e}")
        logging.error(f"Timeout Error. Stack trace is: {e}")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Http Error. Stack trace is: {e}")
        print("Http Error:")
    except requests.exceptions.RequestException as e:
        logging.error(f"OOps: Something Else. Stack trace is: {e}")
        print("OOps: Something Else")


def get_systeminfo():
    if os.name == 'nt':
        sysname = os.name
    else:
        sysname = os.uname().sysname
    hostname = socket.gethostname()
    systeminfo = {"host_information": {"sysname": sysname, "hostname": hostname}}
    logging.debug(f"get_systeminfo is: {systeminfo}")
    return systeminfo


def get_networkinfo():
    net_adapters_info = []
    for name in list(psutil.net_if_stats()):
        interface_status = str(psutil.net_if_stats()[name][0]).encode("UTF-8")
        if interface_status == True:
            interface_status = "up"
        else:
            interface_status = "down"
        speed = psutil.net_if_stats()[name][2]
        mtu = psutil.net_if_stats()[name][3]
        dict = {"name": name,"interface_status": interface_status, "speed": speed, "mtu": mtu}
        net_adapters_info.append(dict)
    data = {"network": net_adapters_info}
    logging.debug(f"get_networkinfo is: {data}")
    return data


def get_memoryinfo():
    mem = psutil.virtual_memory()
    mem_info = {"memory": {"memory_total": mem.total,"memory_used": mem.used, "memory_percent": mem.percent}}
    logging.debug(f"get_memoryinfo is: {mem_info}")
    return mem_info


def get_diskinfo():
    disks_names = [] # name of disks
    disk_info = []   # list of dic with disk info
    for disk in list(psutil.disk_partitions()):
        disks_names.append(disk)

    i = 0
    for i in range(len(disks_names)):
        disk_name = disks_names[i][0]
        disk_total_space = psutil.disk_usage(disk_name).total
        disk_used_space = psutil.disk_usage(disk_name).used
        disk_used_percent = psutil.disk_usage(disk_name).percent
        mountpoint = disks_names[i][1]
        fstype =  disks_names[i][2]
        dict ={"disk_name": disk_name, "mountpoint": mountpoint, "fstype": fstype,"disk_total_space": disk_total_space, "disk_used_space": disk_used_space, "disk_used_percent": disk_used_percent}
        disk_info.append(dict)
    data = {"disks": disk_info}
    logging.debug(f"get_diskinfo is: {data}")
    return data


def get_loadaverage():
    lv = psutil.getloadavg()
    data = {"load_average": {"lv_1m": lv[0],"lv_5m": lv[1],"lv_15m": lv[2]}}
    logging.debug(f"get_loadaverage is: {data}")
    return data


def get_totalinfo():
    temp_data = get_systeminfo()
    temp_data.update(get_memoryinfo())
    temp_data.update(get_networkinfo())
    temp_data.update(get_diskinfo())
    temp_data.update(get_diskinfo())
    temp_data.update(get_loadaverage())
    logging.debug(f"temp_data is: {temp_data}")
    data = {"totalinfo": temp_data}
    data = json.dumps(data)
    logging.info(f"get_totalinfo is: {data}")
    return data

def send_totalinfo(my_dict):
    try:
        my_dict = str(my_dict).encode("UTF-8")
        headers = {'Content-type': 'application/json; charset=UTF-8'}
        r = requests.post(server_address + "/api/servers/totalinfo", data = my_dict, headers=headers)
        if r.status_code < 200 or r.status_code > 300:
            print(f"totalinfo was not sent error code is: {r.status_code} {r.text}")
            logging.error(f"totalinfo was not sent. error code is: {r.status_code} error message is: {r.text}\n data is {my_dict}")
            r.raise_for_status()
        else:
            print("totalinfo was sent")
            logging.info("totalinfo was sent")
            logging.debug(my_dict)
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Failed to establish a new connection. Stack trace is: {e}")
        print("ConnectionError:")
        raise SystemExit()
    except requests.exceptions.Timeout as e:
        print("Timeout Error. Stack trace is: {e}")
        logging.error(f"Timeout Error. Stack trace is: {e}")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Http Error. Stack trace is: {e}")
        print("Http Error:")
    except requests.exceptions.RequestException as e:
        logging.error(f"OOps: Something Else. Stack trace is: {e}")
        print("OOps: Something Else")