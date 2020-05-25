import React from 'react';
import axios from 'axios';
import AppTable from './Table.js';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import StockDesriptionHeader from './StockDesriptionHeader';
import ChartComponent from './StockPriceChart';
import ScatterPlot from './scatterplot';
import PieChartGraph from './PieChart';

// Code to display chaer
import { tsvParse, csvParse } from  "d3-dsv";
import { timeParse } from "d3-time-format";


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
			],
			historicalArbitrageData:'',
			scatterPlotData:'',
			PNLOverDates:'',
			LoadingStatement: "Loading.. PNL for " + this.props.ETF,
			parseDate : timeParse("%Y-%m-%d %H:%M:%S"),
			etfPriceData:''
		}
		this.fetchDataForADateAndETF = this.fetchDataForADateAndETF.bind(this);
		this.fetchDataCommonToAllDates = this.fetchDataCommonToAllDates.bind(this);
	}

	componentDidMount() {
		this.fetchDataForADateAndETF();
		this.fetchDataCommonToAllDates();
  	}
  	
  	// Use instead of unsafe to update
  	componentDidUpdate(prevProps,prevState) {
  		// This updates states which corresponds to any day for any etf
  		// If date changes update the states to get data for the date
  		// If ETFName changes get the data for that day for the etf
  		const condition1=this.props.ETF !== prevProps.ETF;
  		const condition2=this.props.startDate !== prevProps.startDate;
  		if (condition1 || condition2) {
  			this.fetchDataForADateAndETF()
		}

  		// This updates data which is common to an etf - eg all historical PNL dates datas
  		// This data is common for a particular etf. eg for XLK, this data will remain same for all dates
  		// Only update when etfname changes
  		if (condition1) {
  			this.state.PNLOverDates='';
  			this.state.LoadingStatement= "Loading.. PNL for " + this.props.ETF;
		    this.fetchDataCommonToAllDates()
		}
	}
	
	render(){

  		return(
  		<Container fluid>
			<Row>
	          <Col className="etfArbitrageTable" xs={12} md={5}>
	            <StockDesriptionHeader startDate = {this.props.startDate} ETF={this.props.ETF} />
		      	{this.state.etfArbitrageTableData}
	          </Col>

	          <Col xs={12} md={7}>
				<Row>
					
					<Col xs={12} md={8}>
						<p>Price Chart</p>
		          		<ChartComponent data={this.state.etfPriceData} />
	          		</Col>

	          		<Col xs={12} md={4}>
	          			<p>ETF Movers(Weighted)</p>
	          			<PieChartGraph data={this.state.etfmoversDictCount} element={"Count"}/>
	          			<p>Holdings with most movement</p>
	          			<PieChartGraph data={this.state.highestChangeDictCount} element={"Count"}/>
		          	</Col>
				</Row>

				<ul>
	          		<li>Confidence in signals</li>
	          		<li>Filter by Magnitude Of arbitrage(Left Side to play with)</li>
	          		<li>Give example of days where arbitrage was not that bad</li>
	          		<li>Give Buy/Sell Signal on the chart, CHange time series data</li>
	          		<li>For holidays and weekends data not available</li>
	          		<li>Make table smaller and scrollable</li>
	          	</ul>
	          	
	          	{this.state.PNLStatementForTheDay}

	          	<h5>ETF Change % Vs NAV change %</h5>
	          	{this.state.scatterPlotData}

	          	<h5>PNL For all Dates for ETF</h5>
	          	{
                    (this.state.PNLOverDates) ? this.state.PNLOverDates : this.state.LoadingStatement
                }
	          </Col>
	        </Row>
         </Container>
  		)
  	}


  	// Fetch Data For an ETF & a Date
	fetchDataForADateAndETF(url){
		axios.get(`http://localhost:5000/PastArbitrageData/${this.props.ETF}/${this.props.startDate}`).then(res =>{
			this.setState({
			 	etfArbitrageTableData : <AppTable data={JSON.parse(res.data.etfhistoricaldata)}/>,
			 	PNLStatementForTheDay : <AppTable data={JSON.parse(res.data.PNLStatementForTheDay)}/>,
			 	etfPriceData : {'data':tsvParse(res.data.etfPrices, this.parseData(this.state.parseDate))},
			 	scatterPlotData: <ScatterPlot data={JSON.parse(res.data.scatterPlotData)}/>,
			 	etfmoversDictCount: JSON.parse(res.data.etfmoversDictCount),
			 	highestChangeDictCount: JSON.parse(res.data.highestChangeDictCount)
			});
			console.log(this.state.etfPriceData);
		});
	}

   	// Fetch Data which is common to an ETF across all dates
   	fetchDataCommonToAllDates(url){
   		console.log("All Dates ETFCALled");
		axios.get(`http://localhost:5000/PastArbitrageData/CommonDataAcrossEtf/${this.props.ETF}`).then(res =>{
			console.log(res.data.PNLOverDates);
			this.setState({
			 	PNLOverDates: <AppTable data={JSON.parse(res.data.PNLOverDates)}/>
			});
   		});
   	}

   	// Parse Data For Stock Price Chart
   	parseData(parse) {
		return function(d) {
			d.date = parse(d.date);
			d.open = +parseFloat(d.open);
			d.high = +parseFloat(d.high);
			d.low = +parseFloat(d.low);
			d.close = +parseFloat(d.close);
			d.volume = +parseInt(d.volume);
			
			return d;
		};
	}

}


export default HistoricalArbitrage;