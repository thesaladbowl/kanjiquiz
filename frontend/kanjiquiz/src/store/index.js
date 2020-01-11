import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || "",
    teacher: ''
  },
  mutations: {
    auth_request(state){
      state.status = 'loading'
    },
    auth_success(state, payload){
      state.status = 'success'
      state.token = payload.token
      state.teacher = payload.user
    },
    auth_error(state){
      state.status = 'error'
    },
    logout(state){
      state.status = '',
      state.token = ''
    }
  },
  actions: {
    login({commit}, user){
      return new Promise((resolve) => {
        commit('auth_request')
        axios({url: 'http://127.0.0.1:5000/login', data: user, method: 'POST'})
        .then(response => {
          const token = response.data.access_token
          const user = response.data.user
          localStorage.setItem('token', token)
          // axios.defaults.headers.common['Authorization'] = token
          commit('auth_success', {
            token: token,
            user: user
          })
          resolve(response)
        })
      })
    },
    logout({commit}){
      return new Promise((resolve) => {
        commit('logout')
        localStorage.removeItem('token')
        // delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    }
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    isTeacher: state => state.teacher,
    token: state => state.token
  },
  modules: {}
});
