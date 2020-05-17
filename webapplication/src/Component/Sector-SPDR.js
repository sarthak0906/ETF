import React, { PureComponent } from 'react';
import { PieChart, Pie, Sector, Cell } from 'recharts';

const RADIAN = Math.PI / 180;
const renderActiveShape = (props) => {
  const {
    cx, cy, outerRadius, startAngle, endAngle,
    fill
  } = props;

  return (
    <g>
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={0}
        outerRadius={outerRadius + 10}
        fill={fill}
      />
    </g>
  );
};

const renderCustomizedLabel = ({
  cx, cy, midAngle, innerRadius, outerRadius, percent, index, key
}) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'}>
      {`${key}`}
    </text>
  );
};

export default class Example extends PureComponent {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            activeIndex: 0,
            COLORS     : ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']
        };
    }

    async componentDidMount (){
        var d = [
            { key: 'XLE', value: 1 },
            { key: 'XLU', value: 1 },
            { key: 'XLK', value: 1 },
            { key: 'XLB', value: 1 },
            { key: 'XLP', value: 1 },
            { key: 'XLY', value: 1 },
            { key: 'XLI', value: 1 },
            { key: 'XLC', value: 1 },
            { key: 'XLV', value: 1 },
            { key: 'XLF', value: 1 },
            { key: 'XLRE', value: 1 }
        ]
        this.setState({data: d});
    }
    
    onPieEnter = (data, index) => {
        this.setState({
            activeIndex: index,
        });
    };
    
    render() {
        return (
        <PieChart width={400} height={350}>
          <Pie
            activeIndex={this.state.activeIndex}
            activeShape={renderActiveShape}
            data={this.state.data}
            cx={200}
            cy={200}               
            outerRadius={90}
            fill="#8884d8"
            dataKey="value"
            labelLine={false}
            label={renderCustomizedLabel}
            onMouseEnter={this.onPieEnter}
            onClick={(e) => this.props.submitFn(e.key)}
          >
          {
              this.state.data.map((entry, index) => <Cell key={index} fill={this.state.COLORS[index % this.state.COLORS.length]}/>)
          }
          </Pie>
        </PieChart>
        );
    }
}