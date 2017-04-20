import React, { Component } from 'react';
import Control from 'react-leaflet-control';
import { connect } from 'react-redux';

import {paramTemperature, paramsColors, temperatureColors, isInArray, paramsWithMontlyValues, AQI_INDEX, displayMeasurementUnit, OZONE_INDEX} from '../utils.jsx';

@connect(state => state)
export default class InfoPanelControl extends Component {

    generateLegendEntry = (firstValue, secondValue, colorIndex, parameterIndex, measurementUnits)=> {
        let colors = parameterIndex == paramTemperature ? temperatureColors : paramsColors;

        if (parameterIndex == OZONE_INDEX) {
            colors = colors.slice()
            colors.splice(1, 1);
        }

        return (<div key={colorIndex}><i style={{background: colors[colorIndex], width: '18px', height: '18px', float: 'left', marginRight: '8px', opacity: 0.7}}></i> {firstValue} &ndash; {secondValue} {displayMeasurementUnit(parameterIndex, measurementUnits)}<br/></div>);
    }

    generateLegendEntryForAQI = (value) => {
        const colors = paramsColors;
        return (
            <div key={value}><i style={{background: colors[value], width: '18px', height: '18px', float: 'left', marginRight: '8px', opacity: 0.7}}></i> {value} </div>
        );
    }

    generate

    render() {
        const {state} = this.props;

        let paramsLevels;

        if (state.selectedParameter.index == AQI_INDEX) {
            paramsLevels = [0, 1, 2, 3, 4, 5];
        }
        else if (isInArray(state.selectedParameter.index, paramsWithMontlyValues)) {
            paramsLevels = state.paramsLevels[state.selectedParameter.index][state.selectedMonth];
        }
        else {
            paramsLevels = state.paramsLevels[state.selectedParameter.index];
        }

        if (state.selectedParameter.index == OZONE_INDEX) {
            paramsLevels = paramsLevels.slice()
            paramsLevels.splice(1, 1);
        }

        const that = this;
        return (
            <Control position="bottomright">
                <div style={{
                padding: '6px 8px',
                font: '14px/16px Arial, Helvetica, sans-serif',
                background: 'white',
                background: 'rgba(255, 255, 255, 1)',
                boxShadow: '0 0 15px rgba(0, 0, 0, 0.2)',
                borderRadius: '5px',
                lineHeight: '18px',
                color: '#555'}}>{
                    state.selectedParameter.index == AQI_INDEX ?
                        paramsLevels.map(function(element, index, array) {
                            return that.generateLegendEntryForAQI(element);
                        }) :
                        paramsLevels.map(function(element, index, array) {
                            let firstValue;
                            if (index == 0 && state.selectedParameter.index == paramTemperature) {
                                firstValue = -10;
                            }
                            else if (index == 0) {
                                firstValue = 0;
                            }
                            else {
                                firstValue = array[index-1];
                            }

                            return that.generateLegendEntry(firstValue, element, index,
                                    state.selectedParameter.index, state.measurementUnits);
                        })
                }</div>
            </Control>
        );
    }

}
