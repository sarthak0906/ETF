import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router } from 'react-router-dom'
import Former from './Component/Form.js';
import Comparison from './Component/ETF-Comparison';
import Description from './Component/ETF-Description';
import HistoricalArbitrage from './Component/Historical-Arbitrage';
import Live_Arbitrage from './Component/Live-Arbitrage';
import ML from './Component/Machine-Learning';

// StylesSheets
import './static/css/style.css';


class App extends Component {
  
  state={
    ETF:'XLK',
    startDate:'20200511'
  };

  
SubmitFn = (stock, date) => {	
    console.log("Change ETF Name & Date");
    const startDate = this.state.startDate;
    const ETF = this.state.ETF;
    this.setState({startDate});
    this.setState({ETF});
    console.log(startDate);
    console.log(ETF);
};


  render(){
  	return (
      <Router>
      <div className="Container">
        <div>
          <div className="Form">
            <Former submitFn={this.state.SubmitFn} ETF={this.state.ETF} />
          </div>
        </div>
      </div>
      <Route path="/ETF-Comparison" render={Comparison} />
      <Route path="/ETF-Description" render={() => <Description startDate={this.state.startDate} ETF={this.state.ETF} submitFn={this.state.SubmitFn} />} />
      <Route path="/HistoricalArbitrage" render={() => <HistoricalArbitrage startDate ={this.state.startDate} ETF={this.state.ETF} submitFn={this.state.SubmitFn} />} />
      <Route path="/Live-Arbitrage" render={Live_Arbitrage} />
      <Route path="/Machine-Learning" render={ML} />
    </ Router>
    );
  }

}

ReactDOM.render(<App />,document.getElementById('root'));
