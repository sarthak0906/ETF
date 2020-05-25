import React, {Component} from 'react';


class StockDesriptionHeader extends Component {
	
	render(){
		return (
		<div>
			<p> {this.props.ETF} </p>
    		<p> Date of Arbitrage : {this.props.startDate}</p>
    		<ColoredLine color="black" />
		</div>
		);
	}
}


const ColoredLine = ({ color }) => (
<hr
    style={{
        color: color,
        backgroundColor: color
    }}
/>
);

export default StockDesriptionHeader;

