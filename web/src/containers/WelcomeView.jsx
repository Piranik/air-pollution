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
                <Row style={{ width: '100%', paddingTop: '10em' }}>
                    <Col xs="70%" sm="70%" md="70%" lg="70%">
                    </Col>
                    <Col xs="30%" sm="30%" md="30%" lg="30%">
                        <Link style={{ textDecoration: 'none', color: 'white', textSize: '2.5em' }} to="/air/disease-evolution">
                            <Button type="hollow-primary" size="lg" style={{width: '15em', height: '5em', color: '#41F6FE'}}>
                                    Disease Evolution
                            </Button>
                        </Link>
                    </Col>
                </Row>
                <Row style={{ width: '100%',  paddingTop: '8em' }}>
                    <Col xs="70%" sm="70%" md="70%" lg="70%">
                    </Col>
                    <Col xs="30%" sm="30%" md="30%" lg="30%">
                        <Link style={{ textDecoration: 'none'}} to="/air/air-pollution">
                            <Button type="hollow-primary" size="lg" style={{width: '15em', height: '5em', color: '#41F6FE'}}>
                                Air Pollution
                            </Button>
                        </Link>
                    </Col>
                </Row>
                <Row style={{ width: '100%',  paddingTop: '8em' }}>
                    <Col xs="70%" sm="70%" md="70%" lg="70%">
                    </Col>
                    <Col xs="30%" sm="30%" md="30%" lg="30%">
                        <Link style={{ textDecoration: 'none' }} to="/air/disease-prediction">
                            <Button type="hollow-primary" size="lg" style={{width: '15em', height: '5em', color: '#41F6FE'}}>
                                Disease Prediction
                            </Button>
                        </Link>
                    </Col>
                </Row>
            </div>
        );
    };
}
