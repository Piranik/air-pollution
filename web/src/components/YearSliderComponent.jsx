import { render } from 'react-dom';
import { Router, Route, Link } from 'react-router';
import { connect } from 'react-redux';
import React, { Component } from 'react';
import { Button, Alert, Spinner, Row, Col } from 'elemental';
import { Slider } from 'antd';

import { changeDisplayYear, playButtonPressed, stopButtonPressed, nextStepInTimeline, stopTimeline } from '../actions/DisplayActions.js';
import { store } from '../stores/store.js'

const MONTHS = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];


@connect(state => state)
export default class YearSliderComponent extends Component {

    marks = (function (startYear, endYear) {
        let marks = {}
        let currentPosition = 0;
        const step = 12;

        for (let i = startYear; i <= endYear; i ++) {
            marks[currentPosition] = {
                label: <strong>{i}</strong>
            }
            currentPosition += step;
        }
        return marks;
    })(this.props.startYear, this.props.endYear);

    formatterMarks = (function(startYear, endYear) {
        let formatterMarks = {}
        const monthPrag = 1;
        let currentPosition = 0;

        for (let i = startYear; i < endYear; i ++) {
            for (let j = 0; j < 12; j ++) {
                formatterMarks[currentPosition] = i + ' ' + MONTHS[j];
                currentPosition += monthPrag;
            }
        }
        formatterMarks[currentPosition] = '' + endYear;
        return formatterMarks;
    })(this.props.startYear, this.props.endYear);

    onChangeValueHandler = (value) => {
        const {dispatch} = store;
        const {startYear} = this.props;
        const month = value % 12;
        const year =  startYear + Math.floor(value / 12);

        dispatch(changeDisplayYear(year, month));
    }

    sliderFormatter = (value) => {
        return this.formatterMarks[value];
    }

    nextStepInTimeline = () => {
        const {state, startYear, endYear} = this.props;
        const {dispatch} = store;
        let nextMonth = (state.selectedMonth + 1) % 12

        let nextYear = state.selectedYear

        if (nextMonth == 0) {
            nextYear += 1;
        }

        if ((nextMonth == 12 - this.props.lastMonths + 1) && (nextYear == this.props.endYear - 1)) {
            nextMonth = 0
            nextYear = this.props.startYear;
            dispatch(nextStepInTimeline(nextYear, nextMonth));
            dispatch(stopTimeline());
        }

        if (state.playButtonPressed == true && nextYear < endYear ) {
            dispatch(nextStepInTimeline(nextYear, nextMonth));
            setTimeout(this.nextStepInTimeline, 1000);
        }
        else {
            dispatch(stopTimeline());
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
        const {startYear, endYear} = this.props;
        const {selectedYear, selectedMonth} = this.props.state;
        return (selectedYear - startYear) * 12 + Number.parseInt(selectedMonth, 10);
    }

    render() {
        const max = (this.props.endYear - this.props.startYear) * 12 - this.props.lastMonths;
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
                    <Slider max={max} marks={this.marks} tipFormatter={this.sliderFormatter} value={this.convertToMarkIndex()} onChange={this.onChangeValueHandler} disabled={this.props.state.interfaceDisabled}/>
                </Col>
            </Row>
        );
    }
}
