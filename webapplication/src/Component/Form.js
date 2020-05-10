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
import { Link } from 'react-router-dom';


// CSS Modules, react-datepicker-cssmodules.css
import 'react-datepicker/dist/react-datepicker-cssmodules.css';


function Former(props) {
  const [startDate, setDate] = useState(new Date(2020, 3, 16));
  const [stock, setStock] = useState("XLK");
  const arr = ["BMLP","IHI","SZK","JHMC","FHLC","PUI","KBWB","FTXG","XLV","XBI","RORE","PSCM","PASS","IEO","IYZ","XLY","PSCF","MRRL","PXE","BNKU","XLC","XHB","PPH","XRT","NUGT","FDIS","XWEB","FDN","RTM","SEF","USD","QABA","DRN","KBE","TAWK","IBB","UGE","PSCE","SCC","WANT","RXL","EVX","KRE","DRV","BNKD","BTEC","ROKT","BBC","SOXS","GASX","FXZ","CNRG","PTH","XHE","XLP","HDGE","FXD","FTEC","REZ","XITK","TECS","IHF","DUSL","XLF","ZIG","IYG","PBE","DDG","ZBIO","SCHH","FINU","SOXX","XLB","FRI","IECS","XPH","IYC","SIJ","SKYY","IYE","PKB","RETL","RYU","FTXL","PPA","PYZ","FXU","AMZA","RWR","FMAT","XLI","XLK","REK","ITB","BBH","RYE","BBP","IEDI","IAI","PSCT","TDV","XLE","JHMA","LABU","PPTY","JHME","XSD","VPC","REML","KBWP","DIG","UYM","EWRE","DPST","ROOF","MORL","FTXR","FUTY","XOP","PSL","PXJ","PSI","FTXO","IGN","RTH","IHE","FXH","BBRE","PSCI","ROM","VCR","NAIL","FIVG","MLPQ","ONLN","QQQ","NRGO","AMLP","XLU","FBT","JHMS","SKF","PJP","VNQ","VGT","INDS","CWEB","SMN","WCLD","XTN","ERY","UTES","HOMZ","RHS","FIDU","RDOG","UXI","SRS","IYF","TPOR","PTF","VDE","IGE","JHMH","DUG","PBW","CLIX","JNUG","NURE","MLPA","XNTK","IYM","FIW","PXQ","QTEC","OIH","KIE","FINZ","IYT","XSW","LABD","XHS","JHMU","IAT","PEZ","IFRA","UPW","IEFN","FXR","RGI","ZMLP","VHT","XAR","IGM","RYT","IYW","IYK","IEHS","UCC","VAW","XME","IEZ","PHO","ITA","GASL","SMH","VPU","PSCD","PSCH","PSJ","SDP","NEED","PNQI","SOXL","SSG","KBWR","SRVR","XLRE","FCG","VIS","JHMT","IAK","KBWY","MLPX","ICF","PXI","PAVE","REW","HAIL","DRIP","SLX","PILL","PBS","AIRR","IDU","FITE","IYH","REM","ERX","MLPB","PEJ","NRGU","XTL","BIZD","ARKG","NETL","RCD","SIMS","IETC","RYH","RYF","NRGD","VDC","XES","MORT","FREL","FENY","TDIV","FXG","PFI","BUYN","FXL","PSR","PSCU","SBIO","PRN","FSTA","DFEN","IYR","VOX","FXN","GUSH","CNCR","MLPI","URE","CURE","LACK","UTSL","VMOT","IGV","WDRW","TECL"];
  const [a, setA] = useState(arr);

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
    props.submitFn(stock, startDate.getDate() + '-' + startDate.getMonth() + '-' + startDate.getFullYear());
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
            <Nav.Link as={Link} to="/ETF-Analysis">ETF-Analysis</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link as={Link} to="/ETF-Comparison" eventKey="ETF-Comparison">ETF-Comparison</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link as={Link} to="/ETF-Description" eventKey="ETF-Description">ETF-Description</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link as={Link} to="/Historical" eventKey="Historical">Historical</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link as={Link} to="/Live-Arbitrage" eventKey="Live-Arbitrage">Live-Arbitrage</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link as={Link} to="/Machine-Learning" eventKey="Machine-Learning">Machine-Learning</Nav.Link>
          </Nav.Item>
        </Nav>
      </Navbar>
      <Navbar className="bg-light">
        <Form inline >
            <Form.Group onChange={select}>
              <Form.Label className="FormLabel">Stock Select</Form.Label>
              <Form.Control className="FormInput" as="select">
                {FormSelect(a)}
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

const FormSelect = (arr) => {
  return arr.map((element, index) => {
    return <option>{element}</option>
  })
}

export default Former;