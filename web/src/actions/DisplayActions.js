export const CHANGE_PARAMETER_ACTION = 'CHANGE_PARAMETER_ACTION';
export const CHANGE_COUNTY_ACTION = 'CHANGE_COUNTY_ACTION';
export const CHANGE_DISPLAY_YEAR = 'CHANGE_DISPLAY_YEAR';

export const PLAY_BUTTON_PRESSED = 'PLAY_BUTTON_PRESSED';
export const STOP_BUTTON_PRESSED = 'STOP_BUTTON_PRESSED';
export const NEXT_TIMELINE_STEP = 'NEXT_TIMELINE_STEP';

export function changeParameterAction(newParameter) {
    return {
        type: CHANGE_PARAMETER_ACTION,
        newParameter: newParameter
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
