<template>
  <div id="quiz-create">
      <Navbar />
      <h1>Create Quiz</h1>
      <h1> {{ test }} </h1>
      <!-- Input and forms for creating a quiz -->
      <div class="container">
        <form class="form" @submit.prevent="submit">
            <input type="text" placeholder="Kanji" v-model="kanji" required>
            <input type="text" placeholder="Quiz name" v-model="quizName" required>
            <input type="text" placeholder="Class ID" v-model="quizID" required>
            <input class="btn" type="submit" value="Submit">
        </form>
        </div> 
           <MessageSnack :success="success" :error="error">
                <template v-slot:success>Quiz Created!</template>
                <template v-slot:error>Error creating quiz</template>
           </MessageSnack>
        </div>
</template>

<script>
import Navbar from '../components/Navbar.vue'
import MessageSnack from '@/components/MessageSnack.vue'
import { fetchApiService } from '../../services/apiservice.js'

export default {
    name: 'quiz-create',
    components: {
        Navbar,
        MessageSnack
    },
    data(){
        return {
            test: "",
            kanji: "",
            quizName: "",
            success: false,
            error: false,
            quizID: "",
        }
    },
    methods: {
        submit(){
            const data = {
                'kanji': this.kanji,
                'quiz_name': this.quizName,
                'sentence': "",
                'class_name': this.quizID
            }
            fetchApiService(`http://127.0.0.1:5000/quiz`, 'POST', data)
            .then(response => {
                    this.error = response.error
                    this.success = response.success
                }
            )
        }
    },
}
</script>

<style>

#quiz-create h1, h2{
    text-align: center;
    font-size: 800;
    /* margin: 1rem; */
}

#quiz-create .container {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    max-width: 1100px;
    margin: auto;
}

#quiz-create input {
    margin-top: 1rem;
    padding: 1rem;
    outline-style: auto;
    outline-color: rgb(99, 99, 99);
}

#quiz-create input:focus {
    outline-style: auto;
    outline-color: rgb(99, 99, 99);
    box-shadow: none;
    outline: solid rgb(228, 228, 228);;
}

#quiz-create .btn {
    padding: 0.75rem 0.5rem;
    border-radius: 0;
    outline: none;
}

#quiz-create .form {
    display: flex;
    flex-direction: column;
    border-radius: 30px;
}

</style>