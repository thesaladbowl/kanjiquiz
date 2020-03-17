<template>
  <div>
      <Navbar />
      <div id="student" class="container">
          <div class="message-wrapper">
                <MessageSnack :success="success" :error="error">
                  <template v-slot:success>Quiz Deleted!</template>
                  <template v-slot:error>Error deleting quiz</template>
              </MessageSnack>  
          </div>              
          <div class="student-grid">
                <h1 class="student-name"><img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" class="avatar">{{ studentInfo[0].full_name }}</h1>
                <table>
                    <thead>
                        <tr>
                            <th scope="col">Quiz Name</th>
                            <th scope="col">Date Created</th>
                            <th scope="col">Date Submitted</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody v-for="quiz in studentInfo[0].quizes" :key="quiz.id">
                        <tr>
                            <th scope="row">
                            <router-link 
                            :to="{ name: 'quiz', params: { quiz_id: quiz.id, name: studentInfo[0].full_name, user_id: studentInfo[0].id }}"
                            >{{ quiz.quiz }}
                            </router-link>
                            </th>
                            <td>{{ quiz.date_created }}</td>
                            <td>{{ quiz.date_submitted }}</td>
                            <td>
                                <button @click="deleteQuiz(quiz.id)">Delete</button>
                            </td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <th scope="row" colspan="2">Total # of quizes:</th>
                            <td colspan="2">{{ QuizTotal }}</td>
                        </tr>
                    </tfoot>
                </table>
                    <div class="card">
                        <StatsBox 
                        :title="`% Correct`"
                        :valueNumber = percentageCorrect
                        >%
                        </StatsBox>
                        <StatsBox 
                        :title="`% Incorrect`"
                        :valueNumber = percentageIncorrect
                        >%
                        </StatsBox>
                    </div>
             </div>
        </div>
      </div>
</template>

<script>
import axios from 'axios'
import StatsBox from '../components/StatsBox.vue'
import Navbar from '../components/Navbar.vue'
import MessageSnack from '@/components/MessageSnack.vue'
import { fetchApiService } from '../../services/apiservice.js'

export default {
    name: "student",
    components: { 
        Navbar,
        StatsBox,
        MessageSnack
    },
    data() {
        return {
            studentInfo: [],
            perCorrect: 0,
            perIncorrect: 0,
            success: false,
            error: false
        }
    },
    computed: {
        QuizTotal(){
            return this.studentInfo[0].quizes.length
        },
        percentageCorrect(){
            return this.perCorrect / this.QuizTotal * 100 
        },
        percentageIncorrect(){
            return this.perIncorrect / this.QuizTotal * 100 
        },
    },
    methods: {
        getStudentQuizes(){
            axios.get(`http://127.0.0.1:5000/students/${this.$route.params.student_id}`, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            })
            .then(response => {
                this.studentInfo.push(response.data)
            })
            .then(() => {
                let cortotal = 0;
                let incortotal = 0;

                this.studentInfo[0].quizes.forEach(e => {
                    if(e.question_correct){
                        cortotal ++
                    } else {
                        incortotal ++
                    }
                })
                this.perCorrect = cortotal;
                this.perIncorrect = incortotal;

            })
        },
        deleteQuiz(quiz_id){
            fetchApiService(`http://127.0.0.1:5000/quiz/delete/${quiz_id}`, 'DELETE')
            .then(response => {
                    this.error = response.error
                    this.success = response.success
                }
            )
        }
    },
    mounted (){
        this.getStudentQuizes()
    }
}
</script>

<style>

table {
  table-layout: fixed;
  width: 100%;
  border-collapse: collapse;
  box-shadow: 1px 1px 5px rgb(172, 172, 172); 
  margin-bottom: 5rem;
}

thead th:nth-child(1) {
  width: 30%;
}

thead th:nth-child(2) {
  width: 20%;
}

thead th:nth-child(3) {
  width: 15%;
}

thead th:nth-child(4) {
  width: 15%;
}

th, td {
  padding: 20px;
}

tbody td {
  text-align: center;
}

tbody th:hover {
    background: rgb(245, 245, 245);
    cursor: pointer;
}

tfoot th {
  text-align: right;
}

#student .avatar {
  vertical-align: middle;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin: 0.5rem 1rem; 
}

#student h1 {
    margin-top: 2rem;
    margin-bottom: 0;
}

#student .student-name {
    grid-column: 1 / span 3;
}

/* #student .content-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 1.5rem;
    margin-top: 2rem;
    margin-bottom: 2rem;
    box-shadow: 1px 1px 5px rgb(172, 172, 172); 
    width: 50%;
} */

#student .student-grid {
    display: grid;
    grid-gap: 2rem;
    grid-template-columns: 3fr 1fr;
}

/* #student .content-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
} */

#student button {
    display: block;
    background: none;
    border: none;
    font-weight: 600;
    color: rgb(238, 0, 0);
    cursor: pointer;
}

#student .card {
    padding: 2rem;
    box-shadow: 1px 1px 5px rgb(172, 172, 172);
}

#student .message-wrapper {
    margin-top: 1rem;
}

</style>