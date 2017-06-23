import {REQUEST_ROMANIA_MAP_COORDS, RECEIVE_ROMANIA_MAP_COORDS, REQUEST_AIR_POLLUTION_STATISTICS, RECEIVE_AIR_POLLUTION_STATISTICS, REQUEST_COUNTIES, RECEIVE_COUNTIES, REQUEST_PARAMETERS, RECEIVE_PARAMETERS, REQUEST_DISEASE_STATISTICS, RECEIVE_DISEASE_STATISTICS, REQUEST_DISEASES,
  RECEIVE_DISEASES, REQUEST_PREDICTION_INFO, RECEIVE_PREDICTION_INFO, REQUEST_PREDICTION_RESULT, RECEIVE_PREDICTION_RESULT} from '../actions/apiActions.js'

import {CHANGE_COUNTY_ACTION, CHANGE_PARAMETER_ACTION, CHANGE_DISPLAY_YEAR, PLAY_BUTTON_PRESSED, STOP_BUTTON_PRESSED, NEXT_TIMELINE_STEP, STOP_TIMELINE, HOVER_COUNTY, CHANGE_DISEASE_CATEGORY_ACTION, CHANGE_DISEASE_ACTION} from '../actions/DisplayActions.js';

import {CHANGE_TOOL_ACTION, CHANGE_PREDICTION_DISEASE_ACTION, CHANGE_MONTHS_ACTION, CHANGE_AQI_ACTION, CHANGE_WIND_ACTION, CHANGE_RAINFALL_ACTION, CHANGE_PRESSURE_ACTION, CHANGE_TEMP_ACTION, CHANGE_DISEASE_CLASS_ACTION} from '../actions/DisplayActions.js';

import { combineReducers } from 'redux'


const initialState = {
  mapCoords: {
    data: [],
    centerPosition: [46.130, 25.203],
    isFetching: false,
  },
  airPollution: {
    data: [],
    stationsInCounties: [],
    isFetching: false,
  },
  diseases: {
    classification: {},
    codification: {},
    isFetching: false,
  },
  diseaseStatistics: {
    data: [],
    boundaries: {},
    isFetching: false,
  },
  usedParameters: {
    data: [],
    indexCodification: {},
    isFetching: false,
  },
  counties: {
    data: [],
    indexCodification: {},
    isFetching: false
  },
  selectedYear: 2014,
  selectedMonth: 0,
  selectedParameter: {
    name: 'Air Quality Index',
    formula: 'AQI',
    index: 2000
  },
  selectedDisease: null,
  selectedDiseaseCategory: null,
  interfaceDisabled: false, // this will unlock the interface
  selectedCounty: 'romania',
  hoveredCounty: null,
  prediction: {
    tools: [],
    toolsScores: {},
    toolsCodification: {},
    allDiseases: [],

    selectedMonths: 3,
    selectedTool: null,
    selectedDisease: null,
    selectedAqi: null,
    selectedWind: null,
    selectedPressure: null,
    selectedRainfall: null,
    selectedTemperature: null,
    selectedWind: null,
    selectedDiseaseClass: null,

    result: null,
    isResultFetching: false,
    isFetching: false,
  },
  paramsLevels: {
    1: [50, 74, 124, 349, 499], // Dioxid de sulf
    4: [10, 20, 30, 40, 100], // PM 10 aut
    5: [10, 20, 30, 40, 100], // PM 10 grv
    9: [40, 80, 120, 180, 240], // Ozon
    1001: [50, 100, 140, 200, 400], // Dioxid de azot
    19: [10, 20, 35, 40], // Viteza vant
    22: [745, 760, 770, 775], // Presiune

    24: { // Precipitatii
      '0': [32.5, 37.5, 42.5, 47.5],
      '1': [30, 35, 40, 45],
      '2': [28.5, 33.5, 38.5, 43.5],
      '3': [40, 45, 50, 55],
      '4': [55, 60, 65, 70],
      '5': [75, 80, 85, 90],
      '6': [50, 55, 60, 65],
      '7': [45, 50, 55, 60],
      '8': [35, 40, 45, 50],
      '9': [42.5, 47.5, 52.5, 57.5],
      '10': [40, 45, 50, 55],
      '11': [42.5, 47.5, 52.5, 57.5],
    },
    20: {     // Temperature
      '0': [-5, -3, -1, 1.5],
      '1': [-3, -1, 1, 3],
      '2': [0, 3, 6, 10],
      '3': [5, 9, 12, 15],
      '4': [12, 15, 17, 20],
      '5': [15, 17, 20, 23],
      '6': [15, 19, 23, 26],
      '7': [15, 19, 22, 26],
      '8': [11, 14, 17, 20],
      '9': [6, 9, 12, 15],
      '10': [0, 3, 6, 9],
      '11': [-4, -1, 2, 5],
    }
  },
  measurementUnits: {
      1: 'μg/m',
      3: 'μg/m',
      4: 'μg/m',
      5: 'μg/m',
      9: 'μg/m',
      10: 'μg/m',
      19: 'km/h',
      20: 'C',
      22: 'mb (milibari)',
      24: 'mm',
      2000: '',
      1001: 'μg/m'
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

const mapFunctionForParams = (element) => Number.parseInt(element['index'], 10)

export default function appReducer( state = initialState, action ) {
  let newPredictionObject
  switch( action.type ) {
    case REQUEST_ROMANIA_MAP_COORDS:
      return {...state, mapCoords: {data: [], centerPosition: [46.130, 25.203], isFetching: true}}

    case REQUEST_COUNTIES:
      return {...state, counties: {data: [], isFetching: true, indexCodification: {}}}

    case REQUEST_AIR_POLLUTION_STATISTICS:
      return {...state, airPollution: {data: [], isFetching: true}};

    case REQUEST_DISEASE_STATISTICS:
      return {...state, diseaseStatistics: {data: [], boundaries: {}, isFetching: true}};

    case REQUEST_DISEASES:
      newPredictionObject = {...state.prediction, allDiseases: []}
      return {...state, diseases: {classification: {}, codification: {}, isFetching: true}, prediction: newPredictionObject}

    case REQUEST_PARAMETERS:
      return {...state, usedParameters: {data: [], isFetching: true, indexCodification: {}}};

    case REQUEST_PREDICTION_INFO:
      newPredictionObject = {
        ...state.prediction,
        isFetching: false,
        tools: [],
        toolsScores: {},
        toolsCodification: {}
      }
      return {...state, prediction: newPredictionObject}

    case REQUEST_PREDICTION_RESULT:
      newPredictionObject = {
        ...state.prediction,
        result: null,
        isResultFetching: true,
      }
      return {...state, prediction: newPredictionObject}

    case RECEIVE_ROMANIA_MAP_COORDS:
      return {...state, mapCoords: {data: action.coords, centerPosition: action.position, isFetching: false}}

    case RECEIVE_PARAMETERS:
      const params = action.parameters.map(mapFunctionForParams).sort(sortNumbers);
      return {...state, usedParameters: {data: action.parameters, isFetching: false, indexCodification: computeIndex(params)}};

    case RECEIVE_COUNTIES:
      const counties = action.counties.map(mapFunctionForCounties).sort();
      // add Romania
      return {...state, counties: {data: action.counties, isFetching: false, indexCodification: computeIndex(counties)} };

    case RECEIVE_AIR_POLLUTION_STATISTICS:
      return {...state, airPollution: {data: action.statistics, stationsInCounties: action.county_stations, isFetching: false}};

    case RECEIVE_DISEASE_STATISTICS:
      return {...state, diseaseStatistics: {data: action.statistics, boundaries: action.boundaries,
        isFetching: false}};

    case RECEIVE_DISEASES:
      let allDiseases = []
      for (let diseaseCategory in action.classification) {
        for (let disease in action.classification[diseaseCategory]) {
          allDiseases.push(action.classification[diseaseCategory][disease])
        }
      }
      const diseaseCategory = Object.keys(action.classification)[0]
      newPredictionObject = {...state.prediction, allDiseases: allDiseases, selectedDisease: allDiseases[0]}

      return {...state, diseases: {classification: action.classification, codification: action.codification, isFetching: false}, selectedDiseaseCategory: diseaseCategory, selectedDisease: action.classification[diseaseCategory][0], prediction: newPredictionObject}

    case RECEIVE_PREDICTION_INFO:
      const tools = Object.keys(action.predictionTools)
      newPredictionObject = {...state.prediction, tools: tools, toolsCodification: action.predictionTools, toolsScores: action.predictionScores, selectedTool: tools[0], isFetching: false, selectedMonths: 3};
      return {...state, prediction: newPredictionObject};

    case RECEIVE_PREDICTION_RESULT:
      newPredictionObject = {
        ...state.prediction,
        result: action.result,
        isResultFetching: false
      }
      return {...state, prediction: newPredictionObject}

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
      if (state.playButtonPressed == false) {
        return {...state, interfaceDisabled: false};
      }
      return {...state, selectedMonth: action.nextMonth, selectedYear: action.nextYear};

    case STOP_TIMELINE:
      return {...state, interfaceDisabled: false, playButtonPressed: false};

    case HOVER_COUNTY:
      return {...state, hoveredCounty: action.county}

    case CHANGE_DISEASE_CATEGORY_ACTION:
      return {...state, selectedDiseaseCategory: action.newCategory}

    case CHANGE_DISEASE_ACTION:
      return {...state, selectedDisease: action.newDisease}

    case CHANGE_TOOL_ACTION:
      newPredictionObject = {...state.prediction, selectedTool: action.newTool, result: null};
      return {...state, prediction: newPredictionObject};

    case CHANGE_PREDICTION_DISEASE_ACTION:
      newPredictionObject = {...state.prediction, selectedDisease: action.newDisease, selectedDiseaseClass: null, result: null};
      return {...state, prediction: newPredictionObject};

    case CHANGE_MONTHS_ACTION:
      newPredictionObject = {...state.prediction, selectedMonths: action.newMonth, result: null};
      return {...state, prediction: newPredictionObject};

    case CHANGE_AQI_ACTION:
      newPredictionObject = {...state.prediction, selectedAqi: action.newAqi, result: null};
      return {...state, prediction: newPredictionObject};

    case CHANGE_WIND_ACTION:
      newPredictionObject = {...state.prediction, selectedWind: action.newWind, result: null};
      return {...state, prediction: newPredictionObject};

    case CHANGE_RAINFALL_ACTION:
      newPredictionObject = {...state.prediction, selectedRainfall: action.newRainfall, result: null};
      return {...state, prediction: newPredictionObject};

    case CHANGE_PRESSURE_ACTION:
      newPredictionObject = {...state.prediction, selectedPressure: action.newPressure, result: null};
      return {...state, prediction: newPredictionObject};

    case CHANGE_TEMP_ACTION:
      newPredictionObject = {...state.prediction, selectedTemperature: action.newTemp, result: null};
      return {...state, prediction: newPredictionObject};

    case CHANGE_DISEASE_CLASS_ACTION:
      newPredictionObject = {...state.prediction, selectedDiseaseClass: action.newDiseaseClass, result: null}
      return {...state, prediction: newPredictionObject}

    default:
      return state;
  }

}

