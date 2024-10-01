from virtual_ipc import ComputerIPC

def main3():
    HihiController3 = ComputerIPC(port='COM28', timeout=1, port_socket=5063)
    HihiController3.run_computerIPC()

if __name__ == '__main__':
    main3()
