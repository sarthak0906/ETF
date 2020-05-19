import React from 'react'
import PropTypes from 'prop-types'
import moment from 'moment'

import {
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  LineChart, 
  Line
} from 'recharts'



const TimeSeriesChart = ({ chartData }) => (

  <LineChart
    data={chartData}>
    <XAxis
      dataKey='Time'
      scale='time'
      type='number'
      
    />
    <YAxis/>
    <Line type='linear'
      dataKey={"Close"}
    />
</LineChart>

)

TimeSeriesChart.propTypes = {
  chartData: PropTypes.arrayOf(
    PropTypes.shape({
      Time: PropTypes.number,
      Close: PropTypes.number
    })
  ).isRequired
}

export default TimeSeriesChart