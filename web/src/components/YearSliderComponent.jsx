import { render } from 'react-dom';
import { Router, Route, Link } from 'react-router';
import { connect } from 'react-redux';
import React, { Component } from 'react';
import { Button, Alert, Spinner, Row, Col } from 'elemental';
import { Slider } from 'antd';

import { changeDisplayYear } from '../actions/DisplayActions.js';
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
        const month = value % 12;
        const year =  2010 + Math.floor(value / 12);
        dispatch(changeDisplayYear(year, month));
    }

    sliderFormatter = (value) => {
        return formatterMarks[value];
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
                    color: 'green',
                    fontSize: '3.8em'
                }}>
                    &#9658;
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
                    <Slider max={84} marks={marks} tipFormatter={this.sliderFormatter} defaultValue={24} onChange={this.onChangeValueHandler}/>
                </Col>
            </Row>
        );
    }
}
