from virtual_ipc import ComputerIPC

def main3():
    HihiController3 = ComputerIPC(port='COM26', timeout=1, port_socket=5062)
    HihiController3.run_computerIPC()

if __name__ == '__main__':
    main3()
