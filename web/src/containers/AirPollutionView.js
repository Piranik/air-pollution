import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import {Row, Col, Spinner} from 'elemental'
import { store } from '../stores/store.js'

import {fetchParameters, fetchCounties, fetchMapCoords, fetchAirPollutionStatistics} from '../actions/apiActions.js'


import TitleComponent from '../components/TitleComponent'
import MapComponent from '../components/MapComponent'
import OptionPanelComponent from '../components/OptionPanelComponent'
import YearSliderComponent from '../components/YearSliderComponent'



@connect(state => state)
export default class AirPollutionView extends Component {

    componentDidMount() {
        const {dispatch} = store
        const {airPollution, usedParameters, mapCoords, counties} = this.props.state

        if (mapCoords.data.length == 0 && mapCoords.isFetchinng == false) {
            dispatch(fetchMapCoords())
        }

        if (airPollution.data.length == 0 && airPollution.isFetchinng == false) {
            dispatch(fetchAirPollutionStatistics())
        }

        if (counties.data.length == 0 && counties.isFetchinng == false) {
            dispatch(fetchCounties())
        }

        if (usedParameters.data.length == 0 && usedParameters.isFetchinng == false) {
            dispatch(fetchParameters())
        }
    }

    render() {
        const {airPollution, usedParameters, mapCoords, counties} = this.props.state
        if (mapCoords.data.length == 0 || airPollution.data.length == 0
            || counties.data.length == 0 || usedParameters.data.length == 0) {
            return (
                <Spinner size="lg" />
            );
        }
        else {
            return (
                <div style={{overflowX: 'hidden'}}>
                    <TitleComponent titleText="Air Pollution Statistics" />

                    <Row style={{height: '80%', marginTop: '0.8em', marginBottom: '0.8em'}}>
                        <OptionPanelComponent/>
                        <MapComponent/>
                    </Row>

                    <Row style={{borderTop: '0.2em solid'}}>
                        <YearSliderComponent/>
                    </Row>
                </div>
            );
        }
    };

}
