import React from 'react'
import { Link, browserHistory } from 'react-router'
import store from '../stores/store.js'


export default function App({ children }) {
	return (
		<div>
            <Link to="/disease-evolution">Disease Evolution</Link>
            <Link to="/air-pollution">Air Pollution</Link>
			{children}
		</div>
	)
}
