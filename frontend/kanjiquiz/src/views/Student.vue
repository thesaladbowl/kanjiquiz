<template>
  <div>
      <h1 v-if="message.length"> {{ message }}</h1>
      <h1>{{ studentInfo.first_name }}</h1>
      <div v-for="quiz in studentInfo.quizes" :key="quiz.id">
          {{ quiz.quiz }}
         <router-link 
            :to="{ name: 'quiz', params: { quiz_id: quiz.id }}"
            >View Quiz
         </router-link>
         <button @click="deleteQuiz(quiz.id)">Delete</button>
      </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "student",
    data() {
        return {
            studentInfo: [],
            message: ""
        }
    },
    methods: {
        getStudentQuizes(){
        axios.get(`http://127.0.0.1:5000/students/${this.$route.params.student_id}`, {
            headers: {
                'Access-Control-Allow-Origin': '*',
            }
        })
        .then(response => {
            this.studentInfo = response.data
        })
        },
        deleteQuiz(quiz_id){
            fetch(`http://127.0.0.1:5000/quiz/delete/${quiz_id}`, {
                method: 'DELETE',
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.$store.getters.token
                }
            }).then(response => {
                if(response.ok){
                    this.message = "Success!"
                }
            })
        }
    },
    created (){
        this.getStudentQuizes()
    }
}
</script>

<style>

</style>