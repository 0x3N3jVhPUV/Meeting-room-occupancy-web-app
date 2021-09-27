import axios from 'axios';

const OCCUPANCY_API_BASE_URL = "http://127.0.0.1:5000/api/occupancy";

class occupancyService {

    getOccupancy(){
        return axios.get(OCCUPANCY_API_BASE_URL)
    }

    getOccupancyBySensor(sensor){
        return axios.get(OCCUPANCY_API_BASE_URL + '?sensor=' + sensor)
    }

    getOccupancyBySensorAndTs(sensor, atInstant){
        return axios.get(OCCUPANCY_API_BASE_URL + '?sensor=' + sensor + '&atInstant=' + atInstant)
    }

}

export default new occupancyService()