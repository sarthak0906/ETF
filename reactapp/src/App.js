import React from 'react';
import './App.css';
import Todo from './components/Todo';

class App extends React.Component {
  render(){
    return (
      <div className="App">
        <Todo />
        <h1>ETF Arbitrage Application</h1>
      </div>
    );
  }
}

export default App;
