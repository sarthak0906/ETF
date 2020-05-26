import React, { useState, useEffect } from 'react';
import AppTable from './Table.js';
import Table from 'react-bootstrap/Table';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import SimilarETFList from './SimilarETFs';
import axios from 'axios';
import { ChartCanvas, Chart } from "react-stockcharts";
import PropTypes from "prop-types";

import { scaleTime } from "d3-scale";
import { curveMonotoneX } from "d3-shape";

import { AreaSeries } from "react-stockcharts/lib/series";
import { XAxis, YAxis } from "react-stockcharts/lib/axes";
import { fitWidth } from "react-stockcharts/lib/helper";
import { createVerticalLinearGradient, hexToRGBA } from "react-stockcharts/lib/utils";
import {
    BarSeries,
    CandlestickSeries,
    LineSeries,
    MACDSeries,
} from "react-stockcharts/lib/series";

const canvasGradient = createVerticalLinearGradient([
	{ stop: 0, color: hexToRGBA("#b5d0ff", 0.2) },
	{ stop: 0.7, color: hexToRGBA("#6fa4fc", 0.4) },
	{ stop: 1, color: hexToRGBA("#4286f4", 0.8) },
]);

class Live_Arbitrage extends React.Component{
    constructor(props){
        super(props);
    }

    state ={
        seconds: (new Date()).getSeconds(),
        LiveData: {},
        FullDay : {},
    }

    componentDidMount() {
        console.log(this.state.seconds);
        console.log("part 1")
        this.fetchETFLiveData()
        axios.get(`http://localhost:5000/ETfLiveArbitrage/Single/${this.props.ETF}`).then(res =>{
            console.log(res);
            this.setState({
                LiveData: res.data.Live,
                time: (new Date(res.data.Full_Day.Timestamp["0"])).toLocaleString(),
                FullDay: res.data.Full_Day,
            });
            console.log(this.state.FullDay);
        });
    }
   
  
    componentDidUpdate(prevProps,prevState) {
        const condition1=this.props.ETF !== prevProps.ETF;
        const condition2=this.props.startDate !== prevProps.startDate;
        if (condition1 || condition2) {
            axios.get(`http://localhost:5000/ETfLiveArbitrage/Single/${this.props.ETF}`).then(res =>{
                console.log(res);
                this.setState({
                    LiveData: res.data.Live,
                    FullDay: res.data.Full_Day,
                    time: (new Date(res.data.Full_Day.Timestamp["0"])).toLocaleString(),
                });
            });
            this.fetchETFLiveData();
        }
    }

  
    fetchETFLiveData(){
        setInterval(() => {
            this.setState({
                seconds : (this.state.seconds > 59) ? 0 : this.state.seconds + 1
            });
            console.log(this.state.seconds);
            if (this.state.seconds == 13){
                console.log("this is something")
                axios.get(`http://localhost:5000/ETfLiveArbitrage/Single/${this.props.ETF}`).then(res =>{
                    this.setState({
                        LiveData: res.data.Live,
                        time: (new Date(res.data.Full_Day.Timestamp["0"] - 0)).toLocaleString(),
                        FullDay: res.data.Full_Day,
                    });
                });
            }
        }, 1000)
    }

    render(){
        return (
            <Container fluid>
            <h4> Live Arbitrage </h4>
            <h5> {this.props.ETF} </h5>
            <h5> {this.state.time} </h5>
            <br />
            <Row>
                <Col xs={12} md={6}>
                    <div className="DescriptionTable">
                        {
                            (this.state.LiveData) ? <AppTable data={this.state.LiveData} /> : "Loadingg"
                        }
                    </div>
                </Col>
                <Col xs={12} md={6}>
                    <div className="DescriptionTable">
                        <LiveTable data={this.state.FullDay} />
                    </div>
                </Col>
            </Row>
        </Container>
        )
    }
}

const LiveTable = (props) => {
    console.log(props.data);
    if(props.data.Symbol == null){
        console.log(props.data);
        return "Loading";
    }
    const getKeys = function(someJSON){
        return Object.keys(someJSON);
    }

    const getRowsData = () => {
        var Symbols = getKeys(props.data.Symbol)

        return Symbols.map((key, index) => {
            // console.log(key);
            let cls = "";
            if (props.data.Arbitrage[key] < 0){
                cls = "Red";
            }
            if(props.data.Arbitrage[key] > 0){
                cls = "Green";
            }
            else {
                cls = "";
            }
            return (
                <tr key={index}>
                    <td>{new Date(props.data.Timestamp[key]).toLocaleTimeString()}</td>
                    <td className={cls}>{props.data.Arbitrage[key]}</td>
                    <td>{props.data.Spread[key]}</td>
                </tr>
            )
        })
    }

    return (
        <div className="Table">
          <Table striped bordered hover variant="dark">
          <thead className="TableHead">
            <tr>
                <td>Time</td>
                <td>Arbitrage</td>
                <td>Spread</td>
            </tr>
          </thead>
          <tbody>
            {getRowsData()}
          </tbody>
          </Table>
        </div>          
    );
}

export default Live_Arbitrage;