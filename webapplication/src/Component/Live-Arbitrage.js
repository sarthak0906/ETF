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

class Live_Arbitrage extends React.Component{
    constructor(props){
        super(props);
    }

    state ={
        seconds: (new Date()).getSeconds(),
        LiveData: {},
    }

    componentDidMount() {
        console.log(this.state.seconds);
        if (this.state.seconds > 12 && this.state.seconds < 16){
            console.log("part 1")
            this.fetchETFLiveData()
        }
        else if (this.state.seconds > 16){
            console.log("part 2")
            console.log((73 - this.state.seconds))
            setTimeout(() => {console.log("part 2"); this.fetchETFLiveData()}, ((73 - this.state.seconds) * 1000))
        }
        else {
            console.log("part 3")
            console.log((13 - this.state.seconds))
            setTimeout(() => {console.log("part 3"); this.fetchETFLiveData()}, ((13 - this.state.seconds) * 1000))
        }
    }
   
  
    componentDidUpdate(prevProps,prevState) {
        const condition1=this.props.ETF !== prevProps.ETF;
        const condition2=this.props.startDate !== prevProps.startDate;
        if (condition1 || condition2) {
            this.fetchETFLiveData();
        }
    }

  
    fetchETFLiveData(){
        setInterval(() => {
            console.log("this is something")
            console.log((new Date()).getSeconds());
            axios.get(`http://localhost:5000/ETfLiveArbitrage/Single/${this.props.ETF}`).then(res =>{
                console.log(res.data);
                this.setState({
                    LiveData: res,
                });
            });
        }, 60000)
    }

    render(){
        return (
            <Container fluid>
            <h4> Live Arbitrage </h4>
            <h5> {this.props.ETF} </h5>
            <br />
            <Row>
                <Col xs={12} md={12}>
                    <div className="DescriptionTable">
                        {
                            (this.state.LiveData != null) ? <AppTable data={this.state.LiveData} /> : ""
                        }
                    </div>
                </Col>
            </Row>
        </Container>
        )
    }
}

export default Live_Arbitrage;