import React, { useState, useEffect } from 'react';
import PieChart from './PieChart';
import AppTable from './Table.js';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button';
import axios from 'axios';
import Card from 'react-bootstrap/Card'

class Description extends React.Component{
  
  constructor(props){
    super(props);
  }

  state ={
    DescriptionData :'',
    HoldingsData :'',
    similarETFs:''
  }

  componentDidMount() {
    this.fetchETFDescriptionData()
    this.fetchHoldingsData()
    }
   
  
  componentDidUpdate(prevProps,prevState) {
      const condition1=this.props.ETF !== prevProps.ETF;
      const condition2=this.props.startDate !== prevProps.startDate;
      if (condition1 || condition2) {
        this.fetchETFDescriptionData()
        this.fetchHoldingsData()
    }
  }

  
  fetchETFDescriptionData(){
    axios.get(`http://localhost:5000/ETfDescription/EtfData/${this.props.ETF}/${this.props.startDate}`).then(res =>{
        console.log(res.data);
        this.setState({
          DescriptionData : res.data.ETFDataObject,
          similarETFs: res.data.etfswithsameIssuer
        });
      });
    }

  fetchHoldingsData(){
    axios.get(`http://localhost:5000/ETfDescription/Holdings/${this.props.ETF}/${this.props.startDate}`).then(res =>{
        this.setState({HoldingsData : res});
      });
  }

  render(){
      return (
        <Container fluid className='pt-3'>
          <Row>
            <Col xs={12} md={2}>
              <h6><strong>ETF Description</strong></h6>
              <div className="DescriptionTable">
                {
                  (this.state.DescriptionData != null) ? <AppTable data={this.state.DescriptionData} clickableTable={'False'} /> : ""
                }
              </div>
            </Col>
            
            <Col xs={12} md={4}>

              <div className="DescriptionTable">
                  <AppTable data={this.state.similarETFs} clickableTable='True' submitFn={this.props.submitFn}/>
              </div>
            </Col>

            <Col xs={12} md={3}>
                {
                  (this.state.HoldingsData.data != null) ? <this.HoldingsTableData data={this.state.HoldingsData.data} clickableTable={'False'} /> : ""
                }
            </Col>

          </Row>
       </Container>
      )
    }


  HoldingsTableData = (props) => {
  const [showPie, setPie] = useState(false);
  const handleClose = () => setPie(false);
  const handleShow = () => setPie(true);
  return (
      <Card>
        <Card.Header className="text-white BlackHeaderForModal">ETF Holdings</Card.Header>
        <Card.Body>
            <PieChart data={props.data} element={"TickerWeight"} />
            <div className="DescriptionTable2">
              <AppTable data={props.data} />
            </div>
        </Card.Body>
      </Card>
    )
  }

}
  

export default Description;