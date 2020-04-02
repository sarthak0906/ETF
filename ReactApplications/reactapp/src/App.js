import React from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route} from 'react-router-dom';

import './App.css';
import Todo from './components/Todo';
import AddToDo from './components/AddToDo';
import About from './components/pages/About';
import Header from './components/layout/Header';



class App extends React.Component {
	state={
		todos:[]
	}
	
	componentDidMount(){
		axios.get('https://jsonplaceholder.typicode.com/todos?_limit=10').then(res=>this.setState({todos:res.data}))
	}

	// Toggle Complete
	markComplete = (id) => {
		this.setState({ todos: this.state.todos.map(todo => {
			if(todo.id === id){
				todo.completed = !todo.completed
			}
			return todo;
		})})
	}

	delTodo = (id) => {
		axios.delete('https://jsonplaceholder.typicode.com/todos/${id}').then(
			res => this.setState({ todos: [...this.state.todos.filter(todo => todo.id!==id)]}));
		console.log(id)
	}


	// Add Todo
	addToDo = (title) => {
		
		//const newTodo = {
		//	id: 5,
		//	title: title,
		//	compelted: false
		//}
		axios.post('https://jsonplaceholder.typicode.com/todos',{
			title,
			completed:false
		}).then(res => this.setState({todos:[...this.state.todos, res.data]}));
	}

	render(){
		return (
		<Router>
	      <div className="App">
	      	<div className="container">
		      	<Header />
		      	<Route exact path="/" render={props => (
		      		<React.Fragment>
		      			<AddToDo addToDo = {this.addToDo} />
		      			<Todo todos={this.state.todos} markComplete={this.markComplete} delTodo={this.delTodo}/>
		      		</React.Fragment>
	      		)}/>

	      		<Route path="/about" component={About}/>
			</div>
	      </div>
  		</Router>
	    );
  	}
}

export default App;
 