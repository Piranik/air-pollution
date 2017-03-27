import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import { Dropdown, Button, Menu, Icon } from 'antd';

import {changeParameterAction} from '../actions/DisplayActions.js'
import { store } from '../stores/store.js'

@connect(state => state)
export default class ParametersDropdownComponent extends Component {

    static propTypes = {
        dispatch: React.PropTypes.func,
    }


    createDropdownOptions = () => {
        const params = this.props.state.usedParameters.data.map(function(element){
            return element['name'];
        });

        const params_items = params.map(function(element, index) {
            return (
                <Menu.Item key={index}>{element}</Menu.Item>
            );
        });

        return params_items;
    }

    onParametersDropdownSelect = (value) => {
        const {dispatch} = store;
        console.log('Value in handler ', value)
        dispatch(changeParameterAction(this.props.state.usedParameters.data[value.key].name))
    }

    render() {
        console.log(this.props.state.selectedParameter)
        const menu = (
            <Menu onClick={this.onParametersDropdownSelect}>
                {this.createDropdownOptions()}
            </Menu>
        )

        return (
                <Dropdown overlay={menu} trigger={['click']}>
                  <Button style={{ marginLeft: 8, width: '13em' }}>
                    {this.props.state.selectedParameter} <Icon type="down" />
                  </Button>
                </Dropdown>
        );
    }
}
