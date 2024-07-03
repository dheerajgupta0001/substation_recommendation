def voltageBandRange(voltLvl: int):
    if voltLvl == 400:
        overVoltage = 420
        underVoltage = 380

    if voltLvl == 765:
        overVoltage = 780
        underVoltage = 730

    return overVoltage, underVoltage