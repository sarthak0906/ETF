import React, {useState, useEffect } from 'react';
import AppTable from './Table.js';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'


const Description = (props) => {
    // const [file, setFile] = useState("");

    //var descurl = `/ETfDescription/EtfData/${props.ETF}/${props.startDate}`;
    var descurl = `/ETfDescription/EtfData/${props.ETF}/20200517`;
    var DescriptionTable = updateTableData(descurl);

    
    //var holdingsurls = `/ETfDescription/Holdings/${props.ETF}/${props.startDate}`;
    var holdingsurls = `/ETfDescription/Holdings/${props.ETF}/20200517`;
    var HoldingsTable = updateTableData(holdingsurls);

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


const updateTableData = (url) => {
    console.log(url);
    fetch(url).then(res => res.json()).then(df => {
      console.log(df);
      return <AppTable data={df} />
    });
    return ;
}

export default Description;