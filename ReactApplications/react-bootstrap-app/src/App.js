import React, {Component} from 'react';
import { BrowserRouter as Router, Route, Switch } from  'react-router-dom'

import {Home} from './components/Home';
import {Contact} from './components/Contact';
import {About} from './components/About';
import {NoMatch} from './components/NoMatch';
import {Layout} from './componentdesigns/layout';


class App extends Component {
  render(){
    return (
      <React.Fragment>
      <Layout>
          <Router>
            <Switch>
              <Route exact="/" component={Home} />
              <Route exact="/about" component={About} />
              <Route exact="/contact" component={Contact} />
              <Route component={NoMatch} />
            </Switch>
          </Router>
        </Layout>
      </React.Fragment>
      );
  }
}

export default App;
