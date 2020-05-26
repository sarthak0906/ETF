import React, { useState, useEffect } from 'react';
import PieChart from './PieChart';
import AppTable from './Table.js';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import SimilarETFList from './SimilarETFs';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button';
import axios from 'axios';



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
        <Container fluid>
          <h4> ETF-Description </h4>
          <h5> {this.props.ETF} </h5>
          <h4> <strong>{this.state.DescriptionData.AnnualDividendRate}</strong>  {this.state.DescriptionData.AnnualDividendYield} </h4>
          <br />
          <Row>
            <Col xs={12} md={4}>
              <h6><strong>ETF Description</strong></h6>
              <div className="DescriptionTable">
                {
                  (this.state.DescriptionData != null) ? <AppTable data={this.state.DescriptionData} /> : ""
                }
              </div>
            </Col>
            <Col xs={12} md={4}>
              <h6><strong>ETF Holdings Data</strong></h6>
                {
                  (this.state.HoldingsData.data != null) ? <this.HoldingsTableData data={this.state.HoldingsData.data} /> : ""
                }
            </Col>
            <Col xs={12} md={4}>
                <SimilarETFList data={this.state.similarETFs} submitFn={this.props.submitFn}/>
            </Col>
          </Row>
       </Container>
      )
    }


  HoldingsTableData = (props) => {
  const [showPie, setPie] = useState(false);
  const handleClose = () => setPie(false);
  const handleShow = () => setPie(true);
  console.log("What are we sending to piechart");
  console.log(props.data);
  return (
    <div className="DescriptionTable">
      <Button variant="primary" onClick={handleShow}>
        Holdings Piechart
      </Button>
      <br />
      <br />
      <Modal show={showPie} onHide={handleClose}>
        <Modal.Body>
          <PieChart data={props.data} element={"TickerWeight"} />
        </Modal.Body>
      </Modal>
      <AppTable data={props.data} />
    </div>
    )
  }

}
  

export default Description;