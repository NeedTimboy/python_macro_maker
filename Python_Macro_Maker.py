import PySimpleGUI as sg
import threading
import time
import random
from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KeyboardController, Key

# Initialize controllers
mouse = Controller()
keyboard = KeyboardController()

# Global variable to control the macro
running = False

def click_macro(interval, interval_range, action):
    global running
    while running:
        if action == "Right-Click":
            mouse.click(Button.right)
        elif action == "Left-Click":
            mouse.click(Button.left)
        elif action == "Space Bar":
            keyboard.press(Key.space)
            keyboard.release(Key.space)

        if interval_range:
            time.sleep(random.uniform(interval_range[0], interval_range[1]))
        else:
            time.sleep(interval)

# Define the UI layout
layout = [
    [sg.Text("Time interval (seconds, single value or range):"), sg.InputText("1", key="INTERVAL", size=(15, 1))],
    [sg.Text("Action:"), sg.Combo(["Right-Click", "Left-Click", "Space Bar"], default_value="Right-Click", key="ACTION")],
    [sg.Text("Status: Not Running", size=(30, 1), key="STATUS")],
    [sg.Button("Start", key="START"), sg.Button("Stop", key="STOP"), sg.Button("Exit")]
]

# Create the window
window = sg.Window("Mouse and Keyboard Macro Tool", layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        running = False
        break

    if event == "START":
        try:
            interval_input = values["INTERVAL"].strip()
            action = values["ACTION"]

            # Determine if input is a range
            if "-" in interval_input:
                range_parts = interval_input.split("-")
                interval_range = [float(range_parts[0]), float(range_parts[1])]
                interval_range.sort()  # Ensure range is in ascending order
                interval = None
            else:
                interval = float(interval_input)
                if interval <= 0:
                    sg.popup_error("Please enter a positive number for the interval.")
                    continue
                interval_range = None

            if not running:
                running = True
                window["STATUS"].update("Status: Running")
                threading.Thread(target=click_macro, args=(interval, interval_range, action), daemon=True).start()
        except ValueError:
            sg.popup_error("Invalid input. Please enter a numeric value or a valid range (e.g., 1-5).")

    if event == "STOP":
        running = False
        window["STATUS"].update("Status: Not Running")

window.close()
