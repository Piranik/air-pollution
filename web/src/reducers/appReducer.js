import {REQUEST_ROMANIA_MAP_COORDS, RECEIVE_ROMANIA_MAP_COORDS, REQUEST_AIR_POLLUTION_STATISTICS, RECEIVE_AIR_POLLUTION_STATISTICS, REQUEST_COUNTIES, RECEIVE_COUNTIES, REQUEST_PARAMETERS, RECEIVE_PARAMETERS} from '../actions/apiActions.js'
import {CHANGE_COUNTY_ACTION, CHANGE_PARAMETER_ACTION, CHANGE_DISPLAY_YEAR} from '../actions/DisplayActions.js';

import { combineReducers } from 'redux'


const initialState = {
  mapCoords: {
    data: [],
    centerPosition: [46.130, 25.203],
    isFetchinng: false,
  },
  airPollution: {
    data: [],
    stationsInCounties: [],
    isFetchinng: false,
  },
  disease: {
    data: [],
    isFetchinng: false,
  },
  usedParameters: {
    data: [],
    isFetchinng: false,
  },
  counties: {
    data: [],
    isFetchinng: false
  },
  selectedYear: 2010,
  selectedMonth: '01',
  currentMonthStatistics: [],
  selectedParameter: 'All',
  selectedCounty: 'All'
}


export default function appReducer( state = initialState, action ) {

  switch( action.type ) {
    case REQUEST_ROMANIA_MAP_COORDS:
      return {...state, mapCoords: {data: [], centerPosition: [46.130, 25.203], isFetchinng: true}}

    case REQUEST_COUNTIES:
      return {...state, counties: {data: [], isFetchinng: true}}

    case REQUEST_AIR_POLLUTION_STATISTICS:
      return {...state, airPollution: {data: [], isFetchinng: true}}

    case REQUEST_PARAMETERS:
      return {...state, usedParameters: {data: [], isFetchinng: true}}

    case RECEIVE_ROMANIA_MAP_COORDS:
      return {...state, mapCoords: {data: action.coords, centerPosition: action.position, isFetchinng: false}}

    case RECEIVE_PARAMETERS:
      return {...state, usedParameters: {data: action.parameters, isFetchinng: false}}

    case RECEIVE_COUNTIES:
      return {...state, counties: {data: action.counties, isFetchinng: false}}

    case RECEIVE_AIR_POLLUTION_STATISTICS:
      return {...state, airPollution: {data: action.statistics, stationsInCounties: action.county_stations, isFetchinng: false}}

    case CHANGE_PARAMETER_ACTION:
      return {...state, selectedParameter: action.newParameter}

    case CHANGE_COUNTY_ACTION:
      return {...state, selectedCounty: action.newCounty};

    case CHANGE_DISPLAY_YEAR:
      return {...state, selectedYear: action.newYear, selectedMonth: action.newMonth};

    default:
      return state;
  }

}

