import React from 'react';
import { Link } from 'react-router-dom';

function Header(){
	return (
		<header style={headerStyle}>
			<h1>ToDoList</h1>
			<Link style={linkstyle} to="/">Home</Link> | <Link style={linkstyle} to="/about">About</Link>
		</header>
		)
}

const headerStyle = {
	background : '#333',
	color: '#fff',
	textAlign :'ceter',
	padding: '10px'
}

const linkstyle = {
	color:'#fff',
	textDecoration: 'none'
}

export default Header

