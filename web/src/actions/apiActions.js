import fetch from 'isomorphic-fetch'


export const REQUEST_NEWSPAPERS = 'REQUEST_NEWSPAPERS'
export const RECEIVE_NEWSPAPERS = 'RECEIVE_NEWSPAPERS'
export const REQUEST_CATEGORIES = 'REQUEST_CATEGORIES'
export const RECEIVE_CATEGORIES = 'RECEIVE_CATEGORIES'
export const REQUEST_ROMANIA_MAP_COORDS = 'REQUEST_ROMANIA_MAP_COORDS'
export const RECEIVE_ROMANIA_MAP_COORDS = 'RECEIVE_ROMANIA_MAP_COORDS'

function requestRomaniaMapCoords() {
  return {
    type: REQUEST_ROMANIA_MAP_COORDS
  }
}

function receiveRomaniaMapCoords() {
  return {
    type: REQUEST_ROMANIA_MAP_COORDS
  }
}

function requestNewspapers() {
  return {
    type: REQUEST_NEWSPAPERS
  }
}

function requestCategories() {
	return {
		type: REQUEST_CATEGORIES
	}
}

function receiveNewspapers(json) {
  return {
    type: RECEIVE_NEWSPAPERS,
    newspapers: json.newspapers.map(function(item) {
    	item.selected = false;
    	item.addon_selected = 0;
    	return item;
	}),
    total: json.count
  }
}

function receiveCategories(json) {
  return {
    type: RECEIVE_CATEGORIES,
    categories: json.categories,
    total: json.count
  }
}

export function fetchNewspapers() {
	return function (dispatch) {
		dispatch(requestNewspapers());

		return fetch('http://localhost:8000/newspapers')
			.then(response => response.json())
      		.then(json => {
      			console.log(json)
      			dispatch(receiveNewspapers(json))
      		})
	}
}

export function fetchCategories() {
	return function (dispatch) {
		dispatch(requestCategories());

		return fetch('http://localhost:8000/categories')
			.then(response => response.json())
      		.then(json => {
      			console.log(json)
      			dispatch(receiveCategories(json))
      		})
	}
}
