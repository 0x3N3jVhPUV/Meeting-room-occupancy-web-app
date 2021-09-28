import React, { Component } from 'react'
import Select from 'react-select'
import occupancyService from '../Services/occupancyServices'
import "bootstrap/dist/css/bootstrap.min.css";

class Occupancy extends Component {

  constructor(props){
    super(props)
    this.state = this.getInitialState();
    this.sensorHandleChange = this.sensorHandleChange.bind(this);
    this.TsHandleChange = this.TsHandleChange.bind(this);
    this.submit = this.submit.bind(this);
    this.onClear = this.onClear.bind(this);
  }

 async getSensors(){
    const self = this;
    const res = await occupancyService.getOccupancy()
    if (res.data[0].length > 0){
      const data = res.data[0]
      const options = data.map(d => ({
        "label" : d.sensor,
      }))
      this.setState({sensorOptions: options})
    }else{
      const state = self.getInitialState();
      self.setState(state);
    }
  }

  async getTs(){
    const self = this;
    const res = await occupancyService.getOccupancy()
    if (res.data[1].length > 0){
      const data = res.data[1]
      const options = data.map(d => ({
        "label" : d.Ts,
      }))
      this.setState({tsOptions: options})
    }else{
      const state = self.getInitialState();
      self.setState(state);
    }  
  }

  getInitialState() {
    return {
      sensor: '',
      ts: '',
      inside: '',
      isChecked: false,
      noSensor: false
    }
  }

  sensorHandleChange(e){
    this.setState({sensor:e.label})
   }
  TsHandleChange(e){
    this.setState({ts:e.label})
   }

  componentDidMount(){
      this.getSensors()
      this.getTs()
  }

  async submit(e) {
    e.preventDefault();
    this.setState({ 'isChecked': true });

    const lenSensor = this.state.sensor.length
    const lenTs = this.state.ts.length
    const self = this;
    if(lenSensor> 0 & lenTs>0 ){
     await occupancyService.getOccupancyBySensorAndTs(this.state.sensor, this.state.ts).then(res =>{
          const data = res.data[2];
          self.setState({ inside: data })
        }).catch(function (error) {
          console.log(error);
          self.setState({
            'no sensor': true
          });
        });            
    }else if (lenSensor>0){
      await occupancyService.getOccupancyBySensor(this.state.sensor).then(res =>{
        const data = res.data[2];
        self.setState({ inside: data });
      }).catch(function (error) {
        console.log(error);
      });
    } else {
      self.setState({isChecked: true})
    }
  } 

  onClear(){
    const state = this.getInitialState();
    this.setState(state);
  }

  result(){
    if(!this.state.inside.inside){
      return
    }
    if(this.state.inside.inside & this.state.sensor.length>0 & this.state.ts.length>0){
      console.log(this.state.inside.inside , this.state.sensor)
      return(
        <div className="alert alert-success" role="alert">
          <h1>On <b>{this.state.ts}</b> sensor <b>{this.state.sensor}</b> reported a room occupancy of <b>{this.state.inside.inside}</b> people.</h1>
        </div>  
      )
    }
    if(this.state.inside.inside){
      return(
        <div className="alert alert-success" role="alert">
          <h1> Sensor <b>{this.state.sensor}</b> reports room occupancy of <b>{this.state.inside.inside}</b> people.</h1>
        </div>  
      )
    }
    if(!this.state.inside.inside & this.state.sensor.length>0 & this.state.ts.length>0){
      return(
        <div className="alert alert-warning" role="alert">
          <h1>There are no data at <b>{this.state.ts}</b> for sensor <b>{this.state.sensor}</b>.</h1>
        </div>  
      )
    }
  }

  render() {
    let result = this.result();
    return (
      <div>
        <div className = "container">
          <div className = "row">
              <div className = "card col-md-6 offset-md-3 offset-md-3"></div>
                <h2 className="text-center">Meeting room occupancy web app</h2>
                <br></br>
                <div className = "card-body">
                  <p>Select a sensor:</p>
                  <Select options={this.state.sensorOptions} onChange={this.sensorHandleChange.bind(this)} />
                  <p>Select a date:</p>
                  <Select options={this.state.tsOptions} onChange={this.TsHandleChange.bind(this)} />
                  <br></br>     
                    <button type="submit" className="btn btn-success" onClick={this.submit}>Show occupancy</button>
                    <button type="submit" className="btn btn-outline-secondary" onClick={this.onClear}>Clear</button>
                  <br></br>
                  <br></br>
                    {result}
                  </div>
              </div>
            </div>  
      </div>
    )
  }
}

export default Occupancy