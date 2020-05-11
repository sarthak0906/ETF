import React, {useState, useEffect } from 'react';
import {
  PieChart, Pie, Sector, Cell,
} from 'recharts';
import AppTable from './Table.js';
import '../static/css/Description.css';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const Description = (props) => {
  console.log(props);
  var descurl = `/ETfDescription/EtfData/${props.ETF}/${props.startDate}`;
  // var descurl = `/ETfDescription/EtfData/${props.ETF}/20200517`;
  var DescriptionTable = updateTableData("descurl");

  
  var holdingsurls = `/ETfDescription/Holdings/${props.ETF}/${props.startDate}`;
  // var holdingsurls = `/ETfDescription/Holdings/${props.ETF}/20200517`;
  var HoldingsTable = updateTableData("holdingsurls");

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
    // console.log(url);
    
    if ("descurl"){
      var df = {
        "SCL": {
            "TickerName": "Stepan Co",
            "TickerWeight": 7.0852
        },
        "KWR": {
            "TickerName": "Quaker Chemical Corp",
            "TickerWeight": 6.6852
        },
        "IOSP": {
            "TickerName": "Innospec Inc",
            "TickerWeight": 6.5719
        },
        "FUL": {
            "TickerName": "HB Fuller Co",
            "TickerWeight": 5.9268
        },
        "CLF": {
            "TickerName": "Cleveland-Cliffs Inc",
            "TickerWeight": 5.0702
        },
        "KALU": {
            "TickerName": "Kaiser Aluminum Corp",
            "TickerWeight": 4.5402
        },
        "BCC": {
            "TickerName": "Boise Cascade Co",
            "TickerWeight": 4.1623
        },
        "GCP": {
            "TickerName": "GCP Applied Technologies Inc",
            "TickerWeight": 3.4967
        },
        "ARNC": {
            "TickerName": "Arconic Corp (PITTSBURGH)",
            "TickerWeight": 3.4145
        },
        "LTHM": {
            "TickerName": "Livent Corp",
            "TickerWeight": 3.3925
        },
        "SWM": {
            "TickerName": "Schweitzer-Mauduit International Inc",
            "TickerWeight": 3.3805
        },
        "MTRN": {
            "TickerName": "Materion Corp",
            "TickerWeight": 3.3165
        },
        "FOE": {
            "TickerName": "Ferro Corp",
            "TickerWeight": 2.9378
        },
        "TSE": {
            "TickerName": "Trinseo SA",
            "TickerWeight": 2.9246
        },
        "NP": {
            "TickerName": "Neenah Inc",
            "TickerWeight": 2.8185
        },
        "HCC": {
            "TickerName": "Warrior Met Coal Inc",
            "TickerWeight": 2.3387
        },
        "GLT": {
            "TickerName": "P H Glatfelter Co",
            "TickerWeight": 2.1545
        },
        "TG": {
            "TickerName": "Tredegar Corp",
            "TickerWeight": 1.5196
        },
        "AVD": {
            "TickerName": "American Vanguard Corp",
            "TickerWeight": 1.4889
        },
        "MYE": {
            "TickerName": "Myers Industries Inc",
            "TickerWeight": 1.4536
        },
        "CLW": {
            "TickerName": "Clearwater Paper Corp",
            "TickerWeight": 1.3293
        },
        "MERC": {
            "TickerName": "Mercer International Inc",
            "TickerWeight": 1.3049
        },
        "HWKN": {
            "TickerName": "Hawkins Inc",
            "TickerWeight": 1.2499
        },
        "FF": {
            "TickerName": "FutureFuel Corp",
            "TickerWeight": 1.2025
        },
        "KRA": {
            "TickerName": "Kraton Corp",
            "TickerWeight": 1.1989
        },
        "SXC": {
            "TickerName": "SunCoke Energy Inc",
            "TickerWeight": 1.1375
        },
        "ASIX": {
            "TickerName": "AdvanSix Inc",
            "TickerWeight": 1.0991
        },
        "USCR": {
            "TickerName": "US Concrete Inc",
            "TickerWeight": 1.0945
        },
        "KOP": {
            "TickerName": "Koppers Holdings Inc",
            "TickerWeight": 0.9908
        },
        "HAYN": {
            "TickerName": "Haynes International Inc",
            "TickerWeight": 0.9753
        },
        "CENX": {
            "TickerName": "Century Aluminum Co",
            "TickerWeight": 0.7836
        },
        "TMST": {
            "TickerName": "TimkenSteel Corp",
            "TickerWeight": 0.4689
        },
        "ZEUS": {
            "TickerName": "Olympic Steel Inc",
            "TickerWeight": 0.3056
        },
        "RYAM": {
            "TickerName": "Rayonier Advanced Materials Inc",
            "TickerWeight": 0.216
        },
        "LXU": {
            "TickerName": "LSB Industries Inc",
            "TickerWeight": 0.1477
        },
        "CASH": {
            "TickerName": "Cash Component",
            "TickerWeight": 0.0447
        }
      }
      console.log("DESCURL");
      return (
        <div>
          <AppTable data={df} />
          <PieChart width={400} height={400}>
            <Pie
              data={df}
              cx={200}
              cy={200}
              labelLine={false}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {
                df1.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
              }
            </Pie>
          </PieChart>
        </div>
      )
    }
    
    else {
      var df1 = {
        "SCL": {
            "TickerName": "Stepan Co",
            "TickerWeight": 7.0852
        },
        "KWR": {
            "TickerName": "Quaker Chemical Corp",
            "TickerWeight": 6.6852
        },
        "IOSP": {
            "TickerName": "Innospec Inc",
            "TickerWeight": 6.5719
        },
        "FUL": {
            "TickerName": "HB Fuller Co",
            "TickerWeight": 5.9268
        },
        "CLF": {
            "TickerName": "Cleveland-Cliffs Inc",
            "TickerWeight": 5.0702
        },
        "KALU": {
            "TickerName": "Kaiser Aluminum Corp",
            "TickerWeight": 4.5402
        },
        "BCC": {
            "TickerName": "Boise Cascade Co",
            "TickerWeight": 4.1623
        },
        "GCP": {
            "TickerName": "GCP Applied Technologies Inc",
            "TickerWeight": 3.4967
        },
        "ARNC": {
            "TickerName": "Arconic Corp (PITTSBURGH)",
            "TickerWeight": 3.4145
        },
        "LTHM": {
            "TickerName": "Livent Corp",
            "TickerWeight": 3.3925
        },
        "SWM": {
            "TickerName": "Schweitzer-Mauduit International Inc",
            "TickerWeight": 3.3805
        },
        "MTRN": {
            "TickerName": "Materion Corp",
            "TickerWeight": 3.3165
        },
        "FOE": {
            "TickerName": "Ferro Corp",
            "TickerWeight": 2.9378
        },
        "TSE": {
            "TickerName": "Trinseo SA",
            "TickerWeight": 2.9246
        },
        "NP": {
            "TickerName": "Neenah Inc",
            "TickerWeight": 2.8185
        },
        "HCC": {
            "TickerName": "Warrior Met Coal Inc",
            "TickerWeight": 2.3387
        },
        "GLT": {
            "TickerName": "P H Glatfelter Co",
            "TickerWeight": 2.1545
        },
        "TG": {
            "TickerName": "Tredegar Corp",
            "TickerWeight": 1.5196
        },
        "AVD": {
            "TickerName": "American Vanguard Corp",
            "TickerWeight": 1.4889
        },
        "MYE": {
            "TickerName": "Myers Industries Inc",
            "TickerWeight": 1.4536
        },
        "CLW": {
            "TickerName": "Clearwater Paper Corp",
            "TickerWeight": 1.3293
        },
        "MERC": {
            "TickerName": "Mercer International Inc",
            "TickerWeight": 1.3049
        },
        "HWKN": {
            "TickerName": "Hawkins Inc",
            "TickerWeight": 1.2499
        },
        "FF": {
            "TickerName": "FutureFuel Corp",
            "TickerWeight": 1.2025
        },
        "KRA": {
            "TickerName": "Kraton Corp",
            "TickerWeight": 1.1989
        },
        "SXC": {
            "TickerName": "SunCoke Energy Inc",
            "TickerWeight": 1.1375
        },
        "ASIX": {
            "TickerName": "AdvanSix Inc",
            "TickerWeight": 1.0991
        },
        "USCR": {
            "TickerName": "US Concrete Inc",
            "TickerWeight": 1.0945
        },
        "KOP": {
            "TickerName": "Koppers Holdings Inc",
            "TickerWeight": 0.9908
        },
        "HAYN": {
            "TickerName": "Haynes International Inc",
            "TickerWeight": 0.9753
        },
        "CENX": {
            "TickerName": "Century Aluminum Co",
            "TickerWeight": 0.7836
        },
        "TMST": {
            "TickerName": "TimkenSteel Corp",
            "TickerWeight": 0.4689
        },
        "ZEUS": {
            "TickerName": "Olympic Steel Inc",
            "TickerWeight": 0.3056
        },
        "RYAM": {
            "TickerName": "Rayonier Advanced Materials Inc",
            "TickerWeight": 0.216
        },
        "LXU": {
            "TickerName": "LSB Industries Inc",
            "TickerWeight": 0.1477
        },
        "CASH": {
            "TickerName": "Cash Component",
            "TickerWeight": 0.0447
        }
      }
      console.log("HOLDINGURL");
      return (
        <div>
          <AppTable data={df1} />
          <PieChart width={400} height={400}>
            <Pie
              data={df1}
              cx={200}
              cy={200}
              labelLine={false}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {
                df1.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
              }
            </Pie>
          </PieChart>
        </div>
      )
    }

    // fetch(url).then(res => console.log(res.json()))
    // .then(df => {
    //   console.log(df);
    //   return <AppTable data={df} />
    // });
    return ;
}

export default Description;