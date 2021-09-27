import React from 'react';
import './App.css';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom'
import Occupancy from './Components/Occupancy';
// import HeaderComponent from './Components/HeaderComponent';
// import FooterComponent from './Components/FooterComponent';

function App() {
  return (
    <div>
        <Router>
              {/* <HeaderComponent /> */}
                <div className="container">
                    <Switch> 
                          <Route path = "/api/occupancy" exact component = {Occupancy}></Route>
                    </Switch>
                </div>
              {/* <FooterComponent /> */}
        </Router>
    </div>
    
  );
}

export default App;

