import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'

import MapComponent from '../components/MapComponent'

@connect(state => state)
export default class DiseaseEvolutionView extends Component {

    render() {
        return (
            // <Link to="/air-pollution">Air Pollution</Link>
            <MapComponent />
        );
    };

}
