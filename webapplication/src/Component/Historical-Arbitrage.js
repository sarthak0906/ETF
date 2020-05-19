import React from 'react';
import axios from 'axios';
import AppTable from './Table.js';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import StockDesriptionHeader from './StockDesriptionHeader';
import TimeSeriesChart from './TimeSeriesChart';


class HistoricalArbitrage extends React.Component{
	constructor(props){
		super(props);
		this.state ={
			etfArbitrageTableData : '',
			timeseriesdata : [
			{ Close: 1106, Time: 1503617297689 },
			{ Close: 1105, Time: 1503616962277 },
			{ Close: 1120, Time: 1503616882654 },
			{ Close: 1100, Time: 1503613184594 },
			{ Close: 1110, Time: 1503611308914 },
			]
		}
		this.fetchData = this.fetchData.bind(this);
	}

	componentDidMount() {
		this.fetchData()
  	}
  	
  	// Use instead of unsafe to update
  	componentDidUpdate(prevProps,prevState) {
  		const condition1=this.props.ETF !== prevProps.ETF;
  		const condition2=this.props.startDate !== prevProps.startDate;
  		
  		if (condition1 || condition2) {
		    this.fetchData()
		}
	}
	

  	render(){

  		return(
  		<Container fluid>
			<h4> Historical Arbitrage </h4>
			<Row>
	          <Col xs={12} md={7}>
	            <StockDesriptionHeader startDate = {this.props.startDate} ETF={this.props.ETF} />
		      {this.state.etfArbitrageTableData}
	          </Col>
	          <Col xs={12} md={5}>
	          	<h4>ETF Mover</h4>
	          	<TimeSeriesChart chartData={this.state.timeseriesdata} />
	          	<ul>
	          		<li>Top Movers</li>
	          		<li>Profit and loss</li>
	          		<li>Confidence in signals</li>
	          		<li>Filter by Magnitude Of arbitrage(Left Side to play with)</li>
	          		<li>GIve example of days where arbitrage was not that bad</li>
	          		<li>Give Buy/Sell Signal on the chart, CHange time series data</li>
	          		<li>Update with change in ticker</li>
	          		<li>For holidays and weekends data not available</li>
	          		<li>Make table smaller and scrollable</li>
	          		<li>Scatter plot of arbitrgae and return</li>
	          	</ul>
	          </Col>
	        </Row>
         </Container>
  		)
  	}

	fetchData(url){
		axios.get(`http://localhost:5000/PastArbitrageData/${this.props.ETF}/${this.props.startDate}`).then(res =>{
  			 this.setState({etfArbitrageTableData : <AppTable data={JSON.parse(res.data.etfhistoricaldata)}/>});

   		});
   	}

}


export default HistoricalArbitrage;