from typing import TypedDict

class IFileInfo(TypedDict):
    substation_name: str
    voltage_level: int
    filename: str
    format: str
    folder_location: str