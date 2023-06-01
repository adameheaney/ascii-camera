import cv2
import tkinter as tk
from tkinter import font
from ctypes import windll

# 9 chars
ascii_conversion = ['@', '%', '#', '*', '+', '=', '-', ':', '.']

# unblurs text
windll.shcore.SetProcessDpiAwareness(1)

def createWindow():
    # Create a window
    window = tk.Tk()

    # Set the window title
    window.title("My Window")

    # Set the window size
    window.geometry("1280x720")
    window.configure(bg="black")
    return window

def clamp(value, min_value, max_value):
        return max(min(value, max_value), min_value)

def main():
    window = createWindow()
    capture = cv2.VideoCapture(0)
    custom_font = font.Font(family="Cascadia Mono", size=12)
    label = tk.Label(window, text="", font=custom_font, fg="white", bg="black")
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = capture.read()

            # If frame is read correctly, ret will be True
            if not ret:
                print("Failed to capture frame")
                break

            height, width, channels = frame.shape
            ratio = height / width / 2.7
            newWidth = 100
            newHeight = int(ratio * newWidth)
            frame = cv2.resize(frame, (newWidth, newHeight), cv2.INTER_CUBIC)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            asciiFrame = ''
            for y in range(0, newHeight):
                for x in range(0, newWidth):
                    luminance = clamp(int(frame[y, x] / 24.875), 0, 8)   # noqa: E501
                    asciiFrame = asciiFrame + ascii_conversion[luminance]  
                asciiFrame = asciiFrame + "\n"
            label.config(text = asciiFrame)

            # Pack the label widget to display it on the window
            label.pack()
            window.update()
            # print("\n" + "\n" + asciiFrame)
    except:  # noqa: E722
        print("caught error")
    window.mainloop()

main()

    
