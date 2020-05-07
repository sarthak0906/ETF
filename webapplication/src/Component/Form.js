import React, { useState } from 'react';
import Form from 'react-bootstrap/Form'
import FormControl from 'react-bootstrap/FormControl'
import Button from 'react-bootstrap/Button'
import InputGroup from 'react-bootstrap/InputGroup'
import DatePicker from "react-datepicker";
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import '../static/css/NavStyle.css';
import "react-datepicker/dist/react-datepicker.css";
 
// CSS Modules, react-datepicker-cssmodules.css
import 'react-datepicker/dist/react-datepicker-cssmodules.css';


function Former(props) {
  const [startDate, setDate] = useState(new Date(2020, 3, 16));
  const [stock, setStock] = useState("XLK");

  // handling date change as well as checking if date lies between 16-17 as data provided has only that
  const changeDate = (date) => {
    let d1 = new Date(2020,3,16);
    let d2 = new Date(2020,3,17);
    if (date.getTime() >= d1.getTime() && date.getTime() <= d2.getTime()){
      setDate(date);
    }
  }

  // Submit funtion to send state to parent to render 
  const submit = () => {
    props.submitFn(stock, startDate.getDate());
  }

  // handler for select input method
  const select = (event) => {
    setStock(event.target.value);
  }

  return (
    <Nav className="bg-light justify-content-between">
      <Navbar  className="bg-light">
        <Nav>
          <Nav.Item>
            <Nav.Link href="/ETF-Analysis">ETF-Analysis</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/ETF-Comparison" eventKey="ETF-Comparison">ETF-Comparison</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/ETF-Description" eventKey="ETF-Description">ETF-Description</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/Historical" eventKey="Historical">Historical</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/Live-Arbitrage" eventKey="Live-Arbitrage">Live-Arbitrage</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/Machine-Learning" eventKey="Machine-Learning">Machine-Learning</Nav.Link>
          </Nav.Item>
        </Nav>
      </Navbar>
      <Navbar className="bg-light">
        <Form inline >
          <Form.Group onChange={select}>
              <Form.Label className="FormLabel">Stock Select</Form.Label>
              <Form.Control className="FormInput" as="select">
                <option>XLK</option>
                <option>FTEC</option>
              </Form.Control>
            </Form.Group>
            <DatePicker
              className="FormInput"
              selected={startDate}
              onChange={changeDate}
            />
            <Button variant="primary" onClick={submit}>
              Submit
            </Button>
        </Form>
      </Navbar>
    </Nav>
  )
}

export default Former;