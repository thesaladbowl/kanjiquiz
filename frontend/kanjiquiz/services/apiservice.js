import axios from 'axios'
import store from '../src/store'

const apiService = axios.create({
    baseURL: 'https://kanjiquiz.herokuapp.com/',
    // baseURL: 'http://127.0.0.1:5000/',
    headers: {
        Accept: 'application/json',
        'Content-type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authorization': store.getters.token ? 'Bearer ' + store.getters.token : undefined,
    }
})

const fetchApiService = function(endpoint, method, data){
    const config = {
        method: method || "GET",
        body: data !== undefined ? JSON.stringify(data) : null,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + store.getters.token
        },

    }

    const fullEndpoint = `https://kanjiquiz.herokuapp.com` + endpoint
    // const fullEndpoint = `http://127.0.0.1:5000` + endpoint

    return fetch(fullEndpoint, config)
    .then(response => {
        if(response.ok){
            return {
                error: false,
                success: true
            }
        } else if(response.status === 401){
            fetch(`https://kanjiquiz.herokuapp.com/refresh`, {
                method: 'POST',
                headers: {
                   'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + store.state.refresh
                }
            }).then(response => {
                response.json().then(refresh_token => {
                    store.dispatch('refresh', refresh_token.token)
                }).then(() => fetchApiService(endpoint, method, data))
            })
        } else {
            return {
                success: false,
                error: true
            }
        }
    })
    .catch(() => {
        return {
            success: false,
            error: true
        }
    })
}

export default {
    getApiService(url){
        return apiService.get(url)
    }
}

export { fetchApiService }