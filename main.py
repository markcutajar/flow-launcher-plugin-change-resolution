# -*- coding: utf-8 -*-

import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))


from flowlauncher import FlowLauncher
import win32api
import win32con


class ResolutionChanger(FlowLauncher):
    def query(self, query: str):
        """
        Expected query format: 'resolution <width> <height> <refresh>'
        Example: 'resolution 1920 1080 60'
        """
        parts = query.split()
        if len(parts) != 4 or parts[0].lower() != "resolution":
            return [{
                "Title": "Invalid command",
                "SubTitle": "Use format: resolution <width> <height> <refresh_rate>",
                "IcoPath": "Images/app.png"
            }]
        
        try:
            width = int(parts[1])
            height = int(parts[2])
            refresh_rate = int(parts[3])
            self.set_resolution(width, height, refresh_rate)
            return [{
                "Title": f"Resolution set to {width}x{height} @ {refresh_rate}Hz",
                "SubTitle": "Successfully applied resolution settings",
                "IcoPath": "Images/app.png"
            }]
        except ValueError:
            return [{
                "Title": "Invalid input",
                "SubTitle": "Please enter numeric values for width, height, and refresh rate.",
                "IcoPath": "Images/app.png"
            }]

    def set_resolution(self, width, height, refresh_rate):
        devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
        devmode.PelsWidth = width
        devmode.PelsHeight = height
        devmode.DisplayFrequency = refresh_rate
        devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT | win32con.DM_DISPLAYFREQUENCY
        win32api.ChangeDisplaySettings(devmode, win32con.CDS_FULLSCREEN)


if __name__ == "__main__":
    ResolutionChanger()
