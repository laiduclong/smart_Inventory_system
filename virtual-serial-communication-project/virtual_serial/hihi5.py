from virtual_ipc import ComputerIPC

def main():
    HihiController = ComputerIPC(port='COM10', timeout=1, port_socket=5054)
    HihiController.run_computerIPC()

if __name__ == '__main__':
    main()
