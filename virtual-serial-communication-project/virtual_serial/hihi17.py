from virtual_ipc import ComputerIPC

def main4():
    HihiController4 = ComputerIPC(port='COM34' , timeout=1, port_socket=5066)
    HihiController4.run_computerIPC()

if __name__ == '__main__':
    main4()
