import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'

import { Button, Alert, Spinner, Row, Col } from 'elemental'

import '../styles/elementalUIStyles.min.css'

@connect(state => state)
export default class TitleComponent extends Component {
    static propTypes = {
        dispatch: React.PropTypes.func,
        titleText: React.PropTypes.string
    }

    render() {
        return (
            <div>
                <Row style={{width: '100%', height: '4.5em', backgroundColor: '#226764'}}>
                    <Col xs="25%" sm="25%" md="25%" lg="25%"></Col>
                    <Col xs="50%" sm="50%" md="50%" lg="50%" style={{textAlign: 'center', fontSize: '3em', marginTop: '0.1em', color: '#BAD1D0'}}>
                        {this.props.titleText}
                    </Col>
                    <Col xs="25%" sm="25%" md="25%" lg="25%"></Col>
                </Row>
            </div>
        );
    }

}
