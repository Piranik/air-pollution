export const CHANGE_PARAMETER_ACTION = 'CHANGE_PARAMETER_ACTION'
export const CHANGE_COUNTY_ACTION = 'CHANGE_COUNTY_ACTION'
export const CHANGE_DISPLAY_YEAR = 'CHANGE_DISPLAY_YEAR'


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
