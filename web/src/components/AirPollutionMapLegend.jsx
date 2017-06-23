import React, { Component } from 'react';
import Control from 'react-leaflet-control';
import { connect } from 'react-redux';

import {paramTemperature, paramsColors, temperatureColors, isInArray, paramsIndexesWithMontlyValues, AQI_INDEX, displayMeasurementUnit, OZONE_INDEX, getColorsSetBySelectedIndex} from '../utils.jsx';

@connect(state => state)
export default class InfoPanelControl extends Component {

    generateLegendEntry = (firstValue, secondValue, colorIndex, color, measurementUnit)=> {
        return (<div key={colorIndex}><i style={{background: color, width: '18px', height: '18px', float: 'left', marginRight: '8px', opacity: 0.7}}></i> {firstValue} &ndash; {secondValue} {measurementUnit}<br/></div>);
    }

    generateFirstLegendEntry = (secondValue, colorIndex, color, measurementUnit) => {
        return (<div key={colorIndex}><i style={{background: color, width: '18px', height: '18px', float: 'left', marginRight: '8px', opacity: 0.7}}></i>  &lt; {secondValue} {measurementUnit}<br/></div>);
    }

    generateLastLegendEntry = (firstValue, colorIndex, color, measurementUnit) => {
        return (<div key={colorIndex}><i style={{background: color, width: '18px', height: '18px', float: 'left', marginRight: '8px', opacity: 0.7}}></i> &gt; {firstValue} {measurementUnit} <br/></div>);

    }
    generateLegendEntryForAQI = (value, color) => {
        const colors = paramsColors;
        return (
            <div key={value}><i style={{background: color, width: '18px', height: '18px', float: 'left', marginRight: '8px', opacity: 0.7}}></i> {value} </div>
        );
    }

    generate

    render() {
        const {state} = this.props;

        let paramsLevels;

        if (state.selectedParameter.index == AQI_INDEX) {
            paramsLevels = [1, 2, 3, 4, 5, 6];
        }
        else if (isInArray(state.selectedParameter.index, paramsIndexesWithMontlyValues)) {
            paramsLevels = state.paramsLevels[state.selectedParameter.index][state.selectedMonth];
        }
        else {
            paramsLevels = state.paramsLevels[state.selectedParameter.index];
        }

        const that = this;
        const measurementUnit = displayMeasurementUnit(state.selectedParameter.index,
            state.measurementUnits);
        const colors = getColorsSetBySelectedIndex(state.selectedParameter.index);
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
                            return that.generateLegendEntryForAQI(element, colors[index]);
                        })
                         :
                        paramsLevels.map(function(element, index, array) {
                            let firstValue, secondValue;
                            if (index == 0) {
                                secondValue = element
                                return that.generateFirstLegendEntry(secondValue, index, colors[index], measurementUnit);
                            }
                            else {
                                firstValue = array[index-1];
                                secondValue = array[index];
                                return that.generateLegendEntry(firstValue, secondValue, index, colors[index], measurementUnit);
                            }

                            return that.generateLegendEntry(firstValue, element, index,
                                    state.selectedParameter.index, measurementUnits);
                        }).concat(that.generateLastLegendEntry(paramsLevels[paramsLevels.length - 1], paramsLevels.length, colors[paramsLevels.length], measurementUnit))
                }</div>
            </Control>
        );
    }

}
