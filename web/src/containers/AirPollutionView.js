import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import {Row, Col, Spinner} from 'elemental'
import { store } from '../stores/store.js'

import {fetchParameters, fetchCounties, fetchMapCoords, fetchAirPollutionStatistics} from '../actions/apiActions.js'


import TitleComponent from '../components/TitleComponent';
import PollutionMapComponent from '../components/PollutionMapComponent';
import PollutionOptionPanelComponent from '../components/PollutionOptionPanelComponent';
import YearSliderComponent from '../components/YearSliderComponent';

@connect(state => state)
export default class AirPollutionView extends Component {

    componentDidMount() {
        const {dispatch} = store
        const {airPollution, usedParameters, mapCoords, counties} = this.props.state

        if (mapCoords.data.length == 0 && mapCoords.isFetching == false) {
            dispatch(fetchMapCoords())
        }

        if (airPollution.data.length == 0 && airPollution.isFetching == false) {
            dispatch(fetchAirPollutionStatistics())
        }

        if (counties.data.length == 0 && counties.isFetching == false) {
            dispatch(fetchCounties())
        }

        if (usedParameters.data.length == 0 && usedParameters.isFetching == false) {
            dispatch(fetchParameters())
        }
    }

    render() {
        const {airPollution, usedParameters, mapCoords, counties} = this.props.state
        if (mapCoords.data.length == 0 || airPollution.data.length == 0
            || counties.data.length == 0 || usedParameters.data.length == 0) {
            console.log('loading ...')
            return (
                <Spinner size="lg" />
            );
        }
        else {
            return (
                <div style={{overflowX: 'hidden'}}>
                    <TitleComponent titleText="Air Pollution Statistics" />

                    <Row style={{height: '80%', marginTop: '0.8em', marginBottom: '0.8em'}}>
                        <PollutionOptionPanelComponent/>
                        <PollutionMapComponent/>
                    </Row>

                    <Row style={{borderTop: '0.2em solid'}}>
                        <YearSliderComponent startYear={2010} endYear={2017} lastMonths={2}/>
                    </Row>
                </div>
            );
        }
    };

}
