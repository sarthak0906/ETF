import React from 'react';
import Table from 'react-bootstrap/Table'
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

const AppTable = (props) => {
  // getting all te keys to the json data to diectly fetch the data later
  const getKeys = function(someJSON){
    return Object.keys(someJSON);
  }

  const MainKeys = getKeys(props.data);
  
  // getting the headings for the heading of the table
  const getHeader = function(){
    console.log(whatIsIt(props.data[MainKeys[0]]));
    var keys = (whatIsIt(props.data[MainKeys[0]]) == "Object") ? getKeys(props.data[MainKeys[0]]) : [];
    keys.unshift("");
    console.log(keys);
    return keys.map((key, index)=>{
      // console.log(key);
      return <th key={key}>{key.toUpperCase()}</th>
    })
  }
  
  // getting data for each of the rows
  const getRowsData = function(){
    var keys = (whatIsIt(props.data[MainKeys[0]]) != "Object") ? getKeys(props.data[MainKeys[0]]) : [];
    return MainKeys.map((Key1, index) => {
      var row = (typeof(props.data[Key1]) == Object) ? props.data[Key1].values() : props.data[Key1];
      console.log(row);
      return <RenderRow k={Key1} data={row} />
    }) 
    // var items = props.data;
    // var keys = getKeys();
    // return items.map((row, index)=>{
    //   return <tr key={index}><RenderRow key={index} data={row} keys={keys}/></tr>
    // })
  }
  
  return (
    <div>
      <Table striped bordered hover variant="dark">
      <thead className="TableHead">
        <tr>{getHeader()}</tr>
      </thead>
      <tbody>
        {getRowsData()}
      </tbody>
      </Table>
    </div>          
  );
}

// functional Component to render one row at a time
const RenderRow = (props) =>{
  if (whatIsIt(props.data) != "Object"){
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
            <td>{props.data[key]}</td>
          ))
        }
      </tr>
    );
  }
  return props.data.map((element) => {
    return <td>{(typeof(element) == "number") ? Math.round(element * 1000) / 1000 : element}</td> 
  })
}

export default AppTable