import {REQUEST_ROMANIA_MAP_COORDS, RECEIVE_ROMANIA_MAP_COORDS, REQUEST_AIR_POLLUTION_STATISTICS, RECEIVE_AIR_POLLUTION_STATISTICS, REQUEST_COUNTIES, RECEIVE_COUNTIES, REQUEST_PARAMETERS, RECEIVE_PARAMETERS} from '../actions/apiActions.js'
import {CHANGE_COUNTY_ACTION, CHANGE_PARAMETER_ACTION, CHANGE_DISPLAY_YEAR, PLAY_BUTTON_PRESSED, STOP_BUTTON_PRESSED, NEXT_TIMELINE_STEP} from '../actions/DisplayActions.js';

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
  selectedYear: 2012,
  selectedMonth: 0,
  currentMonthStatistics: [],
  selectedParameter: {
    name: 'Air Quality Index',
    formula: 'AQI',
    index: 1000
  },
  playMode: false, // this enables play mode
  interfaceDisabled: false, // this will unlock the interface
  selectedCounty: 'romania',
  paramsLevels: {
    3: [53, 100, 360, 649, 1249, 2049], // Oxizi de Azot
    10: [50, 100, 200, 300, 350, 400], // Monoxid de Azot
    1: [35, 75, 185, 304, 604, 1004], // Dioxid de sulf
    9: [125, null, 164, 204, 404, 604], // Ozon
    4: [54, 154, 254, 354, 424, 604], // PM 10 aut
    5: [54, 154, 254, 354, 424, 604], // PM 10 grv
    19: [2, 10, 25, 40, 50, 60], // Viteza vant
    22: [900, 1020, 1050, 1100, 1150, 1200], // Presiune

    24: { // Precipitatii
      '0': [40, 45, 50, 55, 60, 65],
      '1': [40, 45, 50, 55, 60, 65],
      '2': [40, 45, 50, 55, 60, 65],
      '3': [50, 55, 60, 65, 70, 75],
      '4': [65, 70, 75, 80, 85, 90],
      '5': [85, 90, 95, 100, 105, 110],
      '6': [60, 65, 70, 75, 80, 85],
      '7': [55, 60, 65, 70, 75, 80],
      '8': [45, 50, 55, 60, 65, 70],
      '9': [50, 55, 60, 65, 70, 75],
      '10': [50, 55, 60, 65, 70, 75],
      '11': [50, 55, 60, 65, 70, 75],
    },
    20: {     // Temperature
      '0': [-5, -3, -1, 1.5, 3],
      '1': [-3, -1, 1, 3, 5],
      '2': [0, 3, 6, 10, 12],
      '3': [5, 9, 12, 15, 18],
      '4': [12, 15, 17, 20, 23],
      '5': [15, 17, 20, 23, 26],
      '6': [15, 19, 23, 26, 30],
      '7': [15, 19, 22, 26, 30],
      '8': [11, 14, 17, 20, 25],
      '9': [6, 9, 12, 15, 18],
      '10': [0, 3, 6, 9, 12],
      '11': [-4, -1, 2, 5, 8],
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
      return {...state, airPollution: {data: [], isFetchinng: true}};

    case REQUEST_PARAMETERS:
      return {...state, usedParameters: {data: [], isFetchinng: true, indexCodification: {}}};

    case RECEIVE_ROMANIA_MAP_COORDS:
      return {...state, mapCoords: {data: action.coords, centerPosition: action.position, isFetchinng: false}}

    case RECEIVE_PARAMETERS:
      const params = action.parameters.map(mapFunctionForParams).sort(sortNumbers);
      return {...state, usedParameters: {data: action.parameters, isFetchinng: false, indexCodification: computeIndex(params)}};

    case RECEIVE_COUNTIES:
      const counties = action.counties.map(mapFunctionForCounties).sort();
      // add Romania
      return {...state, counties: {data: action.counties, isFetchinng: false, indexCodification: computeIndex(counties)} };

    case RECEIVE_AIR_POLLUTION_STATISTICS:
      return {...state, airPollution: {data: action.statistics, stationsInCounties: action.county_stations, isFetchinng: false}};

    case CHANGE_PARAMETER_ACTION:
      return {...state, selectedParameter: action.newParameter};

    case CHANGE_COUNTY_ACTION:
      return {...state, selectedCounty: action.newCounty};

    case CHANGE_DISPLAY_YEAR:
      return {...state, selectedYear: action.newYear, selectedMonth: action.newMonth};

    case PLAY_BUTTON_PRESSED:
      return {...state, playButtonPressed: true, interfaceDisabled: true};

    case STOP_BUTTON_PRESSED:
      return {...state, playButtonPressed: false};

    case NEXT_TIMELINE_STEP:
      console.log(action)
      if (state.playButtonPressed == false) {
        return {...state, interfaceDisabled: false};
      }
      return {...state, selectedMonth: action.nextMonth, selectedYear: action.nextYear};

    default:
      return state;
  }

}

