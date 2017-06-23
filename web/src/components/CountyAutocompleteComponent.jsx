import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import { AutoComplete } from 'antd';

import {changeCountyAction} from '../actions/DisplayActions.js';
import {store} from '../stores/store';

@connect(state => state)
export default class CountyAutocompleteComponent extends Component {

  state = {
    dataSource: []
  }

  handleChange = (value) => {
    this.setState({
      dataSource: !value ? [] : this.props.state.counties.data.filter(function(element, index) {
          return element.name.includes(value)
        }).map(function(element, index) {
          return element['name'];
        })
    });
  }

  onSelectHandler = (value) => {
    console.log(value);
    const {dispatch} = store
    dispatch(changeCountyAction(value))
  }

  render() {
    const {dataSource} = this.state
    return (
      <AutoComplete
        dataSource={dataSource}
        style={{ width: '10em', height: '2.3em' }}
        placeholder="Ex: bucuresti"
        onChange={this.handleChange}
        onSelect={this.onSelectHandler}
      />
    );
  }

}
