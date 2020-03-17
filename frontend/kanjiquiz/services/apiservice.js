import axios from 'axios'
import store from '../src/store'

const apiService = axios.create({
    baseURL: 'http://127.0.0.1:5000',
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
    return fetch(endpoint, config)
    .then(response => {
        if(response.ok){
            return {
                error: false,
                success: true
            }
        } else if(response.status === 401){
            fetch(`http://127.0.0.1:5000/refresh`, {
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