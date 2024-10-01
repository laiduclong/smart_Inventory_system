from pickle import ADDITEMS
import serial
import threading
import socket
from pynput import keyboard
import datetime
from simulator_database import database_cursor, db

HEADER = 64
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT_STRING = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

class ComputerIPC:
    def __init__(self, port='COM1', baudrate=9600, timeout=None, port_socket=5051):
        self.ser = None
        self.server = None
        self.port = port
        self.port_socket = port_socket
        self.address_socket = (SERVER, self.port_socket)
        self.baudrate = baudrate
        self.timeout = timeout
        self.is_running_server = False
        self.is_run = False
        self.current_keys=[]
        self.listen = keyboard.Listener

    def __init_server(self):
        if self.server is None:
            print("hihi server")
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.address_socket)
            print(ADDRESS)

    def __init_serial(self):
        if self.ser is None:
            print("hihi server")
            self.ser = serial.Serial(timeout=self.timeout)
        if self.ser.is_open:
            self.ser.close()
        self.ser.baudrate = self.baudrate
        self.ser.port = self.port
        self.ser.open()

    def handle_client_message(self, conn, address):
        print(f"[CLIENT] {address} connected")

        msg_length = conn.recv(HEADER).decode(FORMAT_STRING)
        print(msg_length)
        if msg_length:
            msg_length = int(msg_length)
            message = conn.recv(msg_length).decode(FORMAT_STRING)
            self.ser.write((message + '\n').encode(FORMAT_STRING))
            if message == DISCONNECT_MESSAGE:
                print(DISCONNECT_MESSAGE)
            print(f"[{address}] {message}")

        conn.close()
    
    def server_listening(self):
        while self.is_running_server:
            conn, address = self.server.accept()
            self.handle_client_message(conn, address)
            if not self.is_running_server:
                break
        self.listen.stop()

    def start(self):
        self.__init_serial()
        self.is_running_server = True 
        self.__init_server()
        self.is_run = True

    def insert_history_status_table(self, rack_id: int):
        created_at = datetime.datetime.now()
        action = f"bạn đang mượn sách: {rack_id}"
        database_cursor.execute("INSERT INTO api_history (rack_id,action,created_at) VALUES (%s,%s,%s)", (rack_id,action,created_at))
        db.commit()
        print('[DATABASE] Insert into history successfully')
    def insert_environment_status_table(self, rack_id: int, temperature: float, humidity: float, weight: float, smoke: float,
                                        active=True):
        created_at = datetime.datetime.now()
        database_cursor.execute("INSERT INTO api_environmentstatus (rack_id, temperature, humidity, weight, smoke,created_at,active) VALUES (%s, %s, %s, %s, %s,%s,%s)", (rack_id, temperature, humidity, weight, smoke,created_at,active))
        db.commit()
        print('[DATABASE] Insert into environmentstatus successfully')

    def insert_operation_status_table(self, rack_id: int, movement_speed: float, displacement: float,
                                      is_hard_locked: bool, is_endpoint: bool,active = True):
        created_at = datetime.datetime.now()
        number_users = 0
        database_cursor.execute(
            "INSERT INTO api_operationstatus (rack_id, movement_speed, displacement, is_hard_locked, is_endpoint, created_at, number_users, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (rack_id, movement_speed, displacement, is_hard_locked, is_endpoint, created_at, number_users, active))
        db.commit()
        print('[DATABASE] Insert into operationstatus successfully')

    def insert_breakdown_status_table(self, rack_id: int, is_obstructed, is_skewed, is_overload_motor,active = True):
        current_time = datetime.datetime.now()
        database_cursor.execute(
            "INSERT INTO api_breakdownstatus (rack_id, is_obstructed, is_skewed, is_overload_motor, created_at, active) VALUES (%s, %s, %s, %s, %s, %s)",
            (rack_id, is_obstructed, is_skewed, is_overload_motor, current_time, active))
        db.commit()
        print('[DATABASE] Insert into breakdownstatus successfully')

    def handle_message_from_serial(self, message):
        env_list = []
        opr_list = []
        brkdown_list = []

        if 'ENVSTT' in message:
            print(message)
            env_list = message.split('|')[1:]
            rack_id, temperature, humidity, weight, smoke = int(env_list[0]), round(float(env_list[1]), 3), round(float(env_list[2]),3), round(float(env_list[3]), 3), round(float(env_list[4]), 3)

            self.insert_environment_status_table(rack_id=rack_id, temperature=temperature, humidity=humidity, weight=weight, smoke=smoke)
            return

        elif 'OPRSTT' in message:
            opr_list = message.split('|')[1:]
            rack_id, movement_speed, displacement, is_hard_locked, is_endpoint = int(opr_list[0]), round(float(opr_list[1]), 3), round(float(opr_list[2]),3), int(opr_list[3]), int(opr_list[4])

            self.insert_operation_status_table(rack_id=rack_id, movement_speed=movement_speed, displacement=displacement, is_hard_locked=is_hard_locked, is_endpoint=is_endpoint)
            self.insert_history_status_table(rack_id=rack_id)
            return

        elif 'BRKSTT' in message:
            brkdown_list = message.split('|')[1:]
            rack_id, is_obstructed, is_skewed, is_overload_motor = int(brkdown_list[0]), int(brkdown_list[1]), int(brkdown_list[2]), int(brkdown_list[3])

            self.insert_breakdown_status_table(rack_id=rack_id, is_obstructed=is_obstructed, is_skewed=is_skewed, is_overload_motor=is_overload_motor)
            return
 
    def read_serial(self):
        while self.is_run:
            line = self.ser.readline().decode('utf-8').replace('\n','')
            if line:
                print('[SERIAL]   Receive serial message successfully')
                self.handle_message_from_serial(line)

            if not self.is_run:
                break
        self.listen.stop()



    def execute_stopRunning(self):
        print('Stop running')
        self.is_run = False
        self.is_running_server = False

    
    def send_operationMessage(self):
        if self.current_keys[0] == 79 and len(self.current_keys) > 1:
            if self.current_keys[1] < 58 and len(self.current_keys) == 3:
                message = '0|' + str(self.current_keys[1] - 48) + '|' + str(self.current_keys[2] - 48)
                self.ser.write((message + '\n').encode(FORMAT_STRING))
                print('[SENT MESSAGE]', message)
                self.current_keys = []
#            elif self.current_keys[1] == 51 and len(self.current_keys) == 2:
#                message = 'O|' + str(self.current_keys[1] - 48)
#                self.ser.write((message + '\n').encode('utf-8'))
#                self.current_keys = []

    # def send_operationMessage_from_server(self, message):
    #     self.ser.write((message + '\n').encode('utf-8'))


    def determine_shortcuts(self, vk):
        if vk == 27:
            self.execute_stopRunning()
            return
#        elif vk == 69 and not self.is_error:
#            self.is_error = True
#
#            # Breakdown thread
#            brkdown_thread = threading.Thread(target=self.run_masterControllerBreakdownState, args=(6,))
#            brkdown_thread.start()
#
#        elif self.current_keys[0] == 69:
#            self.determine_errorInformation()
#
#        elif vk == 79:
#
#            # Send operation message thread
#            send_opr_message_thread = threading.Thread(target=self.send_operationMessage, args=())
#            send_opr_message_thread.start()

        elif self.current_keys[0] == 79:
            self.send_operationMessage()
        else:
            self.current_keys = []


    def on_press(self, key):
        vk = key.vk if hasattr(key, 'vk') else key.value.vk
        print('vk: ', vk)
        self.current_keys.append(vk)
        print('keys: ', self.current_keys)
        if vk == None:
            return
        self.determine_shortcuts(vk)


    def run_computerIPC(self):
        self.start()
        print('Start computer successfully!!')

        if self.server:
            self.server.listen()
            print("[LISTENING] Server  is listening")

        # Server listening thread
        server_listening_thread = threading.Thread(target=self.server_listening, args=(), daemon=True)
        server_listening_thread.start()
        print("oke")
        # Read serial thread
        read_serial_thread = threading.Thread(target=self.read_serial, args=(), daemon=True)
        read_serial_thread.start()
        print("oke 2")

#        with keyboard.Listener(on_press=self.on_press) as listener:
        self.listen = keyboard.Listener(on_press=self.on_press)
        self.listen.start()
        self.listen.join()

if __name__ == '__main__':
    HihiController = ComputerIPC(timeout=1)
    HihiController.run_computerIPC()
    # hihi_thread = threading.Thread(target=HihiController.run_computerIPC, args=(), daemon=True)
    # HihiController2 = ComputerIPC(port='COM4', timeout=1)
    # hihi2_thread = threading.Thread(target=HihiController2.run_computerIPC, args=(), daemon=True)
    # HihiController3 = ComputerIPC(port='COM6', timeout=1)
    # hihi3_thread = threading.Thread(target=HihiController3.run_computerIPC, args=(), daemon=True)
    # HihiController4 = ComputerIPC(port='COM8', timeout=1)
    # hihi4_thread = threading.Thread(target=HihiController4.run_o11o11puterIPC, args=(), daemon=True)
