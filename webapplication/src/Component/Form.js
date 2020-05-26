import React, { Component } from 'react';
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import DatePicker from "react-datepicker";
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import '../static/css/NavStyle.css';
import "react-datepicker/dist/react-datepicker.css";
import { Link } from 'react-router-dom';
import moment from 'moment'
import {
	AuthenticationDetails,
	CognitoUserPool,
	CognitoUserAttribute,
	CognitoUser,
	CognitoUserSession,
} from "amazon-cognito-identity-js";
  
// CSS Modules, react-datepicker-cssmodules.css
import 'react-datepicker/dist/react-datepicker-cssmodules.css';

const userPool = new CognitoUserPool({UserPoolId: 'ap-south-1_x8YZmKVyG', ClientId: '2j72c46s52rm3us8rj720tsknd'});

export function logout(username) {
	var cognitoUser = new CognitoUser({
	  Username: username,
	  Pool: userPool
	});
  
	// call SigOut on User
	cognitoUser.signOut();
}

class Former extends Component{
	state={
	    arr : ["XLK", "BMLP","IHI","SZK","JHMC","FHLC","PUI","KBWB","FTXG","XLV","XBI","RORE","PSCM","PASS","IEO","IYZ","XLY","PSCF","MRRL","PXE","BNKU","XLC","XHB","PPH","XRT","NUGT","FDIS","XWEB","FDN","RTM","SEF","USD","QABA","DRN","KBE","TAWK","IBB","UGE","PSCE","SCC","WANT","RXL","EVX","KRE","DRV","BNKD","BTEC","ROKT","BBC","SOXS","GASX","FXZ","CNRG","PTH","XHE","XLP","HDGE","FXD","FTEC","REZ","XITK","TECS","IHF","DUSL","XLF","ZIG","IYG","PBE","DDG","ZBIO","SCHH","FINU","SOXX","XLB","FRI","IECS","XPH","IYC","SIJ","SKYY","IYE","PKB","RETL","RYU","FTXL","PPA","PYZ","FXU","AMZA","RWR","FMAT","XLI","REK","ITB","BBH","RYE","BBP","IEDI","IAI","PSCT","TDV","XLE","JHMA","LABU","PPTY","JHME","XSD","VPC","REML","KBWP","DIG","UYM","EWRE","DPST","ROOF","MORL","FTXR","FUTY","XOP","PSL","PXJ","PSI","FTXO","IGN","RTH","IHE","FXH","BBRE","PSCI","ROM","VCR","NAIL","FIVG","MLPQ","ONLN","QQQ","NRGO","AMLP","XLU","FBT","JHMS","SKF","PJP","VNQ","VGT","INDS","CWEB","SMN","WCLD","XTN","ERY","UTES","HOMZ","RHS","FIDU","RDOG","UXI","SRS","IYF","TPOR","PTF","VDE","IGE","JHMH","DUG","PBW","CLIX","JNUG","NURE","MLPA","XNTK","IYM","FIW","PXQ","QTEC","OIH","KIE","FINZ","IYT","XSW","LABD","XHS","JHMU","IAT","PEZ","IFRA","UPW","IEFN","FXR","RGI","ZMLP","VHT","XAR","IGM","RYT","IYW","IYK","IEHS","UCC","VAW","XME","IEZ","PHO","ITA","GASL","SMH","VPU","PSCD","PSCH","PSJ","SDP","NEED","PNQI","SOXL","SSG","KBWR","SRVR","XLRE","FCG","VIS","JHMT","IAK","KBWY","MLPX","ICF","PXI","PAVE","REW","HAIL","DRIP","SLX","PILL","PBS","AIRR","IDU","FITE","IYH","REM","ERX","MLPB","PEJ","NRGU","XTL","BIZD","ARKG","NETL","RCD","SIMS","IETC","RYH","RYF","NRGD","VDC","XES","MORT","FREL","FENY","TDIV","FXG","PFI","BUYN","FXL","PSR","PSCU","SBIO","PRN","FSTA","DFEN","IYR","VOX","FXN","GUSH","CNCR","MLPI","URE","CURE","LACK","UTSL","VMOT","IGV","WDRW","TECL"],
	    date: moment(this.props.startDate, 'YYYYMMDD').toDate(),
	    ETF: this.props.ETF
	}

	constructor(props){
    	super(props);
	}
	
	// handling date change as well as checking if date lies between 16-17 as data provided has only that
  	changeDate = (selecteddate) => {
  		var DateCopy =  this.state.date;
  		DateCopy = selecteddate;
  		this.setState({
 	   		date:DateCopy,
 	   	});
 	}

  	// Submit funtion to send state to parent to render 
  	submit = () => {
  		const tempDate=this.state.date;
  		var passdate=''
	    if (tempDate.getMonth() < 9){
	      if (tempDate.getDate() < 10){
	      	passdate=tempDate.getFullYear() + '0' + (tempDate.getMonth()+1) + '0' + tempDate.getDate();
	      }
	      passdate=tempDate.getFullYear() + '0' + (tempDate.getMonth()+1) + '' + tempDate.getDate();
	    }
	    else {
	      if (tempDate.getDate() < 10){
	      	passdate=tempDate.getFullYear() + '' + (tempDate.getMonth()+1) + '0' + tempDate.getDate();
	      }
	      passdate=tempDate.getFullYear() + '' + (tempDate.getMonth()+1) + '' + tempDate.getDate();
	    }
		this.props.SubmitFn(this.state.ETF, passdate);
	}

  	
  	FormSelect = (arr) => {
		return arr.map((element, index) => { 
	    	return <option key={index}>{element}</option>
  		})
	}

	select =  (event) => {
		var DateCopy =  this.state.ETF;
  		DateCopy = event.target.values;
  		
		 this.setState({
 	   		ETF:event.target.value
 	   	});
  	}

  render(){
  	return (
	    <Nav className="bg-dark justify-content-between nav">
	      <Navbar  className="bg-dark">
	        <Nav>
	          <Nav.Item>
	            <Nav.Link style={{color: 'white'}} as={Link} to="/ETF-Comparison" eventKey="ETF-Comparison">ETF-Comparison</Nav.Link>
	          </Nav.Item>
	          <Nav.Item>
	            <Nav.Link style={{color: 'white'}} as={Link} to="/ETF-Description" eventKey="ETF-Description">ETF-Description</Nav.Link>
	          </Nav.Item>
	          <Nav.Item>
	            <Nav.Link style={{color: 'white'}} as={Link} to="/HistoricalArbitrage" eventKey="Historical">Historical Arbitrage</Nav.Link>
	          </Nav.Item>
	          <Nav.Item>
	            <Nav.Link style={{color: 'white'}} as={Link} to="/Live-Arbitrage-single" eventKey="Live-Arbitrage">Live-Arbitrage (Focus)</Nav.Link>
	          </Nav.Item>
	          <Nav.Item>
	            <Nav.Link style={{color: 'white'}} as={Link} to="/Live-Arbitrage" eventKey="Live-Arbitrage">Live-Arbitrage</Nav.Link>
	          </Nav.Item>
	          <Nav.Item>
	            <Nav.Link style={{color: 'white'}} as={Link} to="/Machine-Learning" eventKey="Machine-Learning">Machine-Learning</Nav.Link>
	          </Nav.Item>
	        </Nav>
	      </Navbar>
	      <Navbar className="bg-dark">
	        <Form inline >
	            <Form.Group onChange={this.select}>
	              <Form.Label className="FormLabel">Stock Select</Form.Label>
	              <Form.Control className="FormInput" as="select" value={this.state.ETF}>
	                {this.FormSelect(this.state.arr)}
	              </Form.Control>
	            </Form.Group>
	            <DatePicker
	              className="FormInput"
	              selected={this.state.date}
	              onChange={this.changeDate}
	            />
	            <Button variant="primary" onClick={this.submit}>
	              Submit
	            </Button>
	        </Form>
			<Button variant="dark" onClick={() => {logout(localStorage.getItem("username"))}}>
				logout
			</Button>
	      </Navbar>
	    </Nav>
	  )
	}

}

export default Former;