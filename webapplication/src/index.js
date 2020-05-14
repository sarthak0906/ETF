import React, {useState } from 'react';
import { render } from 'react-dom';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'
import Former from './Component/Form.js';
import Analysis from './Component/ETF-Analysis';
import Comparison from './Component/ETF-Comparison';
import Description from './Component/ETF-Description';
import Historical from './Component/Historical-Arbitrage';
import Live_Arbitrage from './Component/Live-Arbitrage';
import ML from './Component/Machine-Learning';



// StylesSheets
import './static/css/style.css';

const YesterdayDate = () => {
  var d = new Date(Date.now() - 86400000);

  if (d.getMonth() < 9){
    if (d.getDate() < 10){
      return (d.getFullYear() + '0' + (d.getMonth()+1) + '0' + d.getDate());
    }
    return (d.getFullYear() + '0' + (d.getMonth()+1) + '' + d.getDate());
  }
  else {
    if (d.getDate() < 10){
      return (d.getFullYear() + '' + (d.getMonth()+1) + '0' + d.getDate());
    }
    return (d.getFullYear() + '' + (d.getMonth()+1) + '' + d.getDate());
  }
}

const App = (props) => {
  const [startDate, setDate] = useState(YesterdayDate());
  const [file, setFile] = useState("");
  const [ETF, setETF] = useState("");

  const SubmitFn = async (stock, date) => {
    await setETF(stock);
    await setDate(date);
    console.log(date);
    console.log(ETF);
    let a = stock + '-'  +date;
    await setFile(a);
    console.log(file);
  }

  return (
    <Router>
      <div className="Container">
        <div>
          <div className="Form">
            <Former submitFn={SubmitFn} />
          </div>
        </div>
      </div>
      {/* <Route exact path="/" render={} /> */}
      <Route path="/ETF-Analysis" render={Analysis} />
      <Route path="/ETF-Comparison" render={Comparison} />
      <Route path="/ETF-Description" render={() => <Description file={file} startDate ={startDate} ETF={ETF} submitFn={SubmitFn} />} />
      <Route path="/Historical" render={Historical} />
      <Route path="/Live-Arbitrage" render={Live_Arbitrage} />
      <Route path="/Machine-Learning" render={ML} />
    </ Router>
  )
}

render(<App />, document.getElementById('root'));