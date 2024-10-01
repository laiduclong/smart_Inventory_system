import threading
import time

# Hàm in ra màn hình với delay
def print_with_delay(message, delay):
    time.sleep(delay)
    print(message)

# Tạo và khởi chạy các luồng
def main():
    # Tạo luồng 1
    thread1 = threading.Thread(target=print_with_delay, args=("Luồng 1: Bắt đầu", 2))
    thread1.start()

    # Tạo luồng 2
    thread2 = threading.Thread(target=print_with_delay, args=("Luồng 2: Bắt đầu", 1))
    thread2.start()

    # Chờ cho các luồng hoàn thành
    thread1.join()
    thread2.join()

    print("Tất cả các luồng đã hoàn thành.")

if __name__ == "__main__":
    main()