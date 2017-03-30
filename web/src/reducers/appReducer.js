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
    indexCodification: {},
    isFetchinng: false,
  },
  counties: {
    data: [],
    indexCodification: {},
    isFetchinng: false
  },
  selectedYear: 2010,
  selectedMonth: '01',
  currentMonthStatistics: [],
  selectedParameter: {
    name: 'Air Quality Index',
    formula: 'AQI',
    index: 1000
  },
  selectedCounty: 'All Country',
  paramsLevels: {
    3: [53, 100, 360, 649, 1249], // Oxizi de Azot
    10: [50, 100, 200, 300, 400], // Monoxid de Azot
    1: [35, 75, 185, 304,  604], // Dioxid de sulf
    9: [null, null, 164, 204, 404], // Ozon
    4: [50, 100, 150, 200, 300], // PM 10 aut
    5: [50, 100, 150, 200, 300], // PM 10 grv
    19: [2, 10, 25, 40, 50], // Viteza vant
    22: [850, 900, 990, 1050, 1100], // Presiune

    24: { // Precipitatii
      '01': [37, 39,1, 41, 43],
      '02': [35, 37.5, 40, 43],
      '03': [34, 36.5, 39, 42],
      '04': [44, 48.2, 52, 55],
      '05': [59, 63.4, 67, 70],
      '06': [77, 81.0, 85, 88],
      '07': [54, 58.3, 62, 65],
      '08': [46, 51.5, 56, 60],
      '09': [39, 43.9, 48, 52],
      '10': [45, 49.7, 54, 58],
      '11': [44, 48.7, 53, 57], // bad, a little bad, good, a little high, high
      '12': [45, 49.4, 54, 58]
    },
    20: {     // Temperature
      '01': [-3, -1,5, 1.5, 3],
      '02': [-1, 0.6, 2, 3],
      '03': [3, 5.7, 7, 8,5],
      '04': [9, 11.1, 13, 15],
      '05': [14, 16.3, 18, 20],
      '06': [17, 19.6, 22, 24],
      '07': [19, 21.5, 28, 35],
      '08': [19, 20.9, 28, 35],
      '09': [14.5, 16.8, 20, 25],
      '10': [9.5, 11.2, 13, 16],
      '11': [4.4, 5.7, 7, 9],
      '12': [0, 1.2, 3, 5]
    }
  }
}

const compareByName = (a, b) => {
  if (a.name > b.name) {
    return 1;
  }
  return -1;
}

const computeIndex = (elements) => {
  let pos = 0;
  let indexCodification = {}
  for (let index in elements) {
    indexCodification[elements[index]] = pos
    pos ++;
  }
  return indexCodification;
}

const sortNumbers = (a, b) => a - b;

const mapFunctionForCounties = (element) => element['name']

const mapFunctionForParams = (element) => Number.parseInt(element['index'],10)

export default function appReducer( state = initialState, action ) {

  switch( action.type ) {
    case REQUEST_ROMANIA_MAP_COORDS:
      return {...state, mapCoords: {data: [], centerPosition: [46.130, 25.203], isFetchinng: true}}

    case REQUEST_COUNTIES:
      return {...state, counties: {data: [], isFetchinng: true, indexCodification: {}}}

    case REQUEST_AIR_POLLUTION_STATISTICS:
      return {...state, airPollution: {data: [], isFetchinng: true}}

    case REQUEST_PARAMETERS:
      return {...state, usedParameters: {data: [], isFetchinng: true, indexCodification: {}}}

    case RECEIVE_ROMANIA_MAP_COORDS:
      return {...state, mapCoords: {data: action.coords, centerPosition: action.position, isFetchinng: false}}

    case RECEIVE_PARAMETERS:
      const params = action.parameters.map(mapFunctionForParams).sort(sortNumbers);
      return {...state, usedParameters: {data: action.parameters, isFetchinng: false, indexCodification: computeIndex(params)}}

    case RECEIVE_COUNTIES:
      const counties = action.counties.map(mapFunctionForCounties).sort();
      // add Romania
      return {...state, counties: {data: action.counties, isFetchinng: false, indexCodification: computeIndex(counties)} }

    case RECEIVE_AIR_POLLUTION_STATISTICS:
      return {...state, airPollution: {data: action.statistics, stationsInCounties: action.county_stations, isFetchinng: false}}

    case CHANGE_PARAMETER_ACTION:
      return {...state, selectedParameter: action.newParameter}

    case CHANGE_COUNTY_ACTION:
      return {...state, selectedCounty: action.newCounty};

    case CHANGE_DISPLAY_YEAR:
      console.log(action)
      return {...state, selectedYear: action.newYear, selectedMonth: action.newMonth};

    default:
      return state;
  }

}

