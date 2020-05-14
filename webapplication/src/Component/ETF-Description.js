import React, {useState, useEffect } from 'react';
import PieChart from './PieChart';
import AppTable from './Table.js';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

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
  }

  async UNSAFE_componentWillReceiveProps(props) {
    console.log(this.props)
    console.log(`http://localhost:5000/ETfDescription/Holdings/${this.props.ETF}/${this.props.startDate}`);
    fetch(`http://localhost:5000/ETfDescription/EtfData/${this.props.ETF}/${this.props.startDate}`)
    // fetch(`http://localhost:5000/ETfDescription/EtfData/PSCM/20200417`)
      .then(res =>{console.log(res.clone().json()); return res.clone().json()})
      .then(
        async (result) => {
            await this.setState({isLoaded : true, DescriptionData: result});
            console.log(this.state.DescriptionData);
            await this.setState({DescriptionTableData : <DescriptionTableData data={this.state.DescriptionData} />});
            // var DescriptionTableData =  ;
            // console.log(DescriptionTableData);
        },
        async (error) => {
          await this.setState({isLoaded : false, error : error});
        }
      )
    fetch(`http://localhost:5000/ETfDescription/Holdings/${this.props.ETF}/${this.props.startDate}`)
    // fetch(`http://localhost:5000/ETfDescription/Holdings/PSCM/20200417`)
      .then(res => { console.log(res.ok); return res.clone().json()})
      .then(
        async (result) => {
          await this.setState({isLoaded : true, HoldingsData: result});
          await this.setState({HoldingsTableData : <HoldingsTableData data={this.state.HoldingsData} />});
          console.log(this.state.HoldingsData);
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
  console.log(props);
  return (
      <div>
        <AppTable data={props.data} />
      </div>
  )
}

const HoldingsTableData = (props) => {
  console.log(props.data);
    return (
      <div>
        <AppTable data={props.data} />
        <PieChart data={props.data} element={"TickerWeight"} />
      </div>
    )
}

export default Description;

// import React, { Component } from 'react';

// class Description extends Component {
//   constructor(props) {
//     console.log(props);

//     this.state = {
//       error : null,
//       ETFData : null,
//       Holdings : null
//     }
//   }

//   componentWillReceiveProps()
// }