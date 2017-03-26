import fetch from 'isomorphic-fetch'


export const REQUEST_ROMANIA_MAP_COORDS = 'REQUEST_ROMANIA_MAP_COORDS'
export const RECEIVE_ROMANIA_MAP_COORDS = 'RECEIVE_ROMANIA_MAP_COORDS'
export const REQUEST_AIR_POLLUTION_STATISTICS = 'REQUEST_AIR_POLLUTION_STATISTICS'
export const RECEIVE_AIR_POLLUTION_STATISTICS = 'RECEIVE_AIR_POLLUTION_STATISTICS'
export const REQUEST_COUNTIES = 'REQUEST_COUNTIES'
export const RECEIVE_COUNTIES = 'RECEIVE_COUNTIES'
export const REQUEST_PARAMETERS= 'REQUEST_PARAMETERS'
export const RECEIVE_PARAMETERS = 'RECEIVE_PARAMETERS'


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
  return {
    type: RECEIVE_AIR_POLLUTION_STATISTICS,
    statistics: response.statistics,
    county_stations: response.number_of_stations
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

export function fetchParameters() {
  return function(dispatch) {
    dispatch(requestParameters());
    return fetch('http://localhost:8000/api/used_parameters')
      .then(response => response.json)
        .then(json => {
          console.log('Got parameters');
          dispatch(receiveParameters(json));
        })
  }
}

export function fetchCounties() {
  return function(dispatch) {
    dispatch(requestCounties());
    return fetch('http://localhost:8000/api/counties')
      .then(response => response.json)
        .then(json => {
          console.log('Got counties');
          dispatch(receiveCounties(json));
        })
  }
}

export function fetchMapCoords() {
  return function(dispatch) {
    dispatch(requestRomaniaMapCoords());
    return fetch('http://localhost:8000/api/ro_map_data')
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
    return fetch('http://localhost:8000/api/statistics/air_pollution_county')
      .then(response => response.json())
        .then(json => {
          console.log('Got Air Statistics')
          dispatch(receiveAirPollutionStatistics(json))
        })
  }
}

