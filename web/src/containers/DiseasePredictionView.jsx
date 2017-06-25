import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import {Row, Col, Spinner} from 'elemental'
import { store } from '../stores/store.js'

import {fetchDiseaseStatistics, fetchDiseases, fetchPredictionInfo} from '../actions/apiActions.js'
import {isEmpty} from '../utils.jsx';

import TitleComponent from '../components/TitleComponent';
import PredictionPanelComponent from '../components/PredictionPanelComponent';

@connect(state => state)
export default class DiseasePredictionView extends Component {

    componentDidMount() {
        const {dispatch} = store;
        const {diseases, diseaseStatistics, prediction} = this.props.state

        if (isEmpty(diseaseStatistics.boundaries)) {
            dispatch(fetchDiseaseStatistics())
        }

        if (isEmpty(diseases.codification) || prediction.selectedDisease == null) {
            dispatch(fetchDiseases());
        }

        console.log(this.props.state)
        if (prediction.tools.length === 0 && isEmpty(prediction.toolsCodification) && isEmpty(prediction.toolsScores)) {
            dispatch(fetchPredictionInfo());
        }

    }

    render() {
        const {diseases, diseaseStatistics, prediction} = this.props.state
        if (isEmpty(diseases.codification) || isEmpty(diseaseStatistics.boundaries) || prediction.tools.length === 0 || isEmpty(prediction.toolsCodification) || isEmpty(prediction.toolsScores) || prediction.selectedDisease == null || diseases.isFetching || prediction.isFetching) {
            console.log(this.props.state)
            return (
                <Row style={{ width: '99%', paddingTop: '30em', paddingLeft: '50em'}}>
                    <Spinner
                        type="primary"
                        size="lg"/>
                </Row>
            );
        }
        else {
            return (
                <div style={{overflowX: 'hidden'}}>
                    <TitleComponent titleText="Disease Predictions" />

                    <Row style={{height: '70%', marginTop: '4em', marginLeft: '7em'}}>
                        <PredictionPanelComponent/>
                    </Row>

                </div>
            );
        }
    };

}
