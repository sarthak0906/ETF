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
    SameIssuerETFs:'',
    IssuerName:null,
    SimilarTotalAsstUndMgmt:'',
    EtfsWithSameEtfDbCategory:'',
    EtfDbCategory:null
  }

  componentDidMount() {
    this.fetchETFDescriptionData()
    this.fetchSameIssuer()
    this.fetchSameETFdbCategory()
    }
   
  
  componentDidUpdate(prevProps,prevState) {
      const condition1=this.props.ETF !== prevProps.ETF;
      const condition2=this.props.startDate !== prevProps.startDate;
      
      if (condition1 || condition2) {
        this.fetchETFDescriptionData()
      }

      if (this.state.IssuerName !== prevState.IssuerName){
        this.fetchSameIssuer();
      }

      if (this.state.EtfDbCategory !== prevState.EtfDbCategory){
        this.fetchSameETFdbCategory();
      }
  }

  
  fetchETFDescriptionData(){
    axios.get(`http://localhost:5000/ETfDescription/EtfData/${this.props.ETF}/${this.props.startDate}`).then(res =>{
        this.setState({
          DescriptionData : res.data.ETFDataObject,
          HoldingsData : res.data.HoldingsDatObject,
          SimilarTotalAsstUndMgmt: res.data.SimilarTotalAsstUndMgmt,
          IssuerName: res.data.ETFDataObject.Issuer,
          EtfDbCategory: res.data.ETFDataObject.ETFdbCategory
        });
        console.log("HoldingsData");
        console.log(this.state.HoldingsData);
      });
    }

  fetchSameIssuer(){
      if(this.state.IssuerName!== null){
        axios.get(`http://localhost:5000/ETfDescription/getETFWithSameIssuer/${this.state.IssuerName}`).then(res =>{
          this.setState({SameIssuerETFs : res.data});
        });
      }
    }


  fetchSameETFdbCategory(){
      if(this.state.EtfDbCategory!== null){
        axios.get(`http://localhost:5000/ETfDescription/getETFsWithSameETFdbCategory/${this.state.EtfDbCategory}`).then(res =>{
            this.setState({EtfsWithSameEtfDbCategory : res.data});
        });
      }
    }
  

  render(){
      return (
        <Container fluid className='pt-3'>
          <Row>
            <Col xs={12} md={9}>
              <Row>
                <Col xs={12} md={6}>
                  <h6><strong>ETF Description</strong></h6>
                  <div className="DescriptionTable">
                    {
                      (this.state.DescriptionData != null) ? <AppTable data={this.state.DescriptionData} clickableTable={'False'} /> : ""
                    }
                  </div>
                </Col>
                
                <Col xs={12} md={6}>
                  <h6><strong>ETFs from same issuer : {this.state.IssuerName}</strong></h6>
                  <div className="DescriptionTable">
                      <AppTable data={this.state.SameIssuerETFs} clickableTable='True' submitFn={this.props.submitFn}/>
                  </div>
                </Col>

                <Col xs={12} md={6}>
                  <h6><strong>Other ETF similar asset under management</strong></h6>
                  <div className="DescriptionTable">
                    <AppTable data={this.state.SimilarTotalAsstUndMgmt} clickableTable='False' submitFn={this.props.submitFn}/>
                  </div>
                </Col>

                <Col xs={12} md={6}>
                  <h6><strong>ETF within Industry : {this.state.EtfDbCategory}</strong></h6>
                  <div className="DescriptionTable">
                    <AppTable data={this.state.EtfsWithSameEtfDbCategory} clickableTable='False' submitFn={this.props.submitFn}/>
                  </div>
                </Col>

              </Row>
            </Col>
            <Col xs={12} md={3}>
                {
                (this.state.HoldingsData != null) ? <this.HoldingsTableData data={this.state.HoldingsData} clickableTable={'False'} /> : ""
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