import React from 'react';
// react table
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
  getKeys (someJSON) {
    return Object.keys(someJSON);
  }

  getCols (clickableTable, live) {
    var keys = this.getKeys(this.props.data[0]);
    var cols = [];
    if (clickableTable){
      return keys.map((el, i) => {
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
    })
  }

  render() {
    if (this.props.data == "" || this.props.data == {} || this.props.data == undefined){
      return "Loading";
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
            className="-striped -highlight bg-dark" />
        </div>
      );
    }
  }
}

// functional Component to render one row at a time
const RenderLiveData = (props) =>{
  // console.log(props);
  if(props.value < 0){
    return( 
      <td style={{backgroundColor: "red", height: "100%"}} className="Red"> {props.value} </td>
    )
  }
  else if(props.value < 0){
    return( 
      <td className="Green"> {props.value} </td>
    )
  }
  else{
    return( 
      <td> {props.value} </td>
    )
  }
}

export default AppTable