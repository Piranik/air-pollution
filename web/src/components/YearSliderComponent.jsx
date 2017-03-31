import { render } from 'react-dom';
import { Router, Route, Link } from 'react-router';
import { connect } from 'react-redux';
import React, { Component } from 'react';
import { Button, Alert, Spinner, Row, Col } from 'elemental';
import { Slider } from 'antd';

import { changeDisplayYear, playButtonPressed, stopButtonPressed, nextStepInTimeline } from '../actions/DisplayActions.js';
import { store } from '../stores/store.js'

const MONTHS = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

const marks = (function () {
    let marks = {}
    let currentPosition = 0;
    const step = 12;

    for (let i = 2010; i <= 2017; i ++) {
        marks[currentPosition] = {
            label: <strong>{i}</strong>
        }
        currentPosition += step;
    }
    return marks;
})();

const formatterMarks = (function() {
    let formatterMarks = {}
    const monthPrag = 1;
    let currentPosition = 0;

    for (let i = 2010; i < 2017; i ++) {
        for (let j = 0; j < 12; j ++) {
            formatterMarks[currentPosition] = i + ' ' + MONTHS[j];
            currentPosition += monthPrag;
        }
    }
    formatterMarks[currentPosition] = '2017';
    return formatterMarks;
})();

@connect(state => state)
export default class OptionPanelComponent extends Component {

    onChangeValueHandler = (value) => {
        console.log(value)
        const {dispatch} = store;
        const month = '' + value % 12;
        const year =  2010 + Math.floor(value / 12);
        dispatch(changeDisplayYear(year, month));
    }

    sliderFormatter = (value) => {
        return formatterMarks[value];
    }

    nextStepInTimeline = () => {
        const {state} = this.props;
        const {dispatch} = store;
        const nextMonth = (state.selectedMonth + 1) % 12
        let nextYear = state.selectedYear

        if (nextMonth == 0) {
            nextYear += 1;
        }

        if (state.playButtonPressed == true) {
            dispatch(nextStepInTimeline(nextYear, nextMonth));
            setTimeout(this.nextStepInTimeline, 1000);
        }
    }

    onPlayButtonHandler = () => {
        const {dispatch} = store;

        dispatch(playButtonPressed());
        setTimeout(this.nextStepInTimeline, 1000);

    }

    onStopButtonHandler = () => {
        const {dispatch} = store;
        dispatch(stopButtonPressed());
    }

    convertToMarkIndex = () => {
        const {selectedYear, selectedMonth} = this.props.state;
        console.log(selectedYear, selectedMonth);
        return (selectedYear - 2010) * 12 + Number.parseInt(selectedMonth, 10);
    }

    render() {
        return(
            <Row style={{width: '50em', margin: 'auto'}}>
                <Col
                xs="25%"
                sm="25%"
                md="25%"
                lg="25%"
                style={{
                    fontSize: '3.8em'
                }} >
                    { this.props.state.playButtonPressed == true ?
                        <span style={{color: 'red'}} onClick={this.onStopButtonHandler}> &#9612;&#9612;</span> :
                        <span style={{color: 'green'}} onClick={this.onPlayButtonHandler}> &#9658; </span>
                    }
                </Col>
                <Col
                xs="75%"
                sm="75%"
                md="75%"
                lg="75%"
                style={{
                    marginTop: '1.0em'
                }}
                >
                    <Slider max={83} marks={marks} tipFormatter={this.sliderFormatter} value={this.convertToMarkIndex()} onChange={this.onChangeValueHandler}/>
                </Col>
            </Row>
        );
    }
}
