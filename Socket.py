import socket
import time
from tkinter import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def ConnectToEsp32():
    host = "192.168.4.1"  # ESP32 IP in local network
    port = 80  # ESP32 Server Port
    sock.connect((host, port))


def InputFromUser():
    while True:
        inputValue = input("Enter value... ")
        if not inputValue:
            print("Input is Empty")
        else:
            sock.send(bytes(inputValue, 'utf-8'))


def SetAngle(inputValue):
    sock.sendall(inputValue.encode())


def SendingSliderValue(inputValue):
    sock.send(bytes(inputValue, 'utf-8'))
    time.sleep(0.05)
    print(sock.recvmsg(__bufsize=10))



def slider_changed(angle):
    print(angle)
    SendingSliderValue(angle)


def Create_Slider():
    root = Tk()
    root.title("Servo Motor Controller")
    root.geometry("400x200")
    # sliderValue = tkinter.DoubleVar()

    horizontal = Scale(
        root,
        from_=1,
        to=178,
        orient=HORIZONTAL,
        command=slider_changed
    )

    horizontal.pack()
    root.mainloop()

# Create_Slider()
ConnectToEsp32()
InputFromUser()
