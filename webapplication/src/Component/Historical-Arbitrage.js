<<<<<<< HEAD
// eslint-disable-next-line
import React, {useState } from 'react';
=======
import React from 'react';
import axios from 'axios';
import AppTable from './Table.js';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import StockDesriptionHeader from './StockDesriptionHeader';
import TimeSeriesChart from './TimeSeriesChart';
>>>>>>> 9a9abb392cd4d22cb417ea9ad7f30f6ffd880e45


class HistoricalArbitrage extends React.Component{
	
	state ={
		etfArbitrageData : {},
  		etfArbitrageTableData : "",
    	 timeseriesdata : [
		  { value: 14, time: 1503617297689 },
		  { value: 15, time: 1503616962277 },
		  { value: 15, time: 1503616882654 },
		  { value: 20, time: 1503613184594 },
		  { value: 15, time: 1503611308914 },
		]
	}


    

	componentDidMount() {
  		axios.get('http://localhost:5000/PastArbitrageData/XLK/20200504').then(res =>{
  			console.log("Component Load to get ETF Data");
  			this.setState({etfArbitrageData: res});
  			this.setState({etfArbitrageTableData: <AppTable data={this.state.etfArbitrageData.data}/>});
  		});
  	}

  	render(){
		console.log(this.state.etfArbitrageTableData);
  		return(
  		<Container fluid>
			<h4> Historical Arbitrage </h4>
			<Row>
	          <Col xs={12} md={7}>
	            <StockDesriptionHeader startDate = {this.props.startDate} ETF={this.props.ETF}>
				</StockDesriptionHeader>
		      {this.state.etfArbitrageTableData}
	          </Col>
	          <Col xs={12} md={5}>
	          	<h4>ETF Mover</h4>
	          	<TimeSeriesChart chartData={this.state.timeseriesdata} />
	          </Col>
	        </Row>
         </Container>
  		)
  	}
}


export default HistoricalArbitrage;