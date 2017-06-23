import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'

import { Button, Alert, Spinner, Row, Col } from 'elemental'

import '../styles/elementalUIStyles.min.css'

import CountyAutocompleteComponent from '../components/CountyAutocompleteComponent';
import DropdownComponent from '../components/DropdownComponent';
import {changeDiseaseCategory, changeDiseaseAction} from '../actions/DisplayActions.js';
import { store } from '../stores/store.js';


@connect(state => state)
export default class DiseasesOptionPanelComponent extends Component {

    static propTypes = {
        dispatch: React.PropTypes.func,
    }

    onDiseaseCategoryChange = (value) => {
        const {dispatch} = store;
        const {diseases} = this.props.state;
        const newCategory = Object.keys(diseases.classification)[value.key];
        dispatch(changeDiseaseCategory(newCategory));
        dispatch(changeDiseaseAction(diseases.classification[newCategory][0]));
    }

    onDiseaseChange = (value) => {
        const {dispatch} = store;
        const {diseases, selectedDiseaseCategory} = this.props.state;
        const newDisease = diseases.classification[selectedDiseaseCategory][value.key]
        dispatch(changeDiseaseAction(newDisease));
    }

    render() {
        const {diseases, selectedDiseaseCategory} = this.props.state;
        const diseasesCategories = Object.keys(diseases.classification);
        const diseasesForCategory = diseases.classification[selectedDiseaseCategory];
        return (
            <Col
            xs="18%"
            sm="18%"
            md="18%"
            lg="18%"
            style={{
                textAlign: 'center',
                backgroundColor: '#C9E3AC',
                height: '70%',
                border: "5px solid",
                borderRadius: "2em",
                marginLeft: '1.5em',
                marginRight: '1em',
                marginTop: '6.5em'
                }}>
                <Row>
                    <Col style={{textAlign : 'center', margin: 'auto', marginTop: '2.5em', color: '#226764'}}>
                        Select County
                    </Col>
                </Row>
                <Row>
                    <Col style={{margin: 'auto', marginTop: '2.5em'}}>
                        <CountyAutocompleteComponent />
                    </Col>
                </Row>
                <Row>
                    <Col style={{textAlign : 'center', margin: 'auto', marginTop: '2.5em', color: '#226764'}}>
                        Select Disease Category
                    </Col>
                </Row>
                <Row>
                    <Col style={{margin: 'auto', marginTop: '2.5em'}}>
                        <DropdownComponent onSelectHandler={this.onDiseaseCategoryChange} dropdownOptions={diseasesCategories} displayOption={this.props.state.selectedDiseaseCategory} width={'16em'}/>
                    </Col>
                </Row>

                <Row>
                    <Col style={{textAlign : 'center', margin: 'auto', marginTop: '2.5em', color: '#226764'}}>
                        Select Disease
                    </Col>
                </Row>
                <Row>
                    <Col style={{margin: 'auto', marginTop: '2.5em'}}>
                        <DropdownComponent onSelectHandler={this.onDiseaseChange} dropdownOptions={diseasesForCategory} displayOption={this.props.state.selectedDisease}
                            width={'16em'}
                            />
                    </Col>
                </Row>

            </Col>
        );
    }
}
