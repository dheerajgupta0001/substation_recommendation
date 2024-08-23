

def getReasonableVoltVals(busesVolts: dict[str, list[float]])->list[float]:
    # returns the first resonable bus voltage values from multiple bus voltages
    # todo get limit from config
    reasonabilityLimit = 100
    for busVoltMeasId in busesVolts:
        busVoltSamples = busesVolts[busVoltMeasId]
        # disqualify bus for taking voltages if even one voltage value is not reasonable
        if not any(x <= reasonabilityLimit for x in busVoltSamples):
            return busVoltSamples
    return []