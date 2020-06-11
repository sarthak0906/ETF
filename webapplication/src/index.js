import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Route, Redirect , BrowserRouter as Router } from 'react-router-dom'


import Former from './Component/Form.js';
import Comparison from './Component/ETF-Comparison';
import Description from './Component/ETF-Description';
import HistoricalArbitrage from './Component/Historical-Arbitrage';
import Live_Arbitrage from './Component/Live-Arbitrage';
import Live_Arbitrage_Single from './Component/Live-Arbitrage-Single';
import ML from './Component/Machine-Learning';
import SignInFormPage from './Component/User/login';
import SignUpFormPage from './Component/User/signup';
import EmailVerification from './Component/User/emailverification';
import { createBrowserHistory } from "history";

// StylesSheets
import './static/css/style.css';

const history = createBrowserHistory();

class App extends Component {
  
  state={
    ETF:'XLK',
    startDate:'20200511'
  };

  componentDidMount() {
		this.setState({
			ETF:'XLK',
      startDate:'20200511'
		});
  }

  SubmitFn = (etfname, newdate) => {	
    console.log("Change ETF Name & Date");
    
    let ETFcopy = this.state.ETF;
    let startDatecopy = this.state.startDate;

    ETFcopy=etfname
    startDatecopy=newdate

    console.log(etfname);
    console.log(newdate);
      
    this.setState({
      ETF:ETFcopy,
      startDate:startDatecopy
    });
  };

  SubmitNewETF = (etfName) => {
    this.setState({ETF: etfName});
  }

  render(){
  	return (
    <Router history={history} >
      <div className="Container">
        <div>
          <div className="Form">
            <Former SubmitFn={this.SubmitFn} ETF={this.state.ETF} startDate={this.state.startDate}/>
          </div>
        </div>
      </div>
      <ProtectedRoute path="/ETF-Comparison" render={Comparison} />
      <ProtectedRoute path="/ETF-Description" render={() => <Description startDate={this.state.startDate} ETF={this.state.ETF} submitFn={this.SubmitNewETF} />} />
      <ProtectedRoute path="/HistoricalArbitrage" render={() => <HistoricalArbitrage startDate ={this.state.startDate} ETF={this.state.ETF} submitFn={this.SubmitFn} />} />
      <ProtectedRoute path="/Live-Arbitrage-Single" render={() => <Live_Arbitrage_Single ETF={this.state.ETF} />} />
      <ProtectedRoute path="/Live-Arbitrage" render={() => <Live_Arbitrage ETF={this.state.ETF} />} />
      <ProtectedRoute path="/Machine-Learning" render={ML} />
      <Route path="/SignUp" render={() => <SignUpFormPage />} />
      <Route path="/Login" render={SignInFormPage} />
      <Route path="/EmailVerification" render={() => <EmailVerification />} />
    </ Router>
    );
  }

}

const ProtectedRoute = ({ render: Component, ...rest }) => (
  <Route {...rest} render={(props) => (
    localStorage.getItem("username") === null ? 
      <Component {...props} /> : <Redirect to={{ pathname: '/Login', state: { from: props.location }}} />
  )} />
);

ReactDOM.render(<App />,document.getElementById('root'));
