import React, { useState, useEffect } from 'react';
import PieChart from './PieChart';
import AppTable from './Table.js';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import SPDR from './Sector-SPDR';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button';
import axios from 'axios';

const Description = (props) => {
  const [DescriptionData, setDescriptionData] = useState({});
  const [HoldingsData, setHoldingsData] = useState({});

  function fetchData(url, setNewState){
		axios.get(url).then(res =>{
      setNewState(res);
    });
  }

  useEffect(() => {
    fetchData(`http://localhost:5000/ETfDescription/Holdings/${props.ETF}/${props.startDate}`, setHoldingsData);
    fetchData(`http://localhost:5000/ETfDescription/EtfData/${props.ETF}/${props.startDate}`, setDescriptionData);
  }, [props]);
  
    return (
      <Container fluid>
        <h4> ETF-Description </h4>
        <h5> {props.ETF} </h5>
        <h4> <strong>{DescriptionData.AnnualDividendRate}</strong>  {DescriptionData.AnnualDividendYield} </h4>
        <br />
        <Row>
          <Col xs={12} md={4}>
            <h6><strong>ETF Description</strong></h6>
            <div className="DescriptionTable">
              {
                (DescriptionData.data != null) ? <AppTable data={DescriptionData.data} /> : ""
              }
            </div>
          </Col>
          <Col xs={12} md={4}>
          <h6><strong>ETF Holdings Data</strong></h6>
            {
              (HoldingsData.data != null) ? <HoldingsTableData data={HoldingsData.data} /> : ""
            }
          </Col>
          <Col xs={12} md={4}>
            <SPDR submitFn={props.submitFn}/>
          </Col>
        </Row>
     </Container>
    )
}
const HoldingsTableData = (props) => {
  const [showPie, setPie] = useState(false);

  const handleClose = () => setPie(false);
  const handleShow = () => setPie(true);

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

export default Description;