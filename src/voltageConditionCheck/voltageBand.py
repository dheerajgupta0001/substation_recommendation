def voltageBandRange(voltLvl: int)->tuple[int,int]:
    # todo get bands data from config
    if voltLvl == 400:
        overVoltage = 410
        underVoltage = 390

    if voltLvl == 765:
        overVoltage = 783
        underVoltage = 746

    return overVoltage, underVoltage