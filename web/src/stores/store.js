import thunkMiddleware from 'redux-thunk'
import { createStore, combineReducers, applyMiddleware } from 'redux'
import appReducer from '../reducers/appReducer.js'
import { routerReducer } from 'react-router-redux'

console.log(appReducer)

export const store = createStore(
	combineReducers({
		state: appReducer,
		routing: routerReducer
	}),
	applyMiddleware(
	    thunkMiddleware, // lets us dispatch() functions
  )
)
