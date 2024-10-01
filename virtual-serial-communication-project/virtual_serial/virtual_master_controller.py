import time
import math
import serial
import threading
import random
from pynput import keyboard

MAX_RACK_NUMBER=6
MAX_TEMPERATURE=22
MIN_TEMPERATURE=20
MAX_HUMIDITY=80
MIN_HUMIDITY=40


RACK_MOVEMENT_SPEED = 4.0
RACK_MAX_MOVEMENT_SPEED = 15
RACK_WEIGHT = 80.0
RACK_MAX_DISPLACEMENT = 64.0

MASTER_CONTROLLER_IDLE_STATE = 'master_controller_idle_state'
MASTER_CONTROLLER_ENV_STATE = 'master_controller_env_state'
MASTER_CONTROLLER_OPR_STATE = 'master_controller_operation_state'
MASTER_CONTROLLER_BRKDOWN_STATE = 'master_controller_breakDown_state'


class MasterCom:
    def __init__(self, rack_group_id=0, port='COM1', baudrate=9600, timeout=None):
        self.rack_group_id = rack_group_id
        # cấu hình cho kết nối
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        # đặt tên biến trạng thái ban đầu khi chưa thực thi câu lệnh
        self.is_run = False
        self.is_rack_operation = False
        self.is_error = False
        self.is_reading = False

        self.state = MASTER_CONTROLLER_IDLE_STATE
        self.rack_group_state = -1
        self.listen = keyboard.Listener
        self.current_keys = []
        self.error_racks = [[] for i in range(MAX_RACK_NUMBER)]
        self.ventilating_racks_status = [[0.0, 0.0] for i in range(MAX_RACK_NUMBER)]

        self.ventilating_racks = []
        self.opening_racks = []
        self.closing_racks = []
        self.env_messages = ['0|0|0|0|0|0']
        self.opr_messages = ['0|0|0|0|0|0|-1']
        self.brk_messages = ['0|0|0|0|0']

    # def __init_serial(self):
    #     if self.ser is None:
    #         self.ser = serial.Serial(timeout=self.timeout)
    #     if self.ser.is_open:
    #         self.ser.close()
    #     self.ser.baudrate = self.baudrate
    #     self.ser.port = self.port
    #     self.ser.open()

    def start(self):
        # khởi động serial
        if self.ser is None:
            self.ser = serial.Serial(timeout=self.timeout)
        if self.ser.is_open:
            self.ser.close()
        self.ser.baudrate = self.baudrate
        self.ser.port = self.port   #đây là khi tạo dữ liệu và gửi đi từ com3 và com3 nhận luôn

        #còn đây là khi tạo dữ liệu và gửi đi từ com3 và com1 nhận
        #self.ser.port = 'COM1'
        self.ser.open()

        self.is_run = True
        self.is_reading = True

    def run_masterControllerEnvState(self, sleep_time):
        while self.is_run:
            self.state = MASTER_CONTROLLER_ENV_STATE
            print(f'state: {self.state}')
            self.create_environmentStatusData(rack_group_id=self.rack_group_id)

            # The is_run flag to break while loop (run_masterControllerEnvState thread)
            if not self.is_run:
                break
            time.sleep(sleep_time)
            self.state = MASTER_CONTROLLER_IDLE_STATE

            if not self.is_run:
                break

    #        if self.listen:
    #            self.listen.stop()

    def create_environmentStatusData(self, rack_group_id=0):
        #rack_group_id của def này là biến index của file main
        self.env_messages = []
        print('[PORT]', self.port)
        for rack_id in range(rack_group_id * 6, rack_group_id * 6 + MAX_RACK_NUMBER):
            random_parameter = random.random()
            temperature = random_parameter * (MAX_TEMPERATURE - MIN_TEMPERATURE) + MIN_TEMPERATURE
            humidity = random_parameter * (MAX_HUMIDITY - MIN_HUMIDITY) + MIN_HUMIDITY
            # weight = random_parameter * 1.8 * math.pow(-1, math.floor(random_parameter * 10)) + RACK_WEIGHT
            weight = random_parameter * 1.8 * -1 + RACK_WEIGHT
            smoke = 1
            message = 'ENVSTT|'+str(rack_id+1) + '|' + str(temperature) + '|' + str(humidity) + '|' + str(weight) + '|' + str(smoke)
            print(message + "anh long dep trai")
            self.env_messages.append(message)
            self.ser.write((message + '\n').encode('utf-8'))

    def create_movement_speed_number(self, rack_id, random_parameter, settling_time = 1.5) -> float:
        porportional_parameter = RACK_MAX_MOVEMENT_SPEED / settling_time
        time_interval = 1
        if self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] <= 3.2:
            movement_speed = random_parameter * math.pow(-0.4, round(random_parameter * 10)) + porportional_parameter * time_interval / 3
            return movement_speed
        elif self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] < 15:
            movement_speed = random_parameter * math.pow(-0.4, round(random_parameter * 10)) + porportional_parameter * 0.4 + 0.6 * RACK_MAX_MOVEMENT_SPEED
            return movement_speed
        elif self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] < 47:
            movement_speed = random_parameter * math.pow(-0.4, round(random_parameter * 10)) + RACK_MAX_MOVEMENT_SPEED
            return movement_speed
        elif self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] < 59.4:
            movement_speed = random_parameter * math.pow(-0.4, round(random_parameter * 10)) + porportional_parameter * (-1) * 0.25 + RACK_MAX_MOVEMENT_SPEED
            return movement_speed
        movement_speed = random_parameter * math.pow(-0.4, round(random_parameter * 10)) + porportional_parameter * (-1) * time_interval + RACK_MAX_MOVEMENT_SPEED
        return movement_speed

        

    def create_operation_ventilateStatusData(self, rack_id):
        self.opr_messages = []
        operation_message = 'OPRSTT|' + str(rack_id+1)
        random_parameter = random.random()
        movement_speed = self.create_movement_speed_number(rack_id=rack_id, random_parameter=random_parameter)
        is_hard_locked = 0
        displacement = self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] + movement_speed * 1
        is_endpoint = 0

        if self.rack_group_state == -1 and self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][1] == 1:
            print("[DIRECTION]", self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][1])
            self.ventilating_racks.remove(rack_id + 1)
            self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][1] = 0
            displacement = 0
            movement_speed = 0

            if not self.ventilating_racks:
                # set the is_rack_operation flag to False
                self.is_rack_operation = False

        if displacement > 2 and displacement < 50 and self.rack_group_state == -1:
            self.rack_group_state = 3

        if self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][1] == 1:
            displacement = self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] - movement_speed * 1
        
        if displacement > RACK_MAX_DISPLACEMENT:
            displacement = RACK_MAX_DISPLACEMENT
            self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][1] = 1
        if displacement <= 0:
            is_endpoint = 1
            displacement = 0.0
            self.rack_group_state = -1

        self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] = displacement
        
        operation_message += '|' + str(movement_speed) + '|' + str(displacement) + '|' + str(is_hard_locked) + '|' + str(is_endpoint) + '|' + str(self.rack_group_state)
        self.opr_messages.append(operation_message)

        return operation_message

    def create_operation_open_rack_statusData(self, rack_id):
        self.opr_messages = []
        operation_message = 'OPRSTT|' + str(rack_id+1)
        random_parameter = random.random()
        print('[RANDOM PARAMS]', random_parameter)
        movement_speed = self.create_movement_speed_number(rack_id=rack_id, random_parameter=random_parameter)
        is_hard_locked = 0
        displacement = self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] + movement_speed * 1
        is_endpoint = 0
        if displacement > 0 and displacement < 50 and self.rack_group_state == -1:
            self.rack_group_state = 1
#######################################################################
        # đoạn code này là để dừng(stop) gửi thông điệp tới virtual_ipc hãy tự đọc và hiểu nó
        if self.rack_group_state == -1 and displacement > 50:
            self.opening_racks.remove(rack_id + 1)
            movement_speed = 0

            if not self.opening_racks:
                # set the is_rack_operation flag to False
                self.is_rack_operation = False
###########################################################################
        if displacement > RACK_MAX_DISPLACEMENT:
            displacement = RACK_MAX_DISPLACEMENT
            self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][1] = 1
            is_endpoint = 1
            self.rack_group_state = -1

        self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] = displacement
#        print('[DISPLACEMENT]', self.ventilating_racks_status[rack_id][0])
        
        operation_message += '|' + str(movement_speed) + '|' + str(displacement) + '|' + str(is_hard_locked) + '|' + str(is_endpoint) + '|' + str(self.rack_group_state)
        self.opr_messages.append(operation_message)

        return operation_message

    def create_operation_close_rack_statusData(self, rack_id):
        self.opr_messages = []
        operation_message = 'OPRSTT|' + str(rack_id+1)
        random_parameter = random.random()
        movement_speed = self.create_movement_speed_number(rack_id=rack_id, random_parameter=random_parameter)
        is_hard_locked = 0
        is_endpoint = 0
        displacement = self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] - movement_speed * 1

        if displacement > 0 and displacement < 62 and self.rack_group_state == -1:
            self.rack_group_state = 2

        if self.rack_group_state == -1 and displacement < 1:
            self.closing_racks.remove(rack_id + 1)
            movement_speed = 0

            if not self.closing_racks:
                # set the is_rack_operation flag to False
                self.is_rack_operation = False
        
        if displacement <= 0:
            self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][1] = 0
            is_endpoint = 1
            displacement = 0.0
            self.rack_group_state = -1

        self.ventilating_racks_status[rack_id - self.rack_group_id * MAX_RACK_NUMBER][0] = displacement
        
        operation_message += '|' + str(movement_speed) + '|' + str(displacement) + '|' + str(is_hard_locked) + '|' + str(is_endpoint) + '|' + str(self.rack_group_state)
        self.opr_messages.append(operation_message)

        return operation_message

    def create_breakdownStatusData(self, error_numbers, rack_id):
        error_message = 'BRKSTT|' + str(rack_id+1)
        self.brk_messages = []
        for number in range(1,4):
            if number in error_numbers:
                error_message += '|1'
            else:
                error_message += '|0'
        self.brk_messages.append(error_message)
        return error_message


    def read_line_from_computerIPC(self):
        while self.is_reading:
            print("Đang đọc đây ")
            # if not self.is_reading:
            #     break
            line = self.ser.readline().decode('utf-8').replace('\n', '')
            print("tin nhan là ",line)
            if line:

                print('[SERIAL IPC]', line)
                print(len(line))
                print( line[0])

                if len(line) > 4 :
                    print(line[-1])

                    if line[-1] != "0":
                        print(line[-1])
                        print("toang roi ong dao a")
                        self.determine_operationInformation(line)
                        self.is_rack_operation = True
                        opr_thread = threading.Thread(target=self.run_masterControllerOperationState, args=(1,))
                        opr_thread.start()
                        print("toang roi ong dao a")


            if not self.is_reading:
                print("thoi khong doc nua")
                break
#        self.listen.stop()


    def run_masterControllerOperationState(self, sleep_time):
        # Điều kiện để lặp là is_rack_operation nếu muốn dùng gửi chỉ cần cho nó giá trị fail
        # tại sao lại dùng hàm for:
        # có hai cách dùng
        # 1 là dùng để chạy gía trị từ thấp đến cao
        # 2 là dùng để kiểm tra xem có tồn tại giá trị idx trong hàm hay không

        while self.is_rack_operation:
            self.state = MASTER_CONTROLLER_OPR_STATE
            print(f'state: {self.state}')
            for idx in self.ventilating_racks:
                message = ''
                message += self.create_operation_ventilateStatusData(idx-1)
                print(message)
                print('[VENTILATING RACKS]', self.ventilating_racks)
                self.ser.write((message + '\n').encode('utf-8'))

            for idx in self.opening_racks:
                message = ''
                message += self.create_operation_open_rack_statusData(idx-1)
                print(message)
                print('[OPENING RACKS]', self.opening_racks)
                self.ser.write((message + '\n').encode('utf-8'))

            for idx in self.closing_racks:
                message = ''
                message += self.create_operation_close_rack_statusData(idx-1)
                print(message)
                print('[CLOSING RACKS]', self.closing_racks)
                self.ser.write((message + '\n').encode('utf-8'))
            # The is_rack_operation flag to break run_masterControllerOperationState thread
            if not self.is_rack_operation:
                break
            time.sleep(sleep_time)
            self.state = MASTER_CONTROLLER_IDLE_STATE

            if not self.is_rack_operation:
                break
        

    def run_masterControllerBreakdownState(self, sleep_time, rack_id = 1, error_numbers = [1]):
        while self.is_error:
            self.state = MASTER_CONTROLLER_BRKDOWN_STATE
            print(f'state: {self.state}')
            for error_number in error_numbers:
                self.error_racks[rack_id-1-self.rack_group_id * MAX_RACK_NUMBER].append(error_number)
            for idx, elements in enumerate(self.error_racks):
                message = ''
                if elements:
                    message += self.create_breakdownStatusData(elements, idx+self.rack_group_id * MAX_RACK_NUMBER)
                    print(message)
                    self.ser.write((message + '\n').encode('utf-8'))
            # The is_error flag to break run_masterControllerBreakdownState thread
            if not self.is_error:
                self.error_racks[rack_id-1-self.rack_group_id * MAX_RACK_NUMBER].clear()
                break
            time.sleep(sleep_time)
            self.state = MASTER_CONTROLLER_IDLE_STATE

            if not self.is_error:
                self.error_racks[rack_id-1-self.rack_group_id * MAX_RACK_NUMBER].clear()
                break

    def determine_errorInformation(self):
        if len(self.current_keys) == 3 and self.current_keys[0] == 69:
            self.error_racks[self.current_keys[1] - 49].append(self.current_keys[2] - 48)
            print(self.error_racks)
            self.current_keys = []

# kiểm tra xem có đúng mẫu tin nhắn điều khiển không và lấy số rack cần điều khiển trong rack group
    def determine_operationInformation(self, message):
        opr_message_list = []
        # if len(self.current_keys) == 2 and self.current_keys[0] == 79:
        #     self.ventilating_racks.append(self.current_keys[1] - 49)
        #     print(self.ventilating_racks)
        #     self.current_keys = []

        if len(message) > 4 and message[0] == "0" and message[-1]=="1":
            print( message)
            opr_message_list = message.split('|')
            self.opening_racks.append(int(opr_message_list[1]))
            # print('[OPENING RACKS]', self.opening_racks)
        if len(message) > 4 and message[0] == "0" and message[-1]=="2":
            print(message)
            opr_message_list = message.split('|')
            self.closing_racks.append(int(opr_message_list[1]))
            # print('[CLOSING RACKS]', self.closing_racks)
        if len(message) > 4 and message[0] == "0" and message[-1] == "3":
            print(message)
            opr_message_list = message.split('|')
            self.ventilating_racks.append(int(opr_message_list[1]))
            # print('[VENTILATING RACKS]', self.ventilating_racks)

    def execute_stopRunning(self):
        print('Stop running')
        self.is_run = False
        self.is_error = False
        self.is_reading = False
        self.ser.close()

#     def determine_shortcuts(self, vk):
#         if vk == 27:
#             self.execute_stopRunning()
#             return
# #        elif vk == 83:
# #
# #            self.current_keys = []
# #            # Environment thread
# #            env_thread = threading.Thread(target=self.run_masterControllerEnvState, daemon=True, args=(10,))
# #            env_thread.start()
#         elif vk == 69 and not self.is_error:
#             self.is_error = True
#
#             # Breakdown thread
#             brkdown_thread = threading.Thread(target=self.run_masterControllerBreakdownState, args=(6,))
#             brkdown_thread.start()
#
#         elif self.current_keys[0] == 69:
#             self.determine_errorInformation()
#         else:
#             self.current_keys = []

#        elif vk == 79 and not self.is_rack_operation:
#            self.is_rack_operation = True
#
#            # Operation status thread
#            opr_thread = threading.Thread(target=self.run_masterControllerOperationState, args=(4,))
#            opr_thread.start()
#
#        elif self.current_keys[0] == 79:
#            self.determine_operationInformation()

    # def on_press(self, key):
    #     vk = key.vk if hasattr(key, 'vk') else key.value.vk
    #     print('vk: ', vk)
    #     self.current_keys.append(vk)
    #     print('keys: ', self.current_keys)
    #     if vk == None:
    #         return
    #     self.determine_shortcuts(vk)

#     def run_masterController(self):
#         self.start()
#         print('Start controller successfully!!')
#
#         # Readline from ComputerIPC thread
#         env_thread = threading.Thread(target=self.run_masterControllerEnvState, daemon=True, args=(10,))
#         env_thread.start()
#
#         read_computerIPC_thread = threading.Thread(target=self.read_line_from_computerIPC, daemon=True)
#         read_computerIPC_thread.start()
#
#
#         with keyboard.Listener(on_press=self.on_press) as listener:
#             self.listen = listener
#             listener.join()
#
#
#
# if __name__ == '__main__':
#     HahaController = MasterCom()
#     HahaController.run_masterController()



