import React, { PureComponent } from 'react';
import { PieChart, Pie, Sector, Cell } from 'recharts';

const renderActiveShape = (props) => {
  const RADIAN = Math.PI / 180;
  const {
    cx, cy, midAngle, innerRadius, outerRadius, startAngle, endAngle,
    fill, payload, percent, value,
  } = props;
  const sin = Math.sin(-RADIAN * midAngle);
  const cos = Math.cos(-RADIAN * midAngle);
  const sx = cx + (outerRadius + 10) * cos;
  const sy = cy + (outerRadius + 10) * sin;
  const mx = cx + (outerRadius + 30) * cos;
  const my = cy + (outerRadius + 30) * sin;
  const ex = mx + (cos >= 0 ? 1 : -1) * 22;
  const ey = my;
  const textAnchor = cos >= 0 ? 'start' : 'end';

  return (
    <g>
      <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>{payload.name}</text>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
      />
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={outerRadius + 6}
        outerRadius={outerRadius + 10}
        fill={fill}
      />
      <path d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`} stroke={fill} fill="none" />
      <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
      <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} textAnchor={textAnchor} fill="#333">{`${value}`}</text>
    </g>
  );
};


export default class Example extends PureComponent {
    constructor(props) {
        super(props);
        this.state = {data: [],
            activeIndex: 0,
            COLORS : ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']
        };
        console.log(props);
    }

    async componentDidMount (){
        this.setState({data: []});
        for (let key in this.props.data){
            await this.setState({
                data : [...this.state.data, {'name': key, 'value': this.props.data[key][this.props.element]}]
            })
        }
    }
    
    onPieEnter = (data, index) => {
        this.setState({
            activeIndex: index,
        });
    };
    
    render() {
        return (
        <PieChart width={400} height={400}>
            <Pie
            activeIndex={this.state.activeIndex}
            activeShape={renderActiveShape}
            data={this.state.data}
            cx={200}
            cy={200}
            innerRadius={25}
            outerRadius={90}
            fill="#8884d8"
            dataKey="value"
            onMouseEnter={this.onPieEnter}
            >
                {
                    this.state.data.map((entry, index) => <Cell fill={this.state.COLORS[index % this.state.COLORS.length]}/>)
                }
            </Pie>
        </PieChart>
        );
    }
}

// import React, { useEffect, useState } from 'react';
// import {
//   PieChart, Pie, Cell,
// } from 'recharts';

// class pieChart = (props) => {
    
//     const [data, setData] = useState([]);

//     useEffect(() => {
//         // var df = [];
//         Object.keys(props.data).map((key) => {
//             setData(data.concat({'name': key, 'value': props.data.key[props.element]}));
//         })
//     //     for (let key in props.data){
//     //         let item = ;
//     //         setData(data.concat(item));
//     //     }
//     });

//     return (
//         <PieChart width={400} height={400}>
//             <Pie
//             data={data}
//             cx={200}
//             cy={200}
//             labelLine={false}
//             outerRadius={80}
//             fill="#8884d8"
//             dataKey="value"
//             >
//             {
//                 data.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
//             }
//             </Pie>
//         </PieChart>
//     );
// }

// export default pieChart;