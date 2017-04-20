import 'babel-polyfill'
import injectTapEventPlugin from 'react-tap-event-plugin';

import React from 'react'
import ReactDOM from 'react-dom'
import { Router, Route, browserHistory } from 'react-router'
import { syncHistoryWithStore, routerReducer } from 'react-router-redux'
import { store } from './stores/store.js'
import { Provider } from 'react-redux'
import { fetchNewspapers, fetchCategories, fetchRomaniaMapCoords } from './actions/apiActions.js'
import jQuery from 'jquery'

import App from './containers/App'
import WelcomeView from './containers/WelcomeView'
import AirPollutionView from './containers/AirPollutionView'
import DiseaseEvolutionView from './containers/DiseaseEvolutionView'


// injectTapEventPlugin();
const history = syncHistoryWithStore(browserHistory, store)

ReactDOM.render(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/" component={WelcomeView}/>
      <Route path="/air" component={WelcomeView}/>
      <Route path="/air/air-pollution" component={AirPollutionView} />
      <Route path="/air/disease-evolution" component={DiseaseEvolutionView}/>
    </Router>
  </Provider>,
  document.getElementById('app')
)

