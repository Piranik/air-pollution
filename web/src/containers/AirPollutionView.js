import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import {Row, Col} from 'elemental'
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
        return (
            <div style={{overflowX: 'hidden'}}>
                <TitleComponent titleText="Air Pollution Statistics" />

                <Row style={{height: '82%', background: 'brown'}}>
                    <MapComponent/>
                    <OptionPanelComponent/>
                </Row>
                <Row>
                    <YearSliderComponent/>
                </Row>
            </div>
        );
    };

}
