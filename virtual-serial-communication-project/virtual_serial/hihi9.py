from virtual_ipc import ComputerIPC

def main2():
    HihiController1 = ComputerIPC(port='COM18', timeout=1, port_socket=5058)
    HihiController1.run_computerIPC()

if __name__ == '__main__':
    main2()

