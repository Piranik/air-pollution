import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import {Row, Col} from 'elemental'


import TitleComponent from '../components/TitleComponent'
import MapComponent from '../components/MapComponent'
import OptionPanelComponent from '../components/OptionPanelComponent'
import YearSliderComponent from '../components/YearSliderComponent'


@connect(state => state)
export default class AirPollutionView extends Component {

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
