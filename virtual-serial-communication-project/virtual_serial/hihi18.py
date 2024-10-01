from virtual_ipc import ComputerIPC

def main4():
    HihiController4 = ComputerIPC(port='COM36' , timeout=1, port_socket=5067)
    HihiController4.run_computerIPC()

if __name__ == '__main__':
    main4()
