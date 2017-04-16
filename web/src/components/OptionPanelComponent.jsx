import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'

import { Button, Alert, Spinner, Row, Col } from 'elemental'

import '../styles/elementalUIStyles.min.css'

import CountyAutocompleteComponent from '../components/CountyAutocompleteComponent'
import ParametersDropdownComponent from '../components/ParametersDropdownComponent'


@connect(state => state)
export default class OptionPanelComponent extends Component {

    static propTypes = {
        dispatch: React.PropTypes.func,
    }

    onParametersDropdownSelect = (value) => {
        console.log(value)
    }

    render() {
        const params = this.props.state.usedParameters.data.map(function(element){
            return element['name'];
        });

        return (
            <Col
            xs="18%"
            sm="18%"
            md="18%"
            lg="18%"
            style={{
                textAlign: 'center',
                backgroundColor: '#BAD1D0',
                height: '50%',
                border: "5px solid",
                borderRadius: "2em",
                marginLeft: '2.5em',
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
                        Select Parameter
                    </Col>
                </Row>
                <Row>
                    <Col style={{margin: 'auto', marginTop: '2.5em'}}>
                        <ParametersDropdownComponent />
                    </Col>
                </Row>
            </Col>
        );
    }
}
