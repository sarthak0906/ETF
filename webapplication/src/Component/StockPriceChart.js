import React from 'react';
import { render } from 'react-dom';
import Chart from './StockCharts/Chart';
import CandleStickChartWithMACDIndicator from './StockCharts/CandleStickChartWithMACDIndicator';

import { TypeChooser } from "react-stockcharts/lib/helper";

class ChartComponent extends React.Component {
	
	state={
		data: this.props.data
	}
	
	componentWillReceiveProps(nextProps) {
	  // You don't have to do this check first, but it can help prevent an unneeded render
	  	console.log("Check for updates");
		console.log(nextProps.data.data);
		console.log(this.state.data);
	  	if (nextProps.data.data !== this.state.data && nextProps.data.data!==undefined) {
	    	var DataCopy =  this.state.date;
	  		DataCopy = nextProps.data.data;
	  		this.setState({ 
	  			data:DataCopy
	  		});
	  	}
	}

	render() {
		console.log("State of time series data");
		console.log(this.state.data);
		if (this.state.data == '') {
			return <div>Loading...</div>
		}
		return (
		<CandleStickChartWithMACDIndicator data={this.state.data} />
		)
	}
}

export default ChartComponent;