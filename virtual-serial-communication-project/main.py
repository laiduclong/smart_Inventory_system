from PyQt6 import QtCore # type: ignore
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSignal
import time
from simulator_ui import Ui_MainWindow
from virtual_serial.virtual_master_controller import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow(1, 10, 0)
        self.uic.setupUi(self)

        self.rack_group = {}
        # self.uic.rackGroupList[0].runButton.clicked.connect(lambda: self.start_master_controller_fake)
        self.uic.rackGroupList[0].runButton.clicked.connect(lambda: self.start_master_controller(0))
        self.uic.rackGroupList[0].stopButton.clicked.connect(lambda: self.stop_master_controller(0))
        self.uic.rackGroupList[1].runButton.clicked.connect(lambda: self.start_master_controller(1))
        self.uic.rackGroupList[1].stopButton.clicked.connect(lambda: self.stop_master_controller(1))
        self.uic.rackGroupList[2].runButton.clicked.connect(lambda: self.start_master_controller(2))
        self.uic.rackGroupList[2].stopButton.clicked.connect(lambda: self.stop_master_controller(2))
        self.uic.rackGroupList[3].runButton.clicked.connect(lambda: self.start_master_controller(3))
        self.uic.rackGroupList[3].stopButton.clicked.connect(lambda: self.stop_master_controller(3))
        self.uic.rackGroupList[4].runButton.clicked.connect(lambda: self.start_master_controller(4))
        self.uic.rackGroupList[4].stopButton.clicked.connect(lambda: self.stop_master_controller(4))
        self.uic.rackGroupList[5].runButton.clicked.connect(lambda: self.start_master_controller(5))
        self.uic.rackGroupList[5].stopButton.clicked.connect(lambda: self.stop_master_controller(5))
        self.uic.rackGroupList[6].runButton.clicked.connect(lambda: self.start_master_controller(6))
        self.uic.rackGroupList[6].stopButton.clicked.connect(lambda: self.stop_master_controller(6))
        self.uic.rackGroupList[7].runButton.clicked.connect(lambda: self.start_master_controller(7))
        self.uic.rackGroupList[7].stopButton.clicked.connect(lambda: self.stop_master_controller(7))
        self.uic.rackGroupList[8].runButton.clicked.connect(lambda: self.start_master_controller(8))
        self.uic.rackGroupList[8].stopButton.clicked.connect(lambda: self.stop_master_controller(8))
        self.uic.rackGroupList[9].runButton.clicked.connect(lambda: self.start_master_controller(9))
        self.uic.rackGroupList[9].stopButton.clicked.connect(lambda: self.stop_master_controller(9))
        self.uic.rackGroupList[10].runButton.clicked.connect(lambda: self.start_master_controller(10))
        self.uic.rackGroupList[10].stopButton.clicked.connect(lambda: self.stop_master_controller(10))
        self.uic.rackGroupList[11].runButton.clicked.connect(lambda: self.start_master_controller(11))
        self.uic.rackGroupList[11].stopButton.clicked.connect(lambda: self.stop_master_controller(11))
        self.uic.rackGroupList[12].runButton.clicked.connect(lambda: self.start_master_controller(12))
        self.uic.rackGroupList[12].stopButton.clicked.connect(lambda: self.stop_master_controller(12))
        self.uic.rackGroupList[13].runButton.clicked.connect(lambda: self.start_master_controller(13))
        self.uic.rackGroupList[13].stopButton.clicked.connect(lambda: self.stop_master_controller(13))
        self.uic.rackGroupList[14].runButton.clicked.connect(lambda: self.start_master_controller(14))
        self.uic.rackGroupList[14].stopButton.clicked.connect(lambda: self.stop_master_controller(14))
        self.uic.rackGroupList[15].runButton.clicked.connect(lambda: self.start_master_controller(15))
        self.uic.rackGroupList[15].stopButton.clicked.connect(lambda: self.stop_master_controller(15))
        self.uic.rackGroupList[16].runButton.clicked.connect(lambda: self.start_master_controller(16))
        self.uic.rackGroupList[16].stopButton.clicked.connect(lambda: self.stop_master_controller(16))
        self.uic.rackGroupList[17].runButton.clicked.connect(lambda: self.start_master_controller(17))
        self.uic.rackGroupList[17].stopButton.clicked.connect(lambda: self.stop_master_controller(17))
        self.uic.rackGroupList[18].runButton.clicked.connect(lambda: self.start_master_controller(18))
        self.uic.rackGroupList[18].stopButton.clicked.connect(lambda: self.stop_master_controller(18))
        self.uic.rackGroupList[19].runButton.clicked.connect(lambda: self.start_master_controller(19))
        self.uic.rackGroupList[19].stopButton.clicked.connect(lambda: self.stop_master_controller(19))
        self.uic.rackGroupList[20].runButton.clicked.connect(lambda: self.start_master_controller(20))
        self.uic.rackGroupList[20].stopButton.clicked.connect(lambda: self.stop_master_controller(20))

        self.uic.rackGroupList[0].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(0))
        self.uic.rackGroupList[1].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(1))
        self.uic.rackGroupList[2].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(2))
        self.uic.rackGroupList[3].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(3))
        self.uic.rackGroupList[4].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(4))
        self.uic.rackGroupList[5].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(5))
        self.uic.rackGroupList[6].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(6))
        self.uic.rackGroupList[7].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(7))
        self.uic.rackGroupList[8].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(8))
        self.uic.rackGroupList[9].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(9))
        self.uic.rackGroupList[10].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(10))
        self.uic.rackGroupList[11].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(11))
        self.uic.rackGroupList[12].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(12))
        self.uic.rackGroupList[13].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(13))
        self.uic.rackGroupList[14].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(14))
        self.uic.rackGroupList[15].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(15))
        self.uic.rackGroupList[16].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(16))
        self.uic.rackGroupList[17].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(17))
        self.uic.rackGroupList[18].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(18))
        self.uic.rackGroupList[19].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(19))
        self.uic.rackGroupList[20].simulatorErrorButton.clicked.connect(lambda: self.start_simulate_error(20))


    # def start_master_controller_fake(self):
    #     for i in range(20):
    #
    #
    #          self.start_master_controller(i)
    def start_master_controller(self, index):
        self.rack_group[index]  =ThreadClass(index=index)
        self.rack_group[index].start()
        self.uic.rackGroupList[index].rackGroupStateLineEdit.setText("Ready!!!")
        self.rack_group[index].env_signal.connect(self.display_environment_status)
        self.rack_group[index].opr_signal.connect(self.display_operation_status)
        self.uic.rackGroupList[index].runButton.setEnabled(False)
        self.uic.rackGroupList[index].stopButton.setEnabled(True)

    def stop_master_controller(self, index):
        self.rack_group[index].stop()
        self.uic.rackGroupList[index].stopButton.setEnabled(False)
        self.uic.rackGroupList[index].runButton.setEnabled(True)

    def start_simulate_error(self, index):
        err_numbers = []
        
        if self.uic.rackGroupList[index].ObstructCheckBox.isChecked():
            err_numbers.append(1)
        if self.uic.rackGroupList[index].SkewCheckBox.isChecked():
            err_numbers.append(2)
        if self.uic.rackGroupList[index].OverloadMotorCheckBox.isChecked():
            err_numbers.append(3)

        if err_numbers:
            self.rack_group[index].err_numbers = err_numbers
            self.rack_group[index].rack_id = int(self.uic.rackGroupList[index].rackIDNumbersComboBox.currentText())

            self.rack_group[index].run_error()
            self.rack_group[index].brk_signal.connect(self.display_breakdown_status)
        else:
            self.uic.rackGroupList[index].rackGroupErrorLineEdit.setText("")
            self.rack_group[index].brk_signal.disconnect(self.display_breakdown_status)
            self.rack_group[index].stop_error()

    def handle_environment_status(self, message):
        env_list = message.split('|')
        temperature, humidity, weight, smoke = float(env_list[2]), float(env_list[3]), float(env_list[4]), int(env_list[5])
        return temperature, humidity, weight, smoke

    def handle_operation_status(self, message):
        opr_list = message.split('|')
        rack_id, movement_speed, displacement, is_hard_locked, is_endpoint, rack_group_state = int(opr_list[1]), float(opr_list[2]), float(opr_list[3]), int(opr_list[4]), int(opr_list[5]), int(opr_list[6])
        return rack_id, movement_speed, displacement, is_hard_locked, is_endpoint, rack_group_state

    def handle_breakdown_status(self, message):
        brk_list = message.split('|')
        rack_id, is_obstructed, is_skewed, is_overload_motor = int(brk_list[1]), int(brk_list[2]), int(brk_list[3]), int(brk_list[4])
        return rack_id, is_obstructed, is_skewed, is_overload_motor

    def display_rack_group_state(self, rack_id, rack_group_id, rack_group_state):
        if rack_group_state == 0:
            self.uic.rackGroupList[rack_group_id].rackGroupStateLineEdit.setText(f'Rack {rack_id}: Guiding Light...')
        elif rack_group_state == 1:
            self.uic.rackGroupList[rack_group_id].rackGroupStateLineEdit.setText(f'Rack {rack_id}: Opening...')
        elif rack_group_state == 2:
            self.uic.rackGroupList[rack_group_id].rackGroupStateLineEdit.setText(f'Rack {rack_id}: Closing...')
        elif rack_group_state == 3:
            self.uic.rackGroupList[rack_group_id].rackGroupStateLineEdit.setText('Ventilating...')
        elif rack_group_state == -1:
            self.uic.rackGroupList[rack_group_id].rackGroupStateLineEdit.setText('Ready!!!')

    def display_environment_status(self, message: str):
        index = self.sender().index
        print("Displaying env", index)
        if index != -1:
            temperature, humidity, weight, smoke = self.handle_environment_status(message)
            self.uic.rackGroupList[index].temperature.display('{:.02f}'.format(temperature))
            self.uic.rackGroupList[index].humidity.display('{:.02f}'.format(humidity))
            self.uic.rackGroupList[index].weight.display('{:.02f}'.format(weight))
            self.uic.rackGroupList[index].smoke.display(smoke)

    def display_operation_status(self, message: str):
        index = self.sender().index
        print("Displaying opr", index)
        if index != -1:
            rack_id, movement_speed, displacement, is_hard_locked, is_endpoint, rack_group_state = self.handle_operation_status(message)
            self.uic.rackGroupList[index].movementSpeed.display('{:.02f}'.format(movement_speed))
            self.uic.rackGroupList[index].displacement.display('{:.02f}'.format(displacement))
            self.uic.rackGroupList[index].isHardLock.display('{:.02f}'.format(is_hard_locked))
            self.uic.rackGroupList[index].isEndpoint.display(is_endpoint)
            self.display_rack_group_state(rack_id, index, rack_group_state)

    def display_breakdown_status(self, message: str):
        index = self.sender().index
        print("Displaying error", index)
        if index != -1:
            rack_id, is_obstructed, is_skewed, is_overload_motor = self.handle_breakdown_status(message)
            message = "Rack " + str(rack_id) + ": "
            if is_obstructed == 1:
                message += "Obstructed | "
            if is_skewed == 1:
                message += "Skewed | "
            if is_overload_motor == 1:
                message += "Overload Motor"
            self.uic.rackGroupList[index].rackGroupErrorLineEdit.setText(message)

class ThreadClass(QtCore.QThread):
    env_signal = pyqtSignal(str)
    opr_signal = pyqtSignal(str)
    brk_signal = pyqtSignal(str)

    def __init__(self, index=-1, rack_id=1, opr_number = -1, err_numbers = [1]):
        super().__init__()
        self.index = index
        self.master_controller = MasterCom(rack_group_id=self.index, port='COM' + str(3 + self.index * 2))
        self.rack_id = rack_id
        self.opr_number = opr_number
        self.err_numbers = err_numbers

    def run(self):
        print('Starting master controller...', self.index)
        print('Starting simulate normal...', self.index)
        self.master_controller.start()

        env_thread = threading.Thread(target=self.master_controller.run_masterControllerEnvState, daemon=True,args=(5,))
        env_thread.start()

        read_computerIPC_thread = threading.Thread(target=self.master_controller.read_line_from_computerIPC, daemon=True)
        read_computerIPC_thread.start()

        while True:
            time.sleep(1)
            if self.master_controller.env_messages:
                self.env_signal.emit(self.master_controller.env_messages[0])
            if self.master_controller.opr_messages:
                self.opr_signal.emit(self.master_controller.opr_messages[0])
            if self.master_controller.brk_messages:
                self.brk_signal.emit(self.master_controller.brk_messages[0])

    # def start_running_normal(self):
    #     print('Starting simulate normal...', self.index)
    #     self.master_controller.start()
    #
    #     env_thread = threading.Thread(target=self.master_controller.run_masterControllerEnvState, daemon=True, args=(5,))
    #     env_thread.start()
    #
    #     read_computerIPC_thread = threading.Thread(target=self.master_controller.read_line_from_computerIPC, daemon=True)
    #     read_computerIPC_thread.start()

    def run_normal(self):
        self.master_controller.is_run = True
        
        if self.master_controller.ventilating_racks or self.master_controller.closing_racks or self.master_controller.opening_racks:
            self.master_controller.is_rack_operation = True
            opr_thread = threading.Thread(target=self.master_controller.run_masterControllerOperationState, args=(1,))
            opr_thread.start()
            print("operation hihi")

        env_thread = threading.Thread(target=self.master_controller.run_masterControllerEnvState, daemon=True, args=(5,))
        env_thread.start()
    
    def stop_normal(self):
        self.master_controller.is_run = False
        self.master_controller.is_rack_operation = False

    def run_error(self):
        print('Starting simulate error...', self.index)

        # khi mo phong co loi xay ra thi khong hoat dong va gui nhiet do nua
        self.stop_normal()

        self.master_controller.is_error = True
        brkdown_thread = threading.Thread(target=self.master_controller.run_masterControllerBreakdownState, daemon=True, args=(6, self.rack_id, self.err_numbers))
        brkdown_thread.start()

    def stop_error(self):
        self.master_controller.is_error = False

        # master_controller run normal
        self.run_normal()


    def stop(self):
        print('Stopping master controller...', self.index)
        self.master_controller.execute_stopRunning()
        self.terminate()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

