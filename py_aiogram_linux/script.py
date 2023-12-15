# pip install psutil


import psutil

def main():
    # Отримуємо інформацію про оперативну пам'ять
    memory = psutil.virtual_memory()

    # Виводимо інформацію про оперативну пам'ять
    print(f"Загальний обсяг оперативної пам'яті: {memory.total / (1024 ** 3):.2f} GB")
    print(f"Використано оперативної пам'яті: {memory.used / (1024 ** 3):.2f} GB")
    print(f"Залишилось оперативної пам'яті: {memory.available / (1024 ** 3):.2f} GB")


def get_ram():
    # Get info about RAM
    memory = psutil.virtual_memory()

    total = memory.total
    available = memory.available
    result = int(round((available / total) * 100, 0))

    # print(f"{result}%")

    return result

def get_ram_metrics():
    # Get info about RAM
    memory = psutil.virtual_memory()

    total = memory.total
    available = memory.available
    used = memory.used

    return total, available, used

def get_hdd():

    space = psutil.disk_usage('/')

    total = space.total
    used = space.used
    free = space.free
    result = int(round((free / total) * 100, 0))

    # print(f"{result}%")

    return result

def get_hdd_metrics():
    # Get info about RAM
    memory = psutil.disk_usage('/')

    total = memory.total
    used = memory.used
    available = memory.free

    return total, available, used

if __name__ == "__main__":
    main()