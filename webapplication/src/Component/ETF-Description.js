import React, {useState, useEffect } from 'react';
import PieChart from './PieChart';
import AppTable from './Table.js';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
// import Scrollable from 'hide-scrollbar-react';

class Description extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      DescriptionData : {},
      HoldingsData : {},
      DescriptionTableData : "",
      HoldingsTableData : "",
    }
  }

  componentDidMount() {
    this.setState({
        error: null,
        isLoaded: false,
        DescriptionData : {},
        HoldingsData : {},
        DescriptionTableData : ""
    });
    fetch(`http://localhost:5000/ETfDescription/EtfData/${this.props.ETF}/${this.props.startDate}`)
    .then(res =>{console.log(res.clone().json()); return res.clone().json()})
    .then(
      async (result) => {
          await this.setState({isLoaded : true, DescriptionData: result});
          await this.setState({DescriptionTableData : <DescriptionTableData data={this.state.DescriptionData} />});
      },
      async (error) => {
        await this.setState({isLoaded : false, error : error});
      }
    )
  fetch(`http://localhost:5000/ETfDescription/Holdings/${this.props.ETF}/${this.props.startDate}`)
    .then(res => { return res.clone().json()})
    .then(
      async (result) => {
        await this.setState({isLoaded : true, HoldingsData: result});
        await this.setState({HoldingsTableData : <HoldingsTableData data={this.state.HoldingsData} />});
      },
      async (error) => {
        await this.setState({isLoaded : false, error : error});
      }
    )
  }

  async UNSAFE_componentWillReceiveProps(props) {
    fetch(`http://localhost:5000/ETfDescription/EtfData/${this.props.ETF}/${this.props.startDate}`)
      .then(res =>{console.log(res.clone().json()); return res.clone().json()})
      .then(
        async (result) => {
            await this.setState({isLoaded : true, DescriptionData: result});
            await this.setState({DescriptionTableData : <DescriptionTableData data={this.state.DescriptionData} />});
        },
        async (error) => {
          await this.setState({isLoaded : false, error : error});
        }
      )
    fetch(`http://localhost:5000/ETfDescription/Holdings/${this.props.ETF}/${this.props.startDate}`)
      .then(res => { return res.clone().json()})
      .then(
        async (result) => {
          await this.setState({isLoaded : true, HoldingsData: result});
          await this.setState({HoldingsTableData : <HoldingsTableData data={this.state.HoldingsData} />});
        },
        async (error) => {
          await this.setState({isLoaded : false, error : error});
        }
      )
  }
  
  render () {
    return (
      <Container className="Container">
        <h4> ETF-Description </h4>
        <h5> {this.props.ETF} </h5>
        <h4> <strong>{this.state.DescriptionData.AnnualDividendRate}</strong>  {this.state.DescriptionData.AnnualDividendYield} </h4>
        <Row>
          <Col>
            {
              this.state.DescriptionTableData 
            }
          </Col>
          <Col>
            {
              this.state.HoldingsTableData
            }
          </Col>
        </Row>
      </Container>
    )
  }
}

const DescriptionTableData = (props) => {
  // console.log(props);
  // <Scrollable>
  return (
      <div className="DescriptionTable">
        <AppTable data={props.data} />
      </div>
  )
  // </Scrollable>
}

const HoldingsTableData = (props) => {
  // console.log(props.data);
  // <Scrollable>
    return (
        <div className="DescriptionTable">
          <PieChart data={props.data} element={"TickerWeight"} />
          <AppTable data={props.data} />
        </div>
    )
    // </Scrollable>
}

export default Description;