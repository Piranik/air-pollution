import 'bootstrap-webpack';
import React, { Component } from 'react'
import { connect } from 'react-redux'

import {List, ListItem} from 'material-ui/List';
import Divider from 'material-ui/Divider';
import Subheader from 'material-ui/Subheader';
import Avatar from 'material-ui/Avatar';
import {grey400, darkBlack, lightBlack} from 'material-ui/styles/colors';
import IconButton from 'material-ui/IconButton';
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';
import IconMenu from 'material-ui/IconMenu';
import Checkbox from 'material-ui/Checkbox';
import CheckCircle from 'material-ui/svg-icons/action/check-circle';
import ActionFavoriteBorder from 'material-ui/svg-icons/action/favorite-border';

import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import { store } from '../stores/store.js'

import {toggle_in_cart, add_addon, finalize_order} from '../actions/shopActions.js';


const styles = {
  block: {
    maxWidth: 250,
  },
  icon_size: {
    width: 96,
    height: 96,
    paddingBottom: 24,
    paddingLeft: 24,
    paddingRight: 24,
  },
  value: 0,
  style: {
  	width: 200
  }
};

@connect(state => state)
export default class ListComponent extends Component {

	render() {
		console.log(this.props.state.total)
		return (
			<List style={{marginTop: 75, marginBottom: 55}}>
		 		{this.props.state.newspapers.data.map(this.listItem)}
		 	</List>
		)
	}


	handleOnClick = (index) => {
		console.log('Am apasat')
		store.dispatch(toggle_in_cart(index))
	}

	listItem = (newspaper, index) => {
		return (
			<div key={index} >
				<ListItem 
					leftCheckbox={
						<Checkbox
      						checkedIcon={<CheckCircle />}
      						uncheckedIcon={<CheckCircle />}
      						checked={newspaper.selected}
							onCheck={this.handleOnClick.bind(this, index)}
							iconStyle={styles.icon_size}
    					/>
    				}
    				rightToggle={
    					  <SelectField
					          floatingLabelText="Add on"
					          style={styles.style}
					          value={newspaper.addon_selected}
					          disabled={!newspaper.selected}
					          onChange={(event, addon_index, value) => {
									store.dispatch(add_addon(addon_index, index))
								}
							  }
					        >
					        	<MenuItem value={0} primaryText="None" />
					          	<MenuItem value={1} primaryText="CD 6 RON" />
					          	<MenuItem value={2} primaryText="Book 8 RON" />
					          	<MenuItem value={3} primaryText="Book + CD 13 RON" />
					       </SelectField>

    				}
	          		primaryText={<span style={{fontSize: '1.65em', marginLeft: '6em'}}> <b>{newspaper.name}</b></span>}
	          		secondaryText={
			            <p>
			              <span style={{color: darkBlack, fontSize: '1.3em', marginLeft: '10em'}}>{newspaper.category}</span>
			              <br/>
			              <span style={{color: darkBlack, fontSize: '1.3em', marginLeft: '10em'}}><b>Price</b> {newspaper.price} RON</span>
			            </p>
	          		}
	          		secondaryTextLines = {2}
	        	/>
	        	<Divider />
	        </div>
        )
	}

}

