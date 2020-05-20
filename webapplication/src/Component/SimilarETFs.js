import React, { Component } from 'react';
import ClickTable from './ClickTable.js';

class SimilarETFList extends Component {
  
  render() {
      return (
        <ClickTable data={this.props.data} submitFn={this.props.submitFn} />
      );
  }
}

export default SimilarETFList