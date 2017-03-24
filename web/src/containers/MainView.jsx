import React, { Component } from 'react'
import { connect } from 'react-redux'
import AppBar from 'material-ui/AppBar';
import NavigationClose from 'material-ui/svg-icons/navigation/close';
import ShoppingCart from 'material-ui/svg-icons/action/shopping-cart';

import FlatButton from 'material-ui/FlatButton';
import Badge from 'material-ui/Badge';
import IconButton from 'material-ui/IconButton';
import NotificationsIcon from 'material-ui/svg-icons/social/notifications';
import RaisedButton from 'material-ui/RaisedButton';

// import ListComponent from '../components/ListComponent.js'
import {store} from '../stores/store.js';

import { finalize_order } from '../actions/shopActions';

const styles = {
  title: {
    cursor: 'pointer',
  },
  icon_cart_size: {
    width: 40,
    height: 40,
    marginRight: 30
  },
  button: {
    margin: 12,
    backgroundColor: 'red'
  }
};


@connect(state => state)
export default class MainView extends Component {

  static propTypes = {
    dispatch: React.PropTypes.func,
    categories: React.PropTypes.object
  }

  finalizeHandler = () => {
      window.alert("Order with value of " + this.props.state.total + " RON was placed succesfully");
      store.dispatch(finalize_order());
  }

  render () {
    return (
      <div>
          <AppBar
              style={{position: 'fixed', top: 0}}
              title={<span style={styles.title}>Newspapers of the day</span>}
              iconElementLeft={<IconButton><NavigationClose /></IconButton>}
              iconElementRight={
                <Badge
                    badgeStyle={{fontSize: '1.5em', marginRight: 60}}
                    badgeContent={this.props.state.total+'RON'}
                    primary={true}
                >
                    <ShoppingCart style={styles.icon_cart_size} />
                </Badge>
              }
            />

          <AppBar
              style={{position: 'fixed', top: 572}}
              iconElementLeft = {
                <IconButton iconClassName="muidocs-icon-custom-github" disabled={true} />
              }
              iconElementRight={
                  <RaisedButton disabled={(this.props.state.total == 0)} label="Finalize order" primary={true} style={styles.button} onClick={this.finalizeHandler}/>
              }
            />
      </div>
      );
  }
}
