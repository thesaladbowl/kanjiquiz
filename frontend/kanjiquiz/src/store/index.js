import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || "",
    refresh: '',
    teacher: '',
    class: '',
    userId: '',
    teacherHomeData: [],
  },
  mutations: {
    auth_request(state){
      state.status = 'loading'
    },
    auth_success(state, payload){
      state.status = 'success'  
      state.token = payload.token
      state.refresh = payload.refresh
      state.teacher = payload.user
      state.class = payload.classId
      state.userId = payload.userId
    },
    auth_error(state){
      state.status = 'error'
    },
    logout(state){
      state.status = '',
      state.token = '',
      state.classId = ''
    },
    teacherHomeData(state, payload){
      state.teacherHomeData = payload.studentData
    },
    REFRESH(state, refresh_token){
      state.token = refresh_token
    }
  },
  actions: {
    login({commit}, user){
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({url: 'https://kanjiquiz.herokuapp.com/login', data: user, method: 'POST'})
        .then(response => {
            const token = response.data.access_token
            const refresh = response.data.refresh_token
            const user = response.data.user
            const classId = response.data.class_id
            const userId = response.data.id
            localStorage.setItem('token', token)
            commit('auth_success', {
              userId,
              token,
              user,
              classId,
              refresh
            })
            resolve(response)
        }).catch(() => {
          reject("Invalid username/password")
        })
      })
    },
    logout({commit}){
      return new Promise((resolve) => {
        commit('logout')
        localStorage.removeItem('token')
        resolve()
      })
    },
    teacherHomeData({commit}){
      return new Promise((resolve) => {
        axios({url: `https://kanjiquiz.herokuapp.com/student_list/${this.getters.classId}`, method: 'GET'})
        .then(response => {
          commit('teacherHomeData', {
            studentData: response.data
          })
          resolve()
        })
      })
    },
    refresh({commit}, refresh_token){
      commit('REFRESH', refresh_token)
    }
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    isTeacher: state => state.teacher,
    userId: state => state.userId,
    token: state => state.token,
    classId: state => state.class,
    teacherHomeData: state => state.teacherHomeData,
    totalQuizNumber: state => {
      let totalNumber = 0;
      state.teacherHomeData.forEach(e => {
        totalNumber += e.quizes.length
      })
      return totalNumber
    },
    
  },
  modules: {}
});
