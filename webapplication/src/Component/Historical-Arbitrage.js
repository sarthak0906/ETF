import React from 'react';
import axios from 'axios';
import AppTable from './Table.js';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

class HistoricalArbitrage extends React.Component{
	
	state ={
		etfArbitrageData : {},
  		etfArbitrageTableData : "",
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
			<Row>
	          <Col>
	              <h4>Historical Arbitrage</h4>
	              {this.state.etfArbitrageTableData}
	          </Col>
	          <Col>
	          	<h4>ETF Mover</h4>
	          </Col>
	        </Row>
         </Container>
  		)
  	}
}


export default HistoricalArbitrage;