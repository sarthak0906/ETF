import React, {useState } from 'react';
import AppTable from './Table.js';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

// Importng Datasets
import * as XLK16 from '../Data/XLK-16.json';
import * as XLK17 from '../Data/XLK-17.json';
import * as FTEC17 from '../Data/FTEC-17.json';
import * as FTEC16 from '../Data/FTEC-16.json';

const Description = (props) => {
    // const [file, setFile] = useState("");

    var table = RenderTable(props.file);

    return (
      <Container>
          <h4> ETF-Description </h4>
          <Row>
            <Col>
              <h6> This is the side for Descriptionof the selected ETF</h6>
            </Col>
            <Col>
              <h6> This is the side for Descriptionof the selected ETF</h6>
              {
              (props.file) 
                ? table : ""
              }
            </Col>
          </Row>
      </Container>
);
}

const RenderTable = (file) =>{
    console.log("File is ");
    console.log(file);
    if (file === ""){
      return ;
    }
    if (file === "XLK-16"){
      return <AppTable data={XLK16.data} />
    }
    if (file === "XLK-17"){
      return <AppTable data={XLK17.data} />
    }
    if (file === "FTEC-16"){
      return <AppTable data={FTEC16.data} />
    }
    if (file === "FTEC-17"){
      return <AppTable data={FTEC17.data} />
    }
    return ;
}

export default Description;