import { Router, Route, Link } from 'react-router';
import { connect } from 'react-redux';
import React, { Component } from 'react';
import { Button, Alert, Spinner, Row, Col, FormInput} from 'elemental';

import DropdownComponent from '../components/DropdownComponent';

import {changeToolAction, changePredictedDiseaseAction, changeMonthsAction, changeAqiAction, changeWindAction, changeRainfallAction, changePressureAction, changeTempAction, changeDiseaseClassAction} from '../actions/DisplayActions.js';
import {fetchPredictionResult} from '../actions/apiActions.js';

import {diseasesColors} from '../utils.jsx';

import { store } from '../stores/store.js';

const RESULT_VALUES = ['Good', 'Medium', 'Hard'];

@connect(state => state)
export default class PredictionPanelComponent extends Component {

    getResultElement = () => {
        const {prediction} = this.props.state;
        if (prediction.result == null) {
            return (
                <Col xs="100%" sm="100%" md="100%" lg="100%" style={{border: '0.5em solid black', borderRadius: '25%', backgroundColor: this.getResultColor()}}>
                    <div style={{fontSize: '6.5em', textAlign: 'center', color: '#EAEFBD', height: '2em', marginTop: '0.4em'}}>
                    {'...'} </div>
                </Col>
            );
        }
        else {
            return (
                <Col xs="100%" sm="100%" md="100%" lg="100%" style={{border: '0.5em solid black', borderRadius: '25%', backgroundColor: this.getResultColor()}}>
                    <div style={{fontSize: '6.5em', textAlign: 'center', color: '#EAEFBD', height: '2em', marginTop: '0.4em'}}> {RESULT_VALUES[prediction.result]} </div>
                </Col>
            );
        }
    }

    getValueFromOption = (option) => {
        if (option == null) {
            return null;
        }

        return parseInt(option.substring(0, 1), 10);
    }

    getResultColor = () => {
        const {prediction} = this.props.state;
        let color = 'white';

        if (prediction.result != null) {
            color = diseasesColors[prediction.result];
        }
        return color;
    }

    isButtonDisabled = () => {
        const {prediction} = this.props.state;
        if (prediction.selectedDiseaseClass == null) {
            return true;
        }

        if (prediction.selectedAqi == null) {
            return true;
        }

        if (prediction.selectedWind == null) {
            return true;
        }

        if (prediction.selectedPressure == null) {
            return true;
        }

        if (prediction.selectedRainfall == null) {
            return true;
        }

        if (prediction.selectedTemperature == null) {
            return true;
        }

        return false;
    }

    onPredictionToolChange = (selectedOption) => {
        const {dispatch} = store;
        const {prediction} = this.props.state;
        dispatch(changeToolAction(prediction.tools[selectedOption.key]));
    }

    onDiseaseChange = (selectedOption) => {
        const {dispatch} = store;
        const {prediction} = this.props.state;
        dispatch(changePredictedDiseaseAction(prediction.allDiseases[selectedOption.key]));
    }

    onMonthChange = (selectedOption) => {
        const {dispatch} = store;
        dispatch(changeMonthsAction(this.diseasesMonths[selectedOption.key]));
    }

    onAqiChange = (selectedOption) => {
        const {dispatch} = store;
        dispatch(changeAqiAction(this.aqiOptions[selectedOption.key]));
    }

    onWindChange = (selectedOption) => {
        const {dispatch} = store;
        dispatch(changeWindAction(this.windOptions[selectedOption.key]));
    }

    onPressureChange = (selectedOption) => {
        const {dispatch} = store;
        dispatch(changePressureAction(this.pressureOptions[selectedOption.key]));
    }

    onRainfallChange = (selectedOption) => {
        const {dispatch} = store;
        dispatch(changeRainfallAction(this.rainfallOptions[selectedOption.key]));
    }

    onTemperatureChange = (selectedOption) => {
        const {dispatch} = store;
        dispatch(changeTempAction(this.tempOptions[selectedOption.key]));
    }

    onDiseaseClassChange = (selectedOption) => {
        const {dispatch} = store;
        dispatch(changeDiseaseClassAction(this.computeDiseaseOptions()[selectedOption.key]));
    }

    predictButtonHandler = () => {
        const {prediction} = this.props.state;
        const {dispatch} = store;

        dispatch(fetchPredictionResult(
            prediction.toolsCodification[prediction.selectedTool],
            prediction.selectedDisease,
            prediction.selectedMonths,
            this.getValueFromOption(prediction.selectedAqi),
            this.getValueFromOption(prediction.selectedWind),
            this.getValueFromOption(prediction.selectedPressure),
            this.getValueFromOption(prediction.selectedRainfall),
            this.getValueFromOption(prediction.selectedTemperature),
            this.getValueFromOption(prediction.selectedDiseaseClass)
            ));
    }

    aqiOptions = ['1 - Excelent', '2 - Very good', '3 - Good', '4 - Medium', '5 - Bad', '6 - Very Bad'];
    windOptions = ['0 - (< 10km/h)', '1 - (10 - 20 km/h)', '2 (20 - 35 km/h)', '3 (35 - 40 km/h)', '4 (> 40 km/h)'];
    pressureOptions = ['0 - (< 745mb)', '1 - (745 - 760mb)', '2 - (760 - 770mb)', '3 - (770 - 775mb)', '4 - (> 775mb)'];
    rainfallOptions = ['0 - very low', '1 - low', '2 - medium', '3 - high', '4 - very high'];
    tempOptions = ['0 - very cold', '1 - cold', '2 - medium', '3 - warm', '4 - very warm'];

    diseasesMonths = [1, 2, 3, 4, 5];

    computeDiseaseOptions = () => {
        const {prediction, diseases, diseaseStatistics} = this.props.state
        const selectedDiseaseIndex = diseases.codification[prediction.selectedDisease]
        const diseaseBoundaries = diseaseStatistics.boundaries[selectedDiseaseIndex]
        const diseaseOptions = [
            '0 - (< ' + diseaseBoundaries[0] + ')',
            '1 - (' + diseaseBoundaries[0] + '-' + diseaseBoundaries[1] + ')',
            '2 - (> ' + diseaseBoundaries[1] + ')'];
        return diseaseOptions;
    }

    render() {
        const {prediction, diseases, diseaseStatistics} = this.props.state
        const diseaseOptions = this.computeDiseaseOptions()
        const predictionsTools = prediction.tools;
        console.log(this.props.state.prediction)
        return (
            <Row style={{width: '100%', height: '100%', color: '#5E6472'}}>
                <Col xs="47%" sm="47%" md="47%" lg="47%" style={{border: '0.6em solid black', borderRadius: '10%', backgroundColor: '#C9E3AC'}}>
                    <Row>
                        <Col xs="70%" sm="70%" lg="70%" style={{borderBottom: '0.3em solid black',
                        borderRight: '0.3em solid black', fontSize: '1.4em'}}>
                            <Row style={{marginTop: '1em'}}>
                                <Col xs="40%" sm="40%" md="40%" lg="40%" style={{textAlign: 'right'}}>
                                    Select Tool:
                                </Col>
                                <Col xs="60%" sm="60%" md="60%" lg="60%" style={{textAlign: 'left'}}>
                                    <DropdownComponent onSelectHandler={this.onPredictionToolChange} dropdownOptions={predictionsTools} displayOption={prediction.selectedTool}
                                        width={'17em'}
                                    />
                                </Col>
                            </Row>

                            <Row style={{marginTop: '0.5em'}}>
                                <Col xs="40%" sm="40%" md="40%" lg="40%" style={{textAlign: 'right'}}>
                                    Select Disease:
                                </Col>
                                <Col xs="60%" sm="60%" md="60%" lg="60%" style={{textAlign: 'left'}} >
                                    <DropdownComponent
                                        onSelectHandler={this.onDiseaseChange}
                                        dropdownOptions={prediction.allDiseases}
                                        displayOption={prediction.selectedDisease}
                                        width={'17em'}
                                    />
                                </Col>
                            </Row>

                            <Row style={{marginBottom: '1em', marginTop: '0.5em'}}>
                                <Col xs="40%" sm="40%" md="40%" lg="40%" style={{textAlign: 'right'}}>
                                    Select Months:
                                </Col>
                                <Col xs="60%" sm="60%" md="60%" lg="60%" style={{textAlign: 'left'}}>
                                    <DropdownComponent
                                        onSelectHandler={this.onMonthChange}
                                        dropdownOptions={this.diseasesMonths}
                                        displayOption={prediction.selectedMonths}
                                        width={'5em'}
                                    />
                                </Col>
                            </Row>
                        </Col>
                        <Col xs="30%" sm="30%" lg="30%" style={{borderBottom: '0.3em solid black',
                            borderTopRightRadius: '3.85em', backgroundColor: '#F2E7C9'}}>
                            <Row>
                                <Col xs="100%" sm="100%" md="100%" lg="100%" style={{fontSize: '2em', textAlign: 'center', marginTop: '0.2em'}}>

                                    Accuracy
                                </Col>
                            </Row>
                            <Row>
                                <Col xs="100%" sm="100%" md="100%" lg="100%" style={{fontSize: '3.3em', textAlign: 'center', marginTop: '0.2em'}}>
                                    {(prediction.toolsScores[prediction.selectedMonths][prediction.selectedDisease][prediction.toolsCodification[prediction.selectedTool]].toFixed(4) * 100).toFixed(2)} %
                                </Col>
                            </Row>
                        </Col>
                    </Row>
                    <Row style={{fontSize: '1.4em', marginTop: '2em'}}>
                        <Col xs="50%" sm="50%" md="50%" lg="50%" style={{textAlign: 'right'}}>
                            Disease Class:
                        </Col>
                        <Col xs="50%" sm="50%" md="50%" lg="50%">
                            <DropdownComponent
                                onSelectHandler={this.onDiseaseClassChange}
                                dropdownOptions={diseaseOptions}
                                displayOption={prediction.selectedDiseaseClass || "Disease Class"}
                                width={'10em'}
                            />
                        </Col>
                    </Row>

                    <Row style={{fontSize: '1.4em', marginTop: '0.85em'}}>
                        <Col xs="50%" sm="50%" md="50%" lg="50%" style={{textAlign: 'right'}}>
                            Air Quality Index:
                        </Col>
                        <Col xs="49%" sm="49%" md="49%" lg="49%">
                            <DropdownComponent
                                onSelectHandler={this.onAqiChange}
                                dropdownOptions={this.aqiOptions}
                                displayOption={prediction.selectedAqi || "AQI"}
                                width={'10em'}
                            />
                        </Col>
                    </Row>

                    <Row style={{fontSize: '1.4em', marginTop: '0.85em'}}>
                        <Col xs="50%" sm="50%" md="50%" lg="50%" style={{textAlign: 'right'}}>
                            Wind speed Class:
                        </Col>
                        <Col xs="50%" sm="50%" md="50%" lg="50%">
                           <DropdownComponent
                                onSelectHandler={this.onWindChange}
                                dropdownOptions={this.windOptions}
                                displayOption={prediction.selectedWind || "Wind"}
                                width={'12em'}
                            />
                        </Col>
                    </Row>

                    <Row style={{fontSize: '1.4em', marginTop: '0.85em'}}>
                        <Col xs="50%" sm="50%" md="50%" lg="50%" style={{textAlign: 'right'}}>
                            Pressure Class:
                        </Col>
                        <Col xs="50%" sm="50%" md="50%" lg="50%">
                            <DropdownComponent
                                onSelectHandler={this.onPressureChange}
                                dropdownOptions={this.pressureOptions}
                                displayOption={prediction.selectedPressure || "Pressure"}
                                width={'12em'}
                            />
                        </Col>
                    </Row>

                    <Row style={{fontSize: '1.4em', marginTop: '0.85em'}}>
                        <Col xs="50%" sm="50%" md="50%" lg="50%" style={{textAlign: 'right'}}>
                            Rainfall Class:
                        </Col>
                        <Col xs="50%" sm="50%" md="50%" lg="50%">
                        <DropdownComponent
                                onSelectHandler={this.onRainfallChange}
                                dropdownOptions={this.rainfallOptions}
                                displayOption={prediction.selectedRainfall || "Rainfall"}
                                width={'10em'}
                            />
                        </Col>
                    </Row>

                    <Row style={{fontSize: '1.4em', marginTop: '0.85em'}}>
                        <Col xs="50%" sm="50%" md="50%" lg="50%" style={{textAlign: 'right'}}>
                            Temperature Class:
                        </Col>
                        <Col xs="50%" sm="50%" md="50%" lg="50%">
                            <DropdownComponent
                                onSelectHandler={this.onTemperatureChange}
                                dropdownOptions={this.tempOptions}
                                displayOption={prediction.selectedTemperature || "Temperature"}
                                width={'10em'}
                            />
                        </Col>
                    </Row>

                </Col>
                <Col xs="20%" sm="20%" md="20%" lg="20%">
                    <Button type="success" size="lg" style={{marginTop: '9em', marginLeft: '1.2em', marginRight: '1.2em', fontSize: '2em', backgroundColor: '#226764'}} onClick={this.predictButtonHandler} disabled={this.isButtonDisabled()}>Predict =></Button>
                </Col>
                <Col xs="25%" sm="25%" md="25%" lg="25%">
                    <Row style={{marginTop: '2em'}}>
                        <Col xs="100%" sm="100%" md="100%" lg="100%" style={{fontSize: '4em', textAlign: 'center', color: '#9D8189'}}>
                            RESULT
                        </Col>
                    </Row>
                    <Row style={{marginTop: '4em'}}>
                        {this.getResultElement()}
                    </Row>
                </Col>
            </Row>
        );
    }

}
