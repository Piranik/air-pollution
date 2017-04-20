import React, { Component } from 'react';
import Control from 'react-leaflet-control';
import { connect } from 'react-redux';

import {isInArray, displayMeasurementUnit} from '../utils.jsx';

@connect(state => state)
export default class InfoPanelControl extends Component {

    displayControlInfo = () => {
        const {state, getValue} = this.props;
        if (state.hoveredCounty) {
            const countyName = state.hoveredCounty.charAt(0).toUpperCase() + state.hoveredCounty.slice(1);
            const countyValue = getValue(state.hoveredCounty).toFixed(2);
            const parameterIndex = state.selectedParameter.index;
            return <span><b>{countyName}</b><br/>{countyValue} {displayMeasurementUnit(parameterIndex, state.measurementUnits)}</span>;
        }
        return 'Hover over a county';
    }

    render() {
        const {state} = this.props;

        return (
            <Control position="topright">
                <div style={{
                    padding: '6px 8px',
                    font: '14px/16px Arial, Helvetica, sans-serif',
                    background: 'white',
                    background: 'rgba(255, 255, 255, 1)',
                    boxShadow: '0 0 15px rgba(0, 0, 0, 0.2)',
                    borderRadius: '5px',
                    }}>
                    <h4 style={{
                        margin: '0 0 5px',
                        color: '#777',
                    }}>
                        {state.selectedParameter.name} Value
                    </h4>
                        {this.displayControlInfo()}
                </div>
            </Control>
        );
    }
}
