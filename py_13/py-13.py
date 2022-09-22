import os
import psutil
import sys
from my_exception import *

class PC_memory:
    """Описание Памяти PC"""
    def __init__(self, pc_id, user_name, memory_total, memory_used, memory_percent = (psutil.virtual_memory().used * 100) / psutil.virtual_memory().total):
        self.memory_total_default = 100000000000 # 100Gb
        self.memory_used_default = 0

        self.pc_id = pc_id
        self.user_name = user_name
        
        
        try:
            self.memory_total = memory_total
            if memory_total < 0:
                raise ValueError
        except ValueError:
            print(f'Wrong value: "{memory_total}" memory_total can not be less than 0, default value {self.memory_total_default} will be used')
            self.memory_total = self.memory_total_default

        try:
            self.memory_used = memory_used
            if type(memory_used) is str:
                raise TypeError
            else:
                self.memory_used = int(memory_used) 
            if memory_used < 0:
                raise ValueError
            if memory_used > memory_total:
                raise ValueError
        except TypeError:
            print(f'wrong memory value, memory_used can not be a string\ndefault value {self.memory_used_default} will be used')
            self.memory_used = self.memory_used_default
        except ValueError:
            print(f'Wrong value: "{memory_used}" memory_used can not be greather than memory_total or less than 0, default value {self.memory_used_default} will be used')
            self.memory_used = self.memory_used_default
        
        
        try:
            self.memory_percent = memory_percent
            if type(memory_percent) is str:
                raise TypeError
            if type(memory_percent) is not float:
                self.memory_percent = float(memory_percent)
            if memory_percent < 0 or memory_percent > 100:
                raise PercentError("Percent value must be between 0 and 100")
        except TypeError:
            print(f'wrong percent value, value calculated automatically')
            self.memory_percent = self.memory_used * 100 / self.memory_total

    def show_used_percent(self):
        message = "PC with id " + self.pc_id + "used " +  str(self.memory_percent) + " percent of memory"
        return message
    def is_enough_memory(self):
        if self.memory_percent < 10 or psutil.virtual_memory().free < 1024 * 1024 * 1024:
            return False
        else:
            return True

# тест для отрецательное значение памяти и memory_used > memory_total
mypc = PC_memory(pc_id = os.environ['COMPUTERNAME'], user_name = os.getlogin(), memory_total = -22, memory_used = 11.111, memory_percent = 30)
print(f'memory_total is {mypc.memory_total}')
print(f'memory_used is {mypc.memory_used}')
print(f'memory_percent is {mypc.memory_percent}')

# тест для memory_used > memory_total и memory_percent строка
mypc2 = PC_memory(pc_id = os.environ['COMPUTERNAME'], user_name = os.getlogin(), memory_total = 100, memory_used = 200, memory_percent = "str")
print(f'memory_total is {mypc2.memory_total}')
print(f'memory_used is {mypc2.memory_used}')
print(f'memory_percent is {mypc2.memory_percent}')


