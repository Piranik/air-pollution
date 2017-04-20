import React, { Component } from 'react';

export const isInArray = (value, array) => {
    return array.indexOf(value) > -1;
}

export const BreakException = {};

export const getCountyNameFromFeature = (feature) => {
    return feature.properties.name.trim().toLowerCase().replace(/ /g, '-');
}

export const temperatureColors = ['#0A43BC', '#6590ED', '#00E400', '#FFA100', '#E31A1C'];
export const BLOCKED_COLOR = '#646161'
export const paramsColors = ['#00E400', '#FFFF00', '#FF7E00', '#FF0000', '#99004C', '#7E0023'];

export const AQI_INDEX = 1000
export const OZONE_INDEX = 9

export const paramsWithMontlyValues = [20, 24]
export const paramTemperature = 20


export const displayMeasurementUnit = (parameterIndex, measurementUnits) => {
    console.log(parameterIndex,measurementUnits);
    const measurementUnit = measurementUnits[parameterIndex];

    if (parameterIndex == 20) {
        return (<span>&deg; {measurementUnit}</span>);
    }
    else if (isInArray(parameterIndex, [1, 3, 4, 5, 9, 10])) {
        return (<span>{measurementUnit}<sup>3</sup></span>);
    }
    else {
        return (<span>{measurementUnit}</span>);
    }

}

