import threading

import cv2
import numpy as np
import tkinter as tk

from PIL import ImageGrab
from screen_brightness_control import set_brightness, get_brightness


# Features to be added(29-11-2023):
"""
1. Add a button to toggle the brightness controller on/off.
2. Add a button to toggle the GUI on/off.
3. Add a button to toggle the GUI transparency.
4. Add a button to toggle the GUI always on top.
5. Add a button to toggle the GUI border.
6. Add a button to toggle the GUI resize.
7. Add a button to toggle the GUI drag.
8. Add a button to toggle the GUI close.
9. Add a button to toggle the GUI minimize.
10. Add a button to toggle the GUI maximize.
11. Save the brightness levels dictionary to a file and load it on startup.
12. Add a button to reset the brightness levels dictionary to default.
13. If the brightness levels dictionary is not found, create it with default values.
14. Update the brightness ratio logic to use PERCEIVED BRIGHTNESS instead of the sum of r, g, b.
"""


# Inputs from Chatgpt on 29-11-2023:
"""
1. Magic Numbers:
Replace the magic number 75 in the get_brightness_ratio method with a named constant or a class variable for better readability.
Consider making total_no_of_brightness_keys a class variable if it is not intended to be changed.

2. Comments:
Add comments to describe the purpose of critical sections of code, especially within the get_brightness_ratio method.
Add comments where necessary to explain the logic behind certain calculations, especially in the set_brightness_levels_dict method.

3. Code Duplication:
The code to create the keys for brightness levels and the values for brightness levels is repeated in the set_brightness_levels_dict method. Consider creating helper methods for these tasks to avoid duplication.

4. Constants:
Consider using uppercase variable names for constants like threshold_sum and total_no_of_brightness_keys for better convention.

5. Exception Handling:
Add appropriate exception handling in critical sections, such as capturing the screen (capture_screen) and setting the brightness (set_brightness). This is important to handle potential errors gracefully.

6. Threading:
Consider providing a way to gracefully exit the continuous_update thread when the application is closed. For example, you could use an event flag to signal the thread to stop.

7. Code Structure:
Group related methods together, for example, all GUI-related methods, all brightness-related methods, etc. This makes the code more readable and maintainable.

8. Scaling Values:
Instead of rounding the start and end ranges in set_brightness_levels_dict to a fixed number of decimal places, you might consider using the round function dynamically based on the precision of the input values.

9. Error Handling:
It might be beneficial to add error handling for cases where the screen capture or brightness adjustment fails.
"""


class BrightnessController:
    def __init__(self):
        self.root = tk.Tk()

        # Define the root window properties
        self.root.overrideredirect(True)
        self.root.geometry("+0+0")
        self.root.attributes('-alpha', 0.35, '-topmost', True)

        # Define the range variables for brightness within which the brightness will be adjusted
        self.max_brightness = tk.IntVar(value=100)
        self.min_brightness = tk.IntVar(value=0)
        
        # Define the brightness levels
        self.brightness_levels_dict = {}
        
        # Frame for brightness and brightness ratio
        self.br_frame = tk.Frame(self.root)
        self.br_frame.pack()

        self.brightness_label = tk.Label(self.br_frame, text="Brightness: ", font=("Helvetica", 12))
        self.brightness_label.pack(side=tk.LEFT)

        self.brRatio = tk.Label(self.br_frame, text="Br Ratio: ", font=("Helvetica", 12))
        self.brRatio.pack()

        # Frame for max brightness
        self.max_frame = tk.Frame(self.root)
        self.max_frame.pack()

        self.max_brightness_label = tk.Label(self.max_frame, text="Max: ", font=("Helvetica", 12))
        self.max_brightness_label.pack(side=tk.LEFT, anchor=tk.S)

        self.max_brightness_scale = tk.Scale(self.max_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.max_brightness, command=self.update_min_scale, length=210)
        self.max_brightness_scale.pack()

        # Frame for min brightness
        self.min_frame = tk.Frame(self.root)
        self.min_frame.pack()

        self.min_brightness_label = tk.Label(self.min_frame, text="Min: ", font=("Helvetica", 12))
        self.min_brightness_label.pack(side=tk.LEFT, anchor=tk.S)

        self.min_brightness_scale = tk.Scale(self.min_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.min_brightness, command=self.update_max_scale, length=210)
        self.min_brightness_scale.pack()

        # Initialize the brightness value in brightness label
        self.update_brightness_text()

        # Initialize the brightness levels dictionary
        self.set_brightness_levels_dict()

        # Start the actual brightness controller on a separate thread
        # This is done to avoid blocking the main thread which is responsible for updating the GUI
        self.start_continuous_update()

        self.root.mainloop()

    def start_continuous_update(self):
        # Start a separate thread for continuous brightness update
        self.update_thread = threading.Thread(target=self.continuous_update)
        self.update_thread.daemon = True    # Stops the thread when the main thread is stopped
        self.update_thread.start()

    def continuous_update(self):
        while True:
            screen_content = self.capture_screen()
            brightness_ratio = self.get_brightness_ratio(screen_content)

            # Set the brightness level based on the brightness ratio
            for (lower, upper), brightness_value in self.brightness_levels_dict.items():
                if lower <= brightness_ratio < upper:
                    set_brightness(int(brightness_value))

                    self.update_brightness_text()
                    self.update_brightness_ratio_text(brightness_ratio)

                    break

    def capture_screen(self):
        # Capture the entire screen content
        screen = np.array(ImageGrab.grab())
        return cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

    def get_brightness_ratio(self, frame):
        # Assuming bright pixels are those with the sum of r, g, b greater than the threshold
        threshold_sum = 75

        # Calculate the sum of r, g, b for each pixel group
        pixel_sums = np.sum(frame, axis=-1)

        # Count the number of pixel groups with sum greater than the threshold
        bright_pixels = np.sum(pixel_sums > threshold_sum)

        dim_pixels = int(frame.size / 3) - bright_pixels

        ratio = bright_pixels / int(frame.size / 3)
        return ratio
    
    def set_brightness_levels_dict(self):
        total_no_of_brightness_keys = 10    # CONSTANT

        # Store all the ranges of brightness levels
        keys = []
        for i in range(total_no_of_brightness_keys):
            start_range = round(i / total_no_of_brightness_keys, 5)
            end_range = round((i + 1) / total_no_of_brightness_keys, 5)

            keys.append((start_range, end_range))

        # Store all the values of brightness levels
        values = []
        for i in range(total_no_of_brightness_keys):
            # Min max formula is:
            # x = (((n - i - 1) * min) + (i * max)) / (n - 1)
            value = (((total_no_of_brightness_keys - i - 1) * self.min_brightness.get()) + (i * self.max_brightness.get())) / (total_no_of_brightness_keys - 1)

            values.append(int(value))

        # Reverse the values list so that for higher brightness ratio, the brightness value is lower
        values.reverse()

        # Create a dictionary of brightness levels
        self.brightness_levels_dict = dict(zip(keys, values))

    def update_brightness_text(self):
        current_brightness = get_brightness()[0]
        self.brightness_label.config(text=f"Brightness: {current_brightness}%")

    def update_brightness_ratio_text(self, brightness_ratio):
        self.brRatio.config(text=f"Br Ratio: {brightness_ratio:.5f}")

    def update_min_scale(self, value):
        max_value = self.max_brightness.get()
        min_value = self.min_brightness.get()
        if min_value > max_value:
            self.max_brightness_scale.set(min_value)
        self.min_brightness_scale.set(min_value)
        
        self.set_brightness_levels_dict()

    def update_max_scale(self, value):
        min_value = self.min_brightness.get()
        max_value = self.max_brightness.get()
        if max_value < min_value:
            self.min_brightness_scale.set(max_value)
        self.max_brightness_scale.set(max_value)

        self.set_brightness_levels_dict()

if __name__ == "__main__":
    brightness_controller = BrightnessController()
