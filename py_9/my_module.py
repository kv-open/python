import os
import psutil


def mem_info(scale_size):
    if scale_size not in ['', 'k', 'm', 'g']:
        help = """
        usage: mem_info()
        default bytes
        mem_info("k"|"m"|"g")
            k for kilobytes
            m for megabytes
            g for gigabytes
        """
        print(help)
    user_name = os.getlogin()
    mem = psutil.virtual_memory()
    memory_total = mem.total
    memory_used = mem.used
    memory_percent = mem.percent
    if scale_size == 'k':
        memory_total = int(mem.total) / 1024
        memory_used = int(mem.used) / 1024
    elif scale_size == 'm':
        memory_total = int(mem.total) / 1024 / 1024
        memory_used = int(mem.used) / 1024 / 1024
    elif scale_size == 'g':
        memory_total = int(mem.total) / 1024 / 1024 / 1024
        memory_used = int(mem.used) / 1024 / 1024 / 1024
    stat = {"user_name": user_name, "memory_total": memory_total, "memory_used": memory_used, "memory_percent": memory_percent}
    return stat




