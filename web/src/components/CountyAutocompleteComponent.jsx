import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { connect } from 'react-redux'
import React, { Component } from 'react'

import { AutoComplete } from 'antd';

function onSelect(value) {
  console.log('onSelect', value);
}

export default class OptionPanelComponent extends Component {

  state = {
    dataSource: [],
  }

  handleChange = (value) => {
    this.setState({
      dataSource: !value ? [] : [
        value,
        value + value,
        value + value + value,
      ],
    });
  }

  render() {
    const { dataSource } = this.state;
    console.log(dataSource)
    return (
      <AutoComplete
        dataSource={dataSource}
        style={{ width: '10em', height: '2.3em' }}
        placeholder="input here"
        onChange={this.handleChange}
        onSelect={onSelect}
      />
    );
  }

}
