import { REQUEST_NEWSPAPERS, RECEIVE_NEWSPAPERS, REQEUST_CATEGORIES, RECEIVE_CATEGORIES } from '../actions/apiActions.js' 
import { TOGGLE_IN_CART, ADD_ADDON, FINALIZE_ORDER } from '../actions/shopActions.js' 
import { combineReducers } from 'redux'

const initialState = {
  newspapers: {
    data: [],
    count: 0,
    isFetchingNewspapers: false,
  },
  categories: {
    data: [],
    count: 0,
    isFetchingCategories: false,
  },
  total: 0
}

const addon_values = {
  0: 0,
  1: 6,
  2: 8,
  3: 13
}

export default function appReducer( state = initialState, action ) {
  let newState = {...state}
  switch( action.type ) {
    case REQUEST_NEWSPAPERS:
      return {...state, newspapers: {data: [], count: 0, isFetchingNewspapers: true}}

    case REQEUST_CATEGORIES:
      return {...state, categories: {data: [], count: 0, isFetchingCategories: true}} 

    case RECEIVE_NEWSPAPERS:
      return {...state, newspapers: {data: action.newspapers, count: action.count, isFetchingNewspapers: false}}

    case REQEUST_CATEGORIES:
      return {...state, categories: {data: action.categories, count: action.count, isFetchingCategories: false}}

    case TOGGLE_IN_CART:
      if (newState.newspapers.data[action.index].selected) {
        newState.newspapers.data[action.index].selected = false
        let newspaper = newState.newspapers.data[action.index]
        newState.total -= newspaper.price + addon_values[newspaper.addon_selected]
        newspaper.addon_selected = 0
        return newState
      }
      else {
        newState.newspapers.data[action.index].selected = true
        let newspaper = newState.newspapers.data[action.index]
        newState.total += newspaper.price
        return newState
      }

    case ADD_ADDON:
      console.log(action)
      let newspaper = newState.newspapers.data[action.index]
      newState.total -= addon_values[newspaper.addon_selected]
      newspaper.addon_selected = action.addon_index
      newState.total += addon_values[newspaper.addon_selected]
      return newState

    case FINALIZE_ORDER:
      newState.newspapers.data = newState.newspapers.data.map(function(item) {
        item.addon_selected = 0;
        item.selected = false;
        return item;
      })
      newState.total = 0
      return newState

    default:
      return state;
  }
}


