import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'

import { Button, Alert, Spinner, Row, Col } from 'elemental'
import { Map, Marker, Popup, TileLayer, GeoJSON } from 'react-leaflet';

import {store} from '../stores/store';


// 46.130/25.203
const position = [46.130, 25.203];
const mapAccessToken = 'pk.eyJ1IjoidGVvZG9yc3RlZnUiLCJhIjoiY2owbDY3dzBqMDJhajJxcWRkdGVoeDQ5ZiJ9.5mPrtadAUQKbMGQBBQ-3kA'

const paramsColors = ['#00E400', '#FFFF00', '#FF7E00', '#FF0000', '#99004C'];

const AQI_INDEX = 1000
const paramsForTempColors = [20]


const tempColors = ['#0A43BC', '#6590ED', '#F0F04C', '#FFA100', '#E31A1C'];

const AQIColors = ['#00E400', '#FFFF00', '#FF7E00', '#FF0000', '#99004C'];

const BLOCKED_COLOR = '#646161'

const isInArray = (value, array) => {
    return array.indexOf(value) > -1;
}

@connect(state => state)
export default class MapComponent extends Component {
    // static propTypes = {
    //     dispatch: React.PropTypes.func,
    //     map_data: React.PropTypes.object
    // }

    getColor = () => {
        return '#4F7E00';
    }

    // check county has stations
    countyHasStations = (countyName) => {

        const {state} = this.props
        const countyIndex = state.counties.indexCodification[countyName];
        const stationsInCounty = state.airPollution.stationsInCounties[countyIndex];
        return stationsInCounty.length > 0;
    }

    countyStyle = (county) => {
        const {state} = this.props
        const countyName = county.properties.name.trim().toLowerCase().replace(/ /g, '-');
        let color = "";

        if (!this.countyHasStations(countyName)) {
            color = BLOCKED_COLOR;
        }
        else if (state.selectedCounty != 'All Country' && countyName != state.selectedCounty) {
            color = BLOCKED_COLOR;
        }
        else {
            const value = this.getValueForCounty(countyName);
            color = this.getColorForCounty(value)
            // console.log(color)
        }

        return {
            fillColor: color,
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7
        };
    }

    getColorForCounty = (value) => {

        const { selectedParameter, paramsLevels } = this.props.state;
        if (selectedParameter.index == AQI_INDEX) {
            return AQIColors[value];
        }
        if (value == 0) {
            return BLOCKED_COLOR;
        }
        else {
            let index = 0;
            const colors = isInArray(selectedParameter.index, paramsForTempColors) ? tempColors : paramsColors;

            const paramsLevelsForCurrent = paramsLevels[selectedParameter.index]

            for (let levelsIndex in paramsLevels) {
                const levelValue = paramsLevelsForCurrent[levelsIndex]

                if (levelValue != null && levelValue <= value) {
                    index ++;
                }
            }

            return colors[index];
        }
    }

    getValueForCounty = (county) => {
        const { selectedYear, selectedMonth, selectedParameter, selectedCounty, airPollution, paramsLevels} = this.props.state
        const countyIndexCodification = this.props.state.counties.indexCodification;
        const paramsIndexCodification = this.props.state.usedParameters.indexCodification;
        const countyIndex = countyIndexCodification[county];
        const parameterIndex = paramsIndexCodification[selectedParameter.index];
        const yearIndex = selectedYear - 2010;
        const monthIndex = Number.parseInt(selectedMonth, 10);
        let values = [];
        if (countyIndex !== undefined && parameterIndex != undefined) {
            // console.log(airPollution)
            return airPollution.data[countyIndex][yearIndex][monthIndex][parameterIndex];
        }

        return undefined;
    }

    render() {
        const {state} = this.props
        if (state.mapCoords.data.length == 0 ||
            state.airPollution.data.length == 0 ||
            state.counties.data.length == 0 ||
            state.usedParameters.data.length == 0
            ) {
            return (
                <Spinner size="lg" />
            );
        }
        else {
            return (
                <Col
                    xs="80%"
                    sm="80%"
                    md="80%"
                    lg="80%"
                    >
                    <Map style={{height: '100%', width: '100%'}} center={state.mapCoords.centerPosition} zoom={6}  zoomControl={false} doubleClickZoom={false} >
                        <TileLayer
                          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                          url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
                        />
                        <GeoJSON data={state.mapCoords.data} style={this.countyStyle}/>
                    </Map>
                </Col>
            );
        }

    }

}
