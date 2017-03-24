import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import { Button, Alert, Spinner, Row, Col } from 'elemental'
import { Slider } from 'antd'

const marks = {
    0: {
        label: <strong>2010</strong>
    },
    14.28: {
        label: <strong>2011</strong>
    },
    28.56: {
        label: <strong>2012</strong>
    },
    42.84: {
        label: <strong>2013</strong>
    },
    57.12: {
        label: <strong>2014</strong>
    },
    71.4: {
        label: <strong>2015</strong>
    },
    84.68: {
        label: <strong>2016</strong>
    },
    100: {
        label: <strong>2017</strong>
    },
};



@connect(state => state)
export default class OptionPanelComponent extends Component {

    render() {
        return(
            <Row style={{width: '60em', margin: 'auto'}}>
                <Col
                xs="25%"
                sm="25%"
                md="25%"
                lg="25%"
                style={{
                    color: 'green',
                    fontSize: '5.8em'
                }}>
                    &#9658;
                </Col>
                <Col
                xs="75%"
                sm="75%"
                md="75%"
                lg="75%"
                style={{
                    marginTop: '2.5em'
                }}
                >
                    <Slider marks={marks} defaultValue={28.56} />
                </Col>
            </Row>
        );
    }
}
