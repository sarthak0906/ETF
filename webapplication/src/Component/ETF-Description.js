import React, {useState, useEffect } from 'react';
import PieChart from './PieChart';
import AppTable from './Table.js';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

const Description = (props) => {
  console.log(props);
  var descurl = `/ETfDescription/EtfData/${props.ETF}/${props.startDate}`;
  // var descurl = `/ETfDescription/EtfData/${props.ETF}/20200517`;
  var DescriptionTable = DescriptionTableData(descurl);

  var holdingsurls = `/ETfDescription/Holdings/${props.ETF}/${props.startDate}`;
  // var holdingsurls = `/ETfDescription/Holdings/${props.ETF}/20200517`;
  var HoldingsTable = HoldingsTableData(holdingsurls);

  return (
    <Container>
      <h4> ETF-Description </h4>
      <Row>
        <Col>
          <h6> This is the side for Descriptionof the selected ETF</h6>
          {
          (props.file) 
            ? DescriptionTable : ""
          }
        </Col>
        <Col>
          <h6> This is the side for Descriptionof the selected ETF</h6>
          {
          (props.file) 
            ? HoldingsTable : ""
          }
        </Col>
      </Row>
    </Container>
  )
}


const DescriptionTableData = (url) => {
     console.log(url);
     fetch(url).then(res => res.json()).then(df => {
       console.log(df);
       return (
        <div>
          <AppTable data={df} />
        </div>
      )
      })
  }

  const HoldingsTableData = (url) => {
     console.log(url);
     fetch(url).then(res => res.json()).then(df => {
       console.log(df);
       return (
        <div>
          <AppTable data={df} />
          <PieChart data={df} element={"TickerWeight"} />
        </div>
      )
      })
  }



export default Description;



