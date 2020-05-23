import React from "react";

import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

const divStyle = {
  paddingTop: '10%',
};


const EmailVerification = () => {
return (
  <Container fluid>
    <Row className="justify-content-center">
      <Col className="etfArbitrageTable align-item-center" style={divStyle} xs={12} md={3}>
        <Form>
          <Form.Group controlId="formBasicPassword">
            <Form.Label>Enter Verification Code</Form.Label>
            <Form.Control type="password" placeholder="Password" />
          </Form.Group>
          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </Col>
    </Row>
   </Container>
);
};


export default EmailVerification;

