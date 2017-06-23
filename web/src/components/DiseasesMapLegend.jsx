import React, { Component } from 'react';
import Control from 'react-leaflet-control';
import { connect } from 'react-redux';

import {diseasesColors} from '../utils.jsx';

@connect(state => state)
export default class InfoPanelControl extends Component {

    generateLegendEntry = (firstValue, secondValue, colorIndex)=> {

        return (<div key={colorIndex}><i style={{background: diseasesColors[colorIndex], width: '18px', height: '18px', float: 'left', marginRight: '8px', opacity: 0.7}}></i> {firstValue} &ndash; {secondValue} <br/></div>);
    }

    render() {
        const {state} = this.props;
        const diseaseIndex = state.diseases.codification[state.selectedDisease]
        const diseaseLevels = state.diseaseStatistics.boundaries[diseaseIndex]

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
                color: '#555'}}>
                    <div key={0}><i style={{background: diseasesColors[0], width: '18px', height: '18px', float: 'left', marginRight: '8px', opacity: 0.7}}></i> {0} &ndash; {diseaseLevels[0]} <br/></div>
                    <div key={1}><i style={{background: diseasesColors[1], width: '18px', height: '18px', float: 'left', marginRight: '8px', opacity: 0.7}}></i> {diseaseLevels[0]} &ndash; {diseaseLevels[1]} <br/></div>
                    <div key={2}><i style={{background: diseasesColors[2], width: '18px', height: '18px', float: 'left', marginRight: '8px', opacity: 0.7}}></i>
                        &gt; {diseaseLevels[1]} <br/></div>
                </div>
            </Control>
        );
    }

}
