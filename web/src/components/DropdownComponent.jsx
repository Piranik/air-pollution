import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import { Dropdown, Button, Menu, Icon } from 'antd';


@connect(state => state)
export default class DropdownComponent extends Component {

    createDropdownOptions = () => {

        const dropdownOptions = this.props.dropdownOptions.map(function(element, index) {
            return (
                <Menu.Item key={index}>{element}</Menu.Item>
            );
        });

        return dropdownOptions;
    }

    render() {
        const menu = (
            <Menu onClick={this.props.onSelectHandler}>
                {this.createDropdownOptions()}
            </Menu>
        )

        return (
                <Dropdown overlay={menu} trigger={['click']}>
                  <Button style={{ marginLeft: 8, width: this.props.width }}>
                    {this.props.displayOption} <Icon type="down" />
                  </Button>
                </Dropdown>
        );
    }
}
