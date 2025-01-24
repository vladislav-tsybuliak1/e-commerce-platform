from enum import Enum


class StockUnitEnum(str, Enum):
    KG = "KG"
    G = "G"
    L = "L"
    ML = "ML"
    PCS = "PCS"
    BOX = "BOX"
