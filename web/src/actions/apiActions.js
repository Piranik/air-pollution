import fetch from 'isomorphic-fetch'


export const REQUEST_ROMANIA_MAP_COORDS = 'REQUEST_ROMANIA_MAP_COORDS'
export const RECEIVE_ROMANIA_MAP_COORDS = 'RECEIVE_ROMANIA_MAP_COORDS'
export const REQUEST_AIR_POLLUTION_STATISTICS = 'REQUEST_AIR_POLLUTION_STATISTICS'
export const RECEIVE_AIR_POLLUTION_STATISTICS = 'RECEIVE_AIR_POLLUTION_STATISTICS'
export const REQUEST_DISEASE_STATISTICS = 'REQUEST_DISEASE_STATISTICS'
export const RECEIVE_DISEASE_STATISTICS = 'RECEIVE_DISEASE_STATISTICS'
export const REQUEST_COUNTIES = 'REQUEST_COUNTIES'
export const RECEIVE_COUNTIES = 'RECEIVE_COUNTIES'
export const REQUEST_PARAMETERS= 'REQUEST_PARAMETERS'
export const RECEIVE_PARAMETERS = 'RECEIVE_PARAMETERS'
export const REQUEST_DISAESES = 'REQUEST_DISEASES_CODIFCIATION'
export const RECEIVE_DISEASES = 'RECEIVE_DISEASES_CODIFICATION'
export const REQUEST_PREDICTION_INFO = 'REQUEST_PREDICTION_INFO'
export const RECEIVE_PREDICTION_INFO = 'RECEIVE_PREDICTION_INFO'
export const REQUEST_PREDICTION_RESULT = 'REQUEST_PREDICTION_RESULT'
export const RECEIVE_PREDICTION_RESULT = 'RECEIVE_PREDICTION_RESULT'

const API_BASE_URL = 'http://opendata.cs.pub.ro/air/api/'
const API_PREDICTION_URL = 'http://opendata.cs.pub.ro/air/api/prediction/'

// For DEv
// const API_BASE_URL = 'http://localhost:8000/api/'
// const API_PREDICTION_URL = 'http://localhost:8001/api/prediction/'

function requestParameters() {
  return {
    type: REQUEST_PARAMETERS
  }
}

function receiveParameters(response) {
  return {
    type: RECEIVE_PARAMETERS,
    parameters: response.parameters
  }
}


function requestCounties() {
  return {
    type: REQUEST_COUNTIES
  }
}


function receiveCounties(response) {
  return {
    type: RECEIVE_COUNTIES,
    counties: response.counties
  }
}


function requestAirPollutionStatistics() {
  return {
    type: REQUEST_AIR_POLLUTION_STATISTICS
  }
}

function receiveAirPollutionStatistics(response) {
  console.log(response)
  return {
    type: RECEIVE_AIR_POLLUTION_STATISTICS,
    statistics: response.statistics,
    county_stations: response.number_of_stations
  }
}


function requestDiseaseStatistics() {
  return {
    type: REQUEST_DISEASE_STATISTICS
  };
}


function receiveDiseaseStatistics(response) {
  console.log(response);
  return {
    type: RECEIVE_DISEASE_STATISTICS,
    statistics: response.statistics,
    boundaries: response.boundaries
  };
}


function requestDiseases() {
  return {
    type: REQUEST_DISAESES
  };
}


function receiveDiseases(response) {
  console.log(response);
  return {
    type: RECEIVE_DISEASES,
    codification: response.codification,
    classification: response.diseases_classification
  }
}


function requestRomaniaMapCoords() {
  return {
    type: REQUEST_ROMANIA_MAP_COORDS
  }
}

function receiveRomaniaMapCoords(response) {
  return {
    type: RECEIVE_ROMANIA_MAP_COORDS,
    coords: JSON.parse(response.coords),
    position: response.center
  }
}

function requestPredictionInfo() {
  return {
    type: REQUEST_PREDICTION_INFO
  }
}

function receivePredictionInfo(response) {
  return {
    type: RECEIVE_PREDICTION_INFO,
    predictionTools: response.prediction_tools,
    predictionScores: response.scores
  }
}


function requestPredictionResult() {
  return {
    type: REQUEST_PREDICTION_RESULT
  }
}

function receivePredictionResult(response) {
  return {
    type: RECEIVE_PREDICTION_RESULT,
    result: response.prediction_result
  }
}

export function fetchParameters() {
  return function(dispatch) {
    dispatch(requestParameters());
    return fetch(API_BASE_URL + 'viewed_parameters')
      .then(response => response.json())
        .then(json => {
          console.log('Got parameters');
          dispatch(receiveParameters(json));
        })
  }
}

export function fetchCounties() {
  return function(dispatch) {
    dispatch(requestCounties());
    return fetch(API_BASE_URL + 'counties')
      .then(response => response.json())
        .then(json => {
          console.log('Got counties');
          dispatch(receiveCounties(json));
        })
  }
}

export function fetchMapCoords() {
  return function(dispatch) {
    dispatch(requestRomaniaMapCoords());
    return fetch(API_BASE_URL + 'ro_map_data')
      .then(response => response.json())
        .then(json => {
          console.log('Got coords', json.coords.length);
          dispatch(receiveRomaniaMapCoords(json))
        })
  }
}

export function fetchAirPollutionStatistics() {
  return function(dispatch) {
    dispatch(requestAirPollutionStatistics());
    return fetch(API_BASE_URL + 'statistics/air_pollution_county')
      .then(response => response.json())
        .then(json => {
          console.log('Got Air Statistics')
          dispatch(receiveAirPollutionStatistics(json))
        });
  }
}

export function fetchDiseaseStatistics() {
  return function(dispatch) {
    dispatch(requestDiseaseStatistics());
    return fetch(API_BASE_URL + 'disease_statistics')
      .then(response => response.json())
        .then(json => {
          console.log('Got Disease Statistics');
          dispatch(receiveDiseaseStatistics(json));
        });
  }
}


export function fetchDiseases() {
  return function(dispatch) {
    dispatch(requestDiseases());
    return fetch(API_BASE_URL + 'diseases')
      .then(response => response.json())
        .then(json => {
          console.log('Got Diseases');
          dispatch(receiveDiseases(json))
        });
  }
}

export function fetchPredictionInfo() {
  return function(dispatch) {
    dispatch(requestPredictionInfo());
    return fetch(API_PREDICTION_URL + 'info')
      .then(response => response.json())
        .then(json => {
          console.log('Got Prediction Info');
          dispatch(receivePredictionInfo(json))
        });
  }
}


export function fetchPredictionResult(toolIndex, disease, months, aqiClass, windClass, pressureClass, rainfallClass, tempClass, diseaseClass) {
  return function(dispatch) {
    dispatch(requestPredictionResult());
    const body = JSON.stringify({
      tool_index: toolIndex,
      disease: disease,
      months_predicted: months,
      aqi_class: aqiClass,
      wind_speed_class: windClass,
      pressure_class: pressureClass,
      rainfall_class: rainfallClass,
      temp_class: tempClass,
      disease_class: diseaseClass
    });

    const headers = new Headers({
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    });

    return fetch(API_PREDICTION_URL + 'result', {headers: headers, method: 'POST', body: body})
      .then(response => response.json())
        .then(json => {
          console.log('Got Prediction Result');
          dispatch(receivePredictionResult(json))
        });
  }
}


