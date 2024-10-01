from virtual_ipc import ComputerIPC

def main3():
    HihiController3 = ComputerIPC(port='COM30', timeout=1, port_socket=5064)
    HihiController3.run_computerIPC()

if __name__ == '__main__':
    main3()
