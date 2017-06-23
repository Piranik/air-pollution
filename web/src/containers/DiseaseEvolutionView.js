import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import {Row, Col, Spinner} from 'elemental'
import { store } from '../stores/store.js'

import {fetchParameters, fetchCounties, fetchMapCoords, fetchDiseaseStatistics, fetchDiseases} from '../actions/apiActions.js'
import {isEmpty} from '../utils.jsx';

import TitleComponent from '../components/TitleComponent';
import DiseasesMapComponent from '../components/DiseasesMapComponent';
import DiseasesOptionPanelComponent from '../components/DiseasesOptionPanelComponent';
import YearSliderComponent from '../components/YearSliderComponent';

@connect(state => state)
export default class DiseaseEvolutionView extends Component {

    componentDidMount() {
        const {dispatch} = store
        const {diseaseStatistics, usedParameters, mapCoords, counties,
            diseases} = this.props.state;

        if (mapCoords.data.length == 0 && mapCoords.isFetching == false) {
            dispatch(fetchMapCoords());
        }

        if (diseaseStatistics.data.length == 0 && diseaseStatistics.isFetching == false) {
            dispatch(fetchDiseaseStatistics());
        }

        if (counties.data.length == 0 && counties.isFetching == false) {
            dispatch(fetchCounties());
        }

        if (usedParameters.data.length == 0 && usedParameters.isFetching == false) {
            dispatch(fetchParameters());
        }
        if (isEmpty(diseases.classification) || isEmpty(diseases.codification)) {
            dispatch(fetchDiseases());
        }
    }

    render() {
        const {diseaseStatistics, usedParameters, mapCoords, counties} = this.props.state
        if (mapCoords.data.length == 0 || diseaseStatistics.data.length == 0
            || counties.data.length == 0 || usedParameters.data.length == 0) {
            return (
                <Spinner size="lg" />
            );
        }
        else {
            return (
                <div style={{overflowX: 'hidden'}}>
                    <TitleComponent titleText="Diseases Statistics" />

                    <Row style={{height: '80%', marginTop: '0.8em', marginBottom: '0.8em'}}>
                        <DiseasesOptionPanelComponent/>
                        <DiseasesMapComponent/>
                    </Row>
                    <Row style={{borderTop: '0.2em solid'}}>
                        <YearSliderComponent startYear={2012} endYear={2017} lastMonths={1}/>
                    </Row>
                </div>
            );
        }
    };

}
