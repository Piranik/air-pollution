import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import './WelcomeViewStyle.css'
import '../styles/elementalUIStyles.min.css'
import { Button, Alert, Spinner, Row, Col } from 'elemental'



@connect(state => state)
export default class MainView extends Component {
    render() {
        return (
            <div className="welcomeViewScreen">
                <Row style={{ paddingTop: '10em' }}>
                    <Col xs="75%" sm="75%" md="75%" lg="75%">
                    </Col>
                    <Col xs="25%" sm="25%" md="25%" lg="25%">
                        <Link style={{ textDecoration: 'none', color: 'white', textSize: '2.5em' }} to="/air/disease-evolution">
                            <Button type="hollow-primary" size="lg" style={{width: '15em', height: '5em'}}>
                                    Disease Evolution
                            </Button>
                        </Link>
                    </Col>
                </Row>
                <Row style={{ marginTop: '8em' }}>
                    <Col xs="75%" sm="75%" md="75%" lg="75%">
                    </Col>
                    <Col xs="25%" sm="25%" md="25%" lg="25%">
                        <Link style={{ textDecoration: 'none' }} to="/air/air-pollution">
                            <Button type="hollow-primary" size="lg" style={{width: '15em', height: '5em'}}>
                                Air Pollution
                            </Button>
                        </Link>
                    </Col>
                </Row>
            </div>
        );
    };
}
