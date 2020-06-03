import React from 'react';
import ReactTable from 'react-table';
import "react-table/react-table.css";
import '../static/css/TableStyle.css'

var stringConstructor = "test".constructor;
var arrayConstructor = [].constructor;
var objectConstructor = ({}).constructor;

function whatIsIt(object) {
  if (object === null) {
    return "null";
  }
  if (object === undefined) {
    return "undefined";
  }
  if (object.constructor === stringConstructor) {
    return "String";
  }
  if (object.constructor === arrayConstructor) {
    return "Array";
  }
  if (object.constructor === objectConstructor) {
    return "Object";
  }
  return "don't know";
}

class AppTable extends React.Component{
  constructor(props){
    super(props);
    this.state = {};
  }

  // getting all te keys to the json data to diectly fetch the data later
  getKeys (someJSON){
    return Object.keys(someJSON);
  }

  getCols(clickableTable, live){
    var keys = this.getKeys(this.props.data[0]);
    var cols = [];

    if (clickableTable){
      return keys.map((el,i) => {
        return {Header: el,accessor: el, Cell: (<td onClick={() => this.props.submitFn(el)} >el</td>)};
      })
    }

    if (live){
      return keys.map((el, i) => {
        if (el == "Arbitrage") return {
          Header: el,
          accessor: el,
          Cell: row => {
            row.styles['color'] = '#fff';
            row.styles['backgroundColor'] = row.value < 0 ? 'red' : 'green';
            return row.value;
          }
        }
        else {
          return {Header: el,accessor: el};            
        }
      })
    }

    return keys.map((el, i) => {
      return {Header: el,accessor: el};
    });
  }

  TableStyling = {
    fontSize: '13px'
  };

  render(){
    if (this.props.data === {} || this.props.data === undefined || this.props.data === null){
      return "Lodaing ...";
    }
    else{
      const columns = this.getCols(this.props.clickableTable, this.props.live);
      return (
        <div>
          <ReactTable 
            data={this.props.data}
            defaultPageSize={this.props.data.length}
            showPagination={false}
            columns={columns}
            noDataText="No Data Available"
            filterable
            className="-striped -highlight bg-dark"
          />
        </div>
      )
    }
  }
}

// functional Component to render one row at a time
const RenderRow = (props) =>{
  if (whatIsIt(props.data) !== "Object"){
    return( 
      <tr>
        <td className="Main">{props.k}</td>
        <td>{props.data}</td>
      </tr>
    )
  }
  else {
    return(
      <tr>
        <td className="Main">{props.k}</td>
        {
          Object.keys(props.data).map((key, i) => (
            <td key={i}>{props.data[key]}</td>
          ))
        }
      </tr>
    );
  }
}


// functional Component to render one row at a time
const RenderRowClickable = (props) =>{
  if (whatIsIt(props.data) !== "Object"){
    return( 
      <tr>
        <td className="Main">{props.k}</td>
        <td>{props.data}</td>
      </tr>
    )
  }
  else {
    return(
      <tr onClick={() => props.submitFn(props.k)}>
        <td className="Main">{props.k}</td>
        {
          Object.keys(props.data).map((key, i) => (
            <td key={i}>{props.data[key]}</td>
          ))
        }
      </tr>
    );
  }
}

export default AppTable