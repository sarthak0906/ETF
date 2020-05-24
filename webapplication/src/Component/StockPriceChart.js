import React from 'react';
import { render } from 'react-dom';
import Chart from './StockCharts/Chart';

import { TypeChooser } from "react-stockcharts/lib/helper";

class ChartComponent extends React.Component {
	
	state={
		data: this.props.data
	}
	
	componentWillReceiveProps(nextProps) {
	  // You don't have to do this check first, but it can help prevent an unneeded render
	  if (nextProps.data !== this.state.data) {
	    this.setState({ data: nextProps.data.data });
	  }
	}

	render() {
		console.log("State of time series data");
		console.log(this.state.data);
		if (this.state.data == '') {
			return <div>Loading...</div>
		}
		return (
			<TypeChooser>
				{type => <Chart type={type} data={this.state.data} />}
			</TypeChooser>
		)
	}
}

export default ChartComponent;