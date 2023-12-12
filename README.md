# Brightness Controller

## Overview

This Python script, `5_screen_brightness.py`, is designed to dynamically adjust the screen brightness based on the content being displayed. It utilizes OpenCV to capture live frames from the screen, calculates the ratio of bright pixels to total pixels, and adjusts the brightness accordingly.

**Caution:**
**ONLY USE THIS PROGRAM IF IT IS OF ABSOLUTE NECESSITY. THIS PROGRAM IS NOT RECOMMENDED FOR REGULAR USE.**

**CAUTION: THIS PROGRAM MAY CAUSE PERMANENT DAMAGE TO YOUR DISPLAY. IT MAY NOT BE IMMEDIATE, BUT IT WILL HAPPEN EVENTUALLY AS THE DISPLAY IS MADE TO HANDLE A SET NUMBER OF BRIGHTNESS CHANGES IN ITS LIFETIME. THIS PROGRAM MAY CAUSE THE DISPLAY TO EXCEED THAT NUMBER OF BRIGHTNESS CHANGES. THIS MAY CAUSE THE DISPLAY TO MALFUNCTION OR EVEN PERMANENTLY DAMAGE THE DISPLAY.

This program is a proof of concept for automatically adjusting the screen brightness based on the brightness of the screen content.

## Features

- Adjust screen brightness based on the ratio of bright pixels to total pixels.
- Real-time adjustment for dynamic responsiveness.

## Dependencies

To ensure a clean and isolated environment, it's recommended to use a virtual environment. Follow these steps:

1. Create a virtual environment (inside the project directory):

   ```bash
   python -m venv env
   ```
2. Activate the virtual environment:

    - On Windows:

        ```
        .\env\Scripts\activate
        ```

    - On macOS/Linux:

        ```
        source env/bin/activate
        ```

3. Install the required Python packages (run any one of the following commands inside the activated environment):

    ```bash
    pip install numpy opencv-python Pillow screen-brightness-control tk
    ```

    OR

   ```bash
   pip install -r requirements.txt
   ```

This will create a separate environment for your project, preventing conflicts with other projects and ensuring a clean setup.

## Usage

1. Make sure dependencies are installed.

2. Run the script in the activated virtual environment:

    ```bash
    python 5_screen_brightness.py
    ```

## Script Details

1. Use with Caution:
    
    This script is not recommended for regular use due to the potential risk of permanent damage to the display.

2. Adjustments:

    Brightness adjustments are made in real-time based on the brightness ratio of the captured screen content.

3. Continuous Update:
    
    The script runs a continuous update thread to monitor screen content and adjust brightness accordingly.

## Planned Features (29-11-2023)
1. Toggle button for brightness controller.
2. Toggle button for GUI visibility.
3. Toggle button for GUI transparency.
4. Toggle button for GUI always on top.
5. Toggle button for GUI border.
6. Toggle button for GUI resize.
7. Toggle button for GUI drag.
8. Toggle button for GUI close.
9. Toggle button for GUI minimize.
10. Toggle button for GUI maximize.
11. Save and load brightness levels to/from a file.
12. Reset brightness levels to default.
13. Create default brightness levels if not found.
14. Use PERCEIVED BRIGHTNESS in brightness ratio calculation.

## Feedback and Contributions

Please use this script with caution and provide feedback for improvements. Contributions are welcome!

Author
[Sushil Maurya]

Date
27-11-2023
