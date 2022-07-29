import time
from tkinter import *

import serial

serial = serial.Serial(port="COM4", baudrate=115200, timeout=.1)


# serial.open()


def slider_changed(angle):
    SendingSliderValue(angle)


def InputFromUser():
    while True:
        inputValue = input("Enter value... ")
        if not inputValue:
            print("Input is Empty")
        else:
            time.sleep(0.05)
            serial.write(bytes(inputValue, 'utf-8'))
            print(serial.readall())


def SendingSliderValue(inputValue):
    # serial.write(bytes([int(inputValue)]))
    serial.write(bytes(inputValue, 'utf-8'))
    time.sleep(0.05)
    print(serial.readall())


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


Create_Slider()
# InputFromUser()
