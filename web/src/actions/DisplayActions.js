export const CHANGE_PARAMETER_ACTION            = 'CHANGE_PARAMETER_ACTION';
export const CHANGE_COUNTY_ACTION               = 'CHANGE_COUNTY_ACTION';
export const CHANGE_DISPLAY_YEAR                = 'CHANGE_DISPLAY_YEAR';
export const CHANGE_DISEASE_CATEGORY_ACTION     = 'CHANGE_DISEASE_CATEGORY_ACTION';
export const CHANGE_DISEASE_ACTION              = 'CHANGE_DISEASE_ACTION';

export const PLAY_BUTTON_PRESSED                = 'PLAY_BUTTON_PRESSED';
export const STOP_BUTTON_PRESSED                = 'STOP_BUTTON_PRESSED';
export const NEXT_TIMELINE_STEP                 = 'NEXT_TIMELINE_STEP';
export const STOP_TIMELINE                      = 'STOP_TIMELINE';
export const HOVER_COUNTY                       = 'HOVER_COUNTY';


export const CHANGE_TOOL_ACTION                 = 'CHANGE_TOOL_ACTION';
export const CHANGE_PREDICTION_DISEASE_ACTION   = 'CHANGE_PREDICTION_DISEASE_ACTION';
export const CHANGE_MONTHS_ACTION               = 'CHANGE_MONTHS_ACTION';
export const CHANGE_AQI_ACTION                  = 'CHANGE_AQI_ACTION';
export const CHANGE_WIND_ACTION                 = 'CHANGE_WIND_ACTION';
export const CHANGE_RAINFALL_ACTION             = 'CHANGE_RAINFALL_ACTION';
export const CHANGE_PRESSURE_ACTION             = 'CHANGE_PRESSURE_ACTION';
export const CHANGE_TEMP_ACTION                 = 'CHANGE_TEMP_ACTION';
export const CHANGE_DISEASE_CLASS_ACTION        = 'CHANGE_DISEASE_CLASS_ACTION';


export function changeToolAction(newTool) {
    return {
        type: CHANGE_TOOL_ACTION,
        newTool: newTool
    }
}

export function changePredictedDiseaseAction(newDisease) {
    return {
        type: CHANGE_PREDICTION_DISEASE_ACTION,
        newDisease: newDisease
    }
}

export function changeMonthsAction(newMonth) {
    return {
        type: CHANGE_MONTHS_ACTION,
        newMonth: newMonth
    }
}

export function changeAqiAction(newAqi) {
    return {
        type: CHANGE_AQI_ACTION,
        newAqi: newAqi
    }
}

export function changeWindAction(newWind) {
    return {
        type: CHANGE_WIND_ACTION,
        newWind: newWind
    }
}

export function changeRainfallAction(newRainfall) {
    return {
        type: CHANGE_RAINFALL_ACTION,
        newRainfall: newRainfall
    }
}

export function changePressureAction(newPressure) {
    return {
        type: CHANGE_PRESSURE_ACTION,
        newPressure: newPressure
    }
}


export function changeTempAction(newTemp) {
    return {
        type: CHANGE_TEMP_ACTION,
        newTemp: newTemp
    }
}
export function changeDiseaseClassAction(newDiseaseClass) {
    return {
        type: CHANGE_DISEASE_CLASS_ACTION,
        newDiseaseClass: newDiseaseClass
    }
}

export function changeParameterAction(newParameter) {
    return {
        type: CHANGE_PARAMETER_ACTION,
        newParameter: newParameter
    }
}

export function changeDiseaseCategory(newCategory) {
    console.log(newCategory)
    return {
        type: CHANGE_DISEASE_CATEGORY_ACTION,
        newCategory: newCategory
    }
}

export function changeDiseaseAction(newDisease) {
    console.log(newDisease)
    return {
        type: CHANGE_DISEASE_ACTION,
        newDisease: newDisease
    }
}

export function changeCountyAction(newCounty) {
    return {
        type: CHANGE_COUNTY_ACTION,
        newCounty: newCounty
    }
}

export function changeDisplayYear(newYear, newMonth) {
    return {
        type: CHANGE_DISPLAY_YEAR,
        newYear: newYear,
        newMonth: newMonth
    }
}


export function playButtonPressed() {
    return {
        type: PLAY_BUTTON_PRESSED
    }
}


export function stopButtonPressed() {
    return {
        type: STOP_BUTTON_PRESSED
    }
}


export function nextStepInTimeline(nextYear, nextMonth) {
    return {
        type: NEXT_TIMELINE_STEP,
        nextYear: nextYear,
        nextMonth: nextMonth
    }
}

export function stopTimeline() {
    return {
        type: STOP_TIMELINE
    }
}

export function hoverCounty(county) {
    return {
        type: HOVER_COUNTY,
        county: county
    }
}
