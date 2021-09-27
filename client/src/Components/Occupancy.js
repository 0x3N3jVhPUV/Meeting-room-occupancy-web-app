import React, { Component } from 'react'
import Select from 'react-select'
import occupancyService from '../Services/occupancyServices'

class Occupancy extends Component {

  constructor(props){
    super(props)
    this.state = {
      selectSensor : [],
      selectTs : [],
      sensor: "",
      ts: '',
      inside: ''
    }
  }

 async getSensors(){
    // const res = await axios.get('https://jsonplaceholder.typicode.com/users')
    const res = await occupancyService.getOccupancy()
    const data = res.data
    console.log("data : ", data)
    const options = data.map(d => ({
      "sensor" : d.sensor
    }))
    this.setState({selectSensor: options})
  }

  handleChange(e){
   this.setState({id:e.value, name:e.label})
  }

  componentDidMount(){
      this.getSensors()
    //   this.getTs()
  }

  render() {
    console.log(this.state.selectSensor)
    return (
      <div>
        <Select options={this.state.selectSensor} onChange={this.handleChange.bind(this)} />
    <p>You have selected <strong>{this.state.sensor}</strong></p>
      </div>
    )
  }
}

export default Occupancy