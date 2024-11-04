import sys
import os
import ctypes
from ctypes import wintypes
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))


from flowlauncher import FlowLauncher


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
        # Define structures
        class DEVMODE(ctypes.Structure):
            _fields_ = [
                ("dmDeviceName", ctypes.c_wchar * 32),
                ("dmSpecVersion", wintypes.WORD),
                ("dmDriverVersion", wintypes.WORD),
                ("dmSize", wintypes.WORD),
                ("dmDriverExtra", wintypes.WORD),
                ("dmFields", wintypes.DWORD),
                ("dmOrientation", wintypes.SHORT),
                ("dmPaperSize", wintypes.SHORT),
                ("dmPaperLength", wintypes.SHORT),
                ("dmPaperWidth", wintypes.SHORT),
                ("dmScale", wintypes.SHORT),
                ("dmCopies", wintypes.SHORT),
                ("dmDefaultSource", wintypes.SHORT),
                ("dmPrintQuality", wintypes.SHORT),
                ("dmColor", wintypes.SHORT),
                ("dmDuplex", wintypes.SHORT),
                ("dmYResolution", wintypes.SHORT),
                ("dmTTOption", wintypes.SHORT),
                ("dmCollate", wintypes.SHORT),
                ("dmFormName", ctypes.c_wchar * 32),
                ("dmLogPixels", wintypes.WORD),
                ("dmBitsPerPel", wintypes.DWORD),
                ("dmPelsWidth", wintypes.DWORD),
                ("dmPelsHeight", wintypes.DWORD),
                ("dmDisplayFlags", wintypes.DWORD),
                ("dmDisplayFrequency", wintypes.DWORD),
                ("dmICMMethod", wintypes.DWORD),
                ("dmICMIntent", wintypes.DWORD),
                ("dmMediaType", wintypes.DWORD),
                ("dmDitherType", wintypes.DWORD),
                ("dmReserved1", wintypes.DWORD),
                ("dmReserved2", wintypes.DWORD),
                ("dmPanningWidth", wintypes.DWORD),
                ("dmPanningHeight", wintypes.DWORD),
            ]

        ENUM_CURRENT_SETTINGS = -1
        CDS_FULLSCREEN = 4
        DM_PELSWIDTH = 0x80000
        DM_PELSHEIGHT = 0x100000
        DM_DISPLAYFREQUENCY = 0x400000

        # Initialize DEVMODE
        devmode = DEVMODE()
        devmode.dmSize = ctypes.sizeof(DEVMODE)
        
        # Get current settings
        ctypes.windll.user32.EnumDisplaySettingsW(None, ENUM_CURRENT_SETTINGS, ctypes.byref(devmode))
        
        # Set the new resolution and refresh rate
        devmode.dmPelsWidth = width
        devmode.dmPelsHeight = height
        devmode.dmDisplayFrequency = refresh_rate
        devmode.dmFields = DM_PELSWIDTH | DM_PELSHEIGHT | DM_DISPLAYFREQUENCY

        # Apply settings
        ctypes.windll.user32.ChangeDisplaySettingsW(ctypes.byref(devmode), CDS_FULLSCREEN)


if __name__ == "__main__":
    ResolutionChanger()
