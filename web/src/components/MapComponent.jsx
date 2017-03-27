import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'

import { Button, Alert, Spinner, Row, Col } from 'elemental'
import { Map, Marker, Popup, TileLayer, GeoJSON } from 'react-leaflet';




// 46.130/25.203
const position = [46.130, 25.203];
const mapAccessToken = 'pk.eyJ1IjoidGVvZG9yc3RlZnUiLCJhIjoiY2owbDY3dzBqMDJhajJxcWRkdGVoeDQ5ZiJ9.5mPrtadAUQKbMGQBBQ-3kA'


@connect(state => state)
export default class MapComponent extends Component {
    // static propTypes = {
    //     dispatch: React.PropTypes.func,
    //     map_data: React.PropTypes.object
    // }

    render() {
        const {state} = this.props

        console.log(state.mapCoords.centerPosition)
        console.log("!!!!!", state.mapCoords.data)
        if (state.mapCoords.data.length == 0) {
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
                        // <GeoJSON data={state.mapCoords.data} />
                    </Map>
                </Col>
            );
        }
        else {
            return (
                <Col
                    xs="70%"
                    sm="70%"
                    md="70%"
                    lg="70%"
                    >
                    <Map style={{height: '100%', width: '100%'}} center={state.mapCoords.centerPosition} zoom={6}  zoomControl={false} doubleClickZoom={false} >
                        <TileLayer
                          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                          url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
                        />
                        <GeoJSON data={state.mapCoords.data} />
                    </Map>
                </Col>
            );
        }

    }

}
