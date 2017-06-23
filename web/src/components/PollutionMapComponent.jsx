import { Router, Route, Link } from 'react-router';
import { connect } from 'react-redux';
import React, { Component } from 'react';
import { Button, Alert, Spinner, Row, Col } from 'elemental';
import { Map, Marker, Popup, TileLayer, GeoJSON } from 'react-leaflet';
import Control from 'react-leaflet-control';


import InfoPanelControl from './InfoPanelControl.jsx';
import AirPollutionMapLegend from './AirPollutionMapLegend.jsx';
import {hoverCounty} from '../actions/DisplayActions.js';
import {store} from '../stores/store';
import {getCountyNameFromFeature, BreakException, isInArray, paramsColors, temperatureColors, rainfallColors, windAndPressureColors, BLOCKED_COLOR, AQI_INDEX, paramsIndexesWithMontlyValues,
    temperatureIndex, rainfallIndex, windOrPressureIndexes, getColorsSetBySelectedIndex } from '../utils.jsx';


@connect(state => state)
export default class PollutionMapComponent extends Component {

    // check county has stations
    countyHasStations = (countyName) => {
        const {state} = this.props
        const countyIndex = state.counties.indexCodification[countyName];
        const stationsInCounty = state.airPollution.stationsInCounties[countyIndex];
        return stationsInCounty.length > 0;
    }

    countyStyle = (county) => {
        const {state} = this.props
        const countyName = getCountyNameFromFeature(county);
        let color = "";

        if (!this.countyHasStations(countyName)) {
            color = BLOCKED_COLOR;
        }
        else if (state.selectedCounty != 'romania' && countyName != state.selectedCounty) {
            color = BLOCKED_COLOR;
        }
        else {
            const value = this.getValueForCounty(countyName);
            color = this.getColorForCounty(value)
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

        const { selectedParameter, paramsLevels, selectedMonth } = this.props.state;
        if (value == 0) {
            return BLOCKED_COLOR;
        }
        else if (selectedParameter.index == AQI_INDEX) {
            return paramsColors[value-1];
        }
        else {
            let index = -1;
            const colors = getColorsSetBySelectedIndex(selectedParameter.index);

            const currentParamsLevels =
                isInArray(selectedParameter.index, paramsIndexesWithMontlyValues) ? paramsLevels[selectedParameter.index][String(selectedMonth)] : paramsLevels[selectedParameter.index]
            try {
                currentParamsLevels.forEach(function(paramLevelValue, levelIndex) {
                    if (value < paramLevelValue ) {
                        index = levelIndex;
                        throw BreakException;
                    }
                })
                if (index == -1) {
                    index = currentParamsLevels.length
                }
            }
            catch (e) {
                if (e !== BreakException) throw e;
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
        let value = undefined;

        if (countyIndex !== undefined && parameterIndex != undefined) {
            value = airPollution.data[countyIndex][yearIndex][monthIndex][parameterIndex];
        }

        return value;
    }

    // Map functions, probably I will send them as props
    highlightFeature = (e) => {
        const layer = e.target;
        store.dispatch(hoverCounty(getCountyNameFromFeature(e.target.feature)));

        layer.setStyle({
            weight: 3,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.7
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
    }

    resetHighlight = (e) => {
        this.refs.geojson.leafletElement.resetStyle(e.target);
        store.dispatch(hoverCounty(null));
    }

    onEachFeature = (feature, layer) => {
        layer.on({
            mouseover: this.highlightFeature,
            mouseout: this.resetHighlight
        });
    }

    render() {
        const {state} = this.props;
        this.state = undefined
        return (
            <Col
                xs="77%"
                sm="77%"
                md="77%"
                lg="77%"
                >
                <Map id='pollution_map' style={{height: '100%',
                        width: '100%',
                        border: "5px solid"
                        }}
                        center={state.mapCoords.centerPosition} zoom={7}  zoomControl={false} doubleClickZoom={false} >
                    <TileLayer
                      attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                      url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
                    />
                    <GeoJSON ref="geojson" data={state.mapCoords.data} style={this.countyStyle} onEachFeature={this.onEachFeature}/>
                    <InfoPanelControl getValue={this.getValueForCounty} header={state.selectedParameter.name + ' Value'} mode={'pollution'}/>
                    <AirPollutionMapLegend />
                </Map>
            </Col>
        );
    }

}
