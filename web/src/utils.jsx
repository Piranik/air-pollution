import React, { Component } from 'react';

export const isInArray = (value, array) => {
    return array.indexOf(value) > -1;
}

export const BreakException = {};

export const getCountyNameFromFeature = (feature) => {
    return feature.properties.name.trim().toLowerCase().replace(/ /g, '-');
}

export const paramsColors = ['#00904E', '#00B756', '#93CA55', '#FFD432', '#FF643A', '#F12568'];
export const temperatureColors = ['#3C78D8', '#6D9EEB', '#93C47D', '#F6B26B', '#E06666'];
export const rainfallColors = ['#E06666', '#F6B26B', '#93C47D', '#6D9EEB', '#3C78D8'];
export const windAndPressureColors = ['#6AA84F', '#93C47D', '#FFE599', '#FFD966', '#E06666'];
export const diseasesColors = ['#00E400', '#FF7E00', '#FF0000'];
export const BLOCKED_COLOR = '#646161'

export const AQI_INDEX = 2000
export const OZONE_INDEX = 9

export const paramsIndexesWithMontlyValues = [20, 24]
export const temperatureIndex = 20
export const rainfallIndex = 24
export const windOrPressureIndexes = [19, 22]

export const displayMeasurementUnit = (parameterIndex, measurementUnits, mode) => {
    if (mode == 'diseases') {
        return (<span></span>);
    }

    const measurementUnit = measurementUnits[parameterIndex];
    if (parameterIndex == 20) {
        return (<span>&deg; {measurementUnit}</span>);
    }
    else if (isInArray(parameterIndex, [1, 3, 4, 5, 9, 10, 1001])) {
        return (<span>{measurementUnit}<sup>3</sup></span>);
    }
    else {
        return (<span>{measurementUnit}</span>);
    }

}

export const isEmpty = (obj) => {
    return Object.keys(obj).length === 0;
}

export const getColorsSetBySelectedIndex = (parameterIndex) => {
    let colors = paramsColors;
    if (isInArray(parameterIndex, windOrPressureIndexes)) {
        colors = windAndPressureColors;
    }
    else if (parameterIndex == temperatureIndex) {
        colors = temperatureColors;
    }
    else if (parameterIndex == rainfallIndex) {
        colors = rainfallColors;
    }
    return colors;
}

