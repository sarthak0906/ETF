import React from 'react';
import Table from 'react-bootstrap/Table'
import '../static/css/TableStyle.css'

class AppTable extends React.Component {    
  constructor(props){
    super(props);
    console.log(props);
    //binding functions to the Component
    this.getHeader = this.getHeader.bind(this);
    this.getRowsData = this.getRowsData.bind(this);
    this.getKeys = this.getKeys.bind(this);
  }

  // ComponentDidMout(){
  //   this.props.
  // }
  
  // getting all te keys to the json data to diectly fetch the data later
  getKeys = function(){
    return Object.keys(this.props.data[0]);
  }
  
  // getting the headings for the heading of the table
  getHeader = function(){
    var keys = this.getKeys();
    return keys.map((key, index)=>{
      return <th key={key}>{key.toUpperCase()}</th>
    })
  }
  
  // getting data for each of the rows
  getRowsData = function(){
    var items = this.props.data;
    console.log(items[0])
    var keys = this.getKeys();
    return items.map((row, index)=>{
      return <tr key={index}><RenderRow key={index} data={row} keys={keys}/></tr>
    })
  }
  
  render() {
      return (
        <div>
          <Table striped bordered hover variant="dark">
          <thead className="TableHead">
            <tr>{this.getHeader()}</tr>
          </thead>
          <tbody>
            {this.getRowsData()}
          </tbody>
          </Table>
        </div>          
      );
  }
}

// functional Component to render one row at a time
const RenderRow = (props) =>{
  return props.keys.map((key, index)=>{
    if (key === "Time"){
      return <td key={props.data[index]} className="TableTime">{props.data[key]}</td>
    }
    return <td key={props.data[index]}>{
      (typeof(props.data[key]) === "number") ? Math.round(props.data[key] * 1000)/1000 : (props.data[key])
    }</td>
  })
}

export default AppTable