<template>
  <div>
      <div v-show="message">{{ message }}</div>
      {{ quizDetail }}
        <div id="quiz-question">
            <div class="container" v-for="quiz in quizDetail" :key="quiz.id">
                <h1>{{quiz.quiz}}</h1>
                <p>{{quiz.kanji}}</p>
                <button @click="active = !active">Make Correction</button>
                <p class="sentence">{{quiz.sentence}}</p>
                <form @submit.prevent="addCorrection">
                <input 
                    type="text" 
                    placeholder="Write correct sentence" 
                    v-show="active" 
                    v-model="correction" 
                    />
                </form>
                <p class="correct-sentence" v-if="quiz.corrected_sentence != null"> {{ quiz.corrected_sentence }}</p>
                <form @submit.prevent="saveChanges">
                    <input type="submit" value="Submit">
                </form>
            </div>
        </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "quiz",
    components: {
    },
    data () {
        return {
            quizDetail: [],
            active: false,
            correction: "",
            message: '',
            test: '',
        }
    },
    methods: {
        getQuizDetail(){
            axios.get(`http://127.0.0.1:5000/quiz/${this.$route.params.quiz_id}`, {
            headers: {
                'Access-Control-Allow-Origin': '*',
            }
        }).then(response => {
            this.quizDetail.push(response.data);
        })
        },
        addCorrection(){
            this.quizDetail[0].corrected_sentence = this.correction;
            this.active = false;
        },

        saveChanges(){
            const data =  {
                'sentence': this.quizDetail[0].sentence,
                'corrected_sentence': this.correction,
               }

            fetch(`http://127.0.0.1:5000/quiz/${this.$route.params.quiz_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.$store.getters.token
                },
                body: JSON.stringify(data)
            }).then((response) => {
                if(response.ok){
                    this.message = 'Updated!'
                } else {
                    this.message = 'Error updating'
                }
            })
        },
    },
    created(){
        this.getQuizDetail()
    }
}
</script>

<style>
    .container {
        max-width: 1100px;
        margin: 0 auto;
    }
    .sentence-color {
        color: red;
    }
    .tooltip {
        position: absolute;
        transform: translate(-40%, -40%);
        background: red; 
        display: none;
    }
    .sentence {
        position: relative;
    }

    .kanji-hover {
        color: blue;
    }
</style>

TODO: 

1. Be able to mark a sentence as correct, incorrect, or partial correct

// Make the option to have different kinds of quizes: Multiple choice, Write a sentence etc *advanced*
// 