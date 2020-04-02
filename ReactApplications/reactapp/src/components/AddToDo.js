import React, {Component} from 'react';
import PropTypes from 'prop-types';

export class AddToDo extends Component{
	state = {
		title:''
	}

	onChange = (e) => this.setState({
		[e.target.name]:e.target.value
	});

	onSubmit = (e) => {
		e.preventDefault();
		this.props.addToDo(this.state.title);
		this.setState({title: '' });
	}

	render(){
		return(
			<form style={{display:'flex'}} onSubmit={this.onSubmit}>
				<input type="text" name="title" style={{flex:'10', padding:'5px'}} placeholder="Add ToDo.."
				value={this.state.title}
				onChange={this.onChange}
				/>
				<input type="submit" name="Subnit" className="btn" style={{flex:'1'}}/>
			</form>
			)
		}
	}


// PropTypes
AddToDo.propTypes = {
	addToDo: PropTypes.func.isRequired,
}

export default AddToDo;

