import React, { Component } from 'react';
import ClickTable from './ClickTable.js';

export default class Example extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: {
        'XLE' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'},
        'XLU' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'},
        'XLK' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'},
        'XLB' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'},
        'XLP' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'},
        'XLY' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'},
        'XLI' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'},
        'XLC' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'},
        'XLV' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'},
        'XLF' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'},
        'XLRE' : { ETFName: 'Technology Select Sector SPDR Fund', ExpenseRatio: '0.3'}
      }
    };
  }
  
  render() {
      return (
        <ClickTable data={this.state.data} submitFn={this.props.submitFn} />
      );
  }
}