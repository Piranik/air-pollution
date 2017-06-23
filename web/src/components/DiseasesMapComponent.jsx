import { Router, Route, Link } from 'react-router';
import { connect } from 'react-redux';
import React, { Component } from 'react';
import { Button, Alert, Spinner, Row, Col } from 'elemental';
import { Map, Marker, Popup, TileLayer, GeoJSON } from 'react-leaflet';
import Control from 'react-leaflet-control';


import InfoPanelControl from './InfoPanelControl.jsx';
import DiseasesMapLegend from './DiseasesMapLegend.jsx';
import {hoverCounty} from '../actions/DisplayActions.js';
import {store} from '../stores/store';
import {getCountyNameFromFeature, diseasesColors, BLOCKED_COLOR} from '../utils.jsx';


@connect(state => state)
export default class PollutionMapComponent extends Component {

    getValueForCounty = (county) => {
        const { selectedYear, selectedMonth, selectedDisease, selectedCounty, diseases, diseaseStatistics} = this.props.state
        const countyIndexCodification = this.props.state.counties.indexCodification;
        const countyIndex = countyIndexCodification[county];
        const diseaseIndex = diseases.codification[selectedDisease];
        const yearIndex = selectedYear - 2010;
        const monthIndex = Number.parseInt(selectedMonth, 10);
        let value = undefined;

        if (countyIndex !== undefined && diseaseIndex != undefined) {
            value = diseaseStatistics.data[countyIndex][yearIndex][monthIndex][diseaseIndex];
        }

        return value;
    }

    getColorForCounty = (value) => {

        const {diseases, diseaseStatistics, selectedDisease} = this.props.state;

        if (value == 0) {
            return BLOCKED_COLOR;
        }
        else {
            let index = 2;
            const diseaseIndex = diseases.codification[selectedDisease]
            const diseaseBoundaries = diseaseStatistics.boundaries[diseaseIndex]
            if (value <= diseaseBoundaries[0]) {
                index = 0;
            }
            if (value > diseaseBoundaries[0] && value <= diseaseBoundaries[1]) {
                index = 1;
            }
            return diseasesColors[index];
        }
    }

    countyStyle = (county) => {
        const {state} = this.props
        const countyName = getCountyNameFromFeature(county);
        let color;

        const value = this.getValueForCounty(countyName);

        if (!value || value == 0) {
            color = BLOCKED_COLOR;
        }
        else if (state.selectedCounty != 'romania' && countyName != state.selectedCounty) {
            color = BLOCKED_COLOR;
        }
        else {
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
                <Map id='disease_map' style={{height: '100%',
                        width: '100%',
                        border: "5px solid"
                        }}
                        center={state.mapCoords.centerPosition} zoom={7}  zoomControl={false} doubleClickZoom={false} >
                    <TileLayer
                      attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                      url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
                    />
                    <GeoJSON ref="geojson" data={state.mapCoords.data} style={this.countyStyle} onEachFeature={this.onEachFeature}/>
                    <InfoPanelControl getValue={this.getValueForCounty} header={state.selectedDisease + ' Cases'} mode={'diseases'}/>
                    <DiseasesMapLegend />
                </Map>
            </Col>
        );
    }

}
