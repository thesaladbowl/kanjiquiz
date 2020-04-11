import Vue from "vue";
import App from "./App.vue";
import store from "./store";
import Axios from 'axios';
import VueRouter from 'vue-router';
import TeacherHome from "./views/TeacherHome.vue";
import StudentHome from "./views/StudentHome.vue";
import Student from "./views/Student.vue"
import QuizDetail from "./views/QuizDetail.vue"
import QuizCreate from "./views/QuizCreate.vue"
import Login from "./views/Login.vue"
import Icon from 'vue-awesome/components/Icon'
import 'vue-awesome/icons'

const lStore = store


Vue.use(VueRouter);
Vue.component('v-icon', Icon)
Vue.prototype.$http = Axios;


const token = localStorage.getItem('token')
if(token){
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: "/teacher-home",
      name: "teacher-home",
      component: TeacherHome,
      meta: {
        requiresAuth: true,
        isTeacher: true
      }
    },
    {
      path: "/student-home",
      name: "student-home",
      component: StudentHome,
      meta: {
        requiresAuth: true,
      }
    },
    {
      path: "/student/:student_id",
      name: "student",
      props: true,
      component: Student,  
      meta: {
        requiresAuth: true,
        isTeacher: true
      }
    },
    {
      path: "/student/quiz/:quiz_id",
      name: "quiz",
      props: true,
      component: QuizDetail,
      meta: {
        requiresAuth: true,
        isTeacher: true
      },
    },
    {
      path: "/quiz-create",
      name: "quiz-create",
      component: QuizCreate,
      meta: {
        requiresAuth: true,
        isTeacher: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/student/quiz/:student_id/:quiz_id',
      name: "student-quiz",
      component: QuizDetail,
      // Need to route guard further: check if quiz.id matches user.id
      // Change models to include a student id along with the quiz and have his included
      beforeEnter: (to,from,next) => {
        if(to.params.student_id !== lStore.getters.userId){
          lStore.dispatch('logout')
          next({name: 'login'})
        } else {
          next()
        }
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if(to.matched.some(record => record.meta.isTeacher)){
      if (store.getters.isLoggedIn && store.getters.isTeacher) {
         next()
         return
       } 
       next('/login')
    } else next()
    if(!store.getters.isLoggedIn){
      next('/login')
    }
  } else {
    next() 
  }
})

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
