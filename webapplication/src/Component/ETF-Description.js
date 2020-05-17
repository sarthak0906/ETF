import React from 'react';
import PieChart from './PieChart';
import AppTable from './Table.js';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import SPDR from './Sector-SPDR';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button';

class Description extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      DescriptionData : {},
      HoldingsData : {},
      DescriptionTableData : "",
      HoldingsTableData : "",
    }
    this.fetchData = this.fetchData.bind(this);
  }

  fetchData() {
    fetch(`http://localhost:5000/ETfDescription/EtfData/${this.props.ETF}/${this.props.startDate}`)
    .then(res =>{return res.clone().json()})
    .then(
      async (result) => {
          await this.setState({isLoaded : true, DescriptionData: result});
          await this.setState({DescriptionTableData : <DescriptionTableData data={this.state.DescriptionData} />});
      },
      async (error) => {
        await this.setState({isLoaded : false, error : error});
      }
    )
  fetch(`http://localhost:5000/ETfDescription/Holdings/${this.props.ETF}/${this.props.startDate}`)
    .then(res => { return res.clone().json()})
    .then(
      async (result) => {
        await this.setState({isLoaded : true, HoldingsData: result});
        await this.setState({HoldingsTableData : <HoldingsTableData data={this.state.HoldingsData} />});
      },
      async (error) => {
        await this.setState({isLoaded : false, error : error});
      }
    )
  }

  componentDidMount() {
    this.fetchData();
  }

  async UNSAFE_componentWillReceiveProps(props) {
    this.fetchData();
  }
  
  render () {
    return (
      <Container fluid>
        <h4> ETF-Description </h4>
        <h5> {this.props.ETF} </h5>
        <h4> <strong>{this.state.DescriptionData.AnnualDividendRate}</strong>  {this.state.DescriptionData.AnnualDividendYield} </h4>
        <br />
        <Row>
          <Col>
          <h6><strong>ETF Description</strong></h6>
            {
              this.state.DescriptionTableData 
            }
          </Col>
          <Col>
          <h6><strong>ETF Holdings Data</strong></h6>
            {
              this.state.HoldingsTableData
            }
          </Col>
          <Col>
            <SPDR submitFn={this.props.submitFn}/>
          </Col>
        </Row>
     </Container>
    )
  }
}

const DescriptionTableData = (props) => {
  return (
    <div className="DescriptionTable">
      <AppTable data={props.data} />
    </div>
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