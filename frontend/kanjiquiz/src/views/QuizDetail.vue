<template>
  <div>
      <Navbar />

        <div id="quiz-question" class="container">
                <div class="detail-flex card" v-for="quiz in quizDetail" :key="quiz.id">
                    <h1>{{quiz.quiz}}</h1>
                    <p class="kanji">{{quiz.kanji}}</p>
                    <p class="sentence"><strong>Sentence:</strong>{{quiz.sentence}}</p>
                    <div class="sentence-correct" v-if="quiz.question_correct">&#10004;</div>
                    <div class="sentence-incorrect" v-else>&#10006;</div>

                    <form @submit.prevent="addCorrection">
                    <input
                        type="text" 
                        placeholder="Write correct sentence" 
                        v-show="active" 
                        v-model="correction" 
                        />
                    </form>
                    <form @submit.prevent="addStudentSentence(); StudentSaveChanges()" class="student-sentence-form">
                        <input type="text"
                        placeholder="Write your sentence!"
                        v-model="studentSentence"
                        v-if="!isTeacher"
                        />
                    </form>
                    <p class="correct-sentence" v-if="quiz.corrected_sentence"><strong>Corrected sentence:</strong> {{ quiz.corrected_sentence }}</p>
                    <div class="button-container" v-if="isTeacher">
                        <button class="btn correction" @click="active = !active">Make Correction</button>
                        <button class="btn mark-correct" v-if="!quiz.question_correct" @click="quiz.question_correct = true">Mark Correct</button>
                        <button class="btn mark-incorrect" v-else @click="quiz.question_correct = false">Mark Incorrect</button>                        
                    </div>
                    <form @submit.prevent="saveChanges" v-if="isTeacher">
                        <input class="btn" type="submit" value="Submit">
                    </form>
          </div>  
            <div class="message-wrapper">
                <MessageSnack :success="success" :error="error">
                  <template v-slot:success>{{ successMessage }}</template>
                  <template v-slot:error>{{ errorMessage }}</template>
              </MessageSnack> 
            </div>
            <div class="comment-wrapper">
                <div class="comment-container card">
                        <div class="question_respond">
                        <h2>
                            Questions
                        </h2>
                        <div class="comment" v-for="comment in commentList" :key="comment.id">
                            {{comment.comment }}
                        </div>
                        </div>
                </div>
                <div class="comment-form card">
                    <p><strong>Reply to {{name}}</strong></p>
                    <form @submit.prevent="addComment">
                        <textarea cols="30" rows="10" v-model="comment" required></textarea>
                        <input class="btn" type="submit" value="Submit">
                    </form>
                </div>
            </div>
        </div>
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue'
import MessageSnack from '@/components/MessageSnack.vue'
import apiservice, { fetchApiService } from '../../services/apiservice.js'

export default {
    name: "quiz",
    components: {
        Navbar,
        MessageSnack
    },
    data () {
        return {
            quizDetail: [],
            active: false,
            correction: "",
            success: false,
            error: false,
            successMessage: '',
            errorMessage: '',
            isTeacher: this.$store.getters.isTeacher,
            comments: [],
            comment: '',
            studentSentence: '',
            name: this.$route.params.name
        }
    },
    computed: {
        commentList(){
            return this.comments
        }
    },
    methods: {
        getQuizDetail(){
        apiservice.getApiService(`/quiz/${this.$route.params.quiz_id}`)
        .then(response => {
            this.quizDetail.push(response.data);
        })
        },
        getComments(){
            apiservice.getApiService(`/comment/${this.$route.params.quiz_id}`)
            .then(response => {
                this.comments = response.data
            })
        },
        addCorrection(){
            this.quizDetail[0].corrected_sentence = this.correction;
            this.active = false;
        },
        addStudentSentence(){
            this.quizDetail[0].sentence = this.studentSentence;
        },
        addComment(){
            const data = {
                'comment': this.comment,
                'user_id': this.$route.params.user_id ? this.$route.params.user_id : this.$route.params.student_id,
                'quiz_id': this.$route.params.quiz_id
            }

            fetchApiService(`/comment/create`, 'POST', data)
            .then((response) => {
                if(response.success){
                    this.comments.push(this.comment)
                    this.comment = ''
                    this.getComments()
                    this.error = false
                    this.success = true
                    this.successMessage = "You added a comment!"
                } else {
                    this.success = false
                    this.error = true
                    this.errorMessage = "An error has occured"
                }
            })
        },
        saveChanges(){
            const data =  {
                'sentence': this.quizDetail[0].sentence,
                'corrected_sentence': this.correction,
                'question_correct': this.quizDetail[0].question_correct,
               }
            fetchApiService(`/quiz/${this.$route.params.quiz_id}`, 'PUT', data)
            .then((response) => {
                if(response.success){
                    this.error = false
                    this.success = true
                    this.successMessage = "Updated!"
                } else {
                    this.success = false
                    this.error = true
                    this.errorMessage = 'Error updating'
                }
            })
        },
        StudentSaveChanges(){
            const data = {
                'sentence': this.studentSentence,
                'question_correct': this.quizDetail[0].question_correct,
            }
            fetchApiService(`/quiz/${this.$route.params.quiz_id}`, 'PUT', data)
            .then(response => {
                if(response.success){
                    this.error = false
                    this.success = true
                    this.successMessage = "You added your sentence!"
                } else {
                    this.success = false
                    this.error = true
                    this.errorMessage = "Error Updating"
                }
            })
        }
    },
    created(){
        this.getQuizDetail()
        this.getComments()
    }
}
</script>

<style>

#quiz-question .container {
        max-width: 1100px;
        margin: 0 auto;
    }

#quiz-question .sentence {
        position: relative;
    }

#quiz-question .detail-flex {
    display: flex;
    flex-direction: column;
    align-items: center;
}

#quiz-question .card {
    padding: 1rem;
    box-shadow: 1px 1px 5px rgb(172, 172, 172);
    margin-top: 2rem;
}

#quiz-question .btn {
    border-radius: 0;
    margin: 0;
}

#quiz-question .kanji {
    font-size: 80px;
    margin: 0;
}

#quiz-question .correction {
    color: rgb(0, 129, 0);
    background: #fff;
    border: 1px solid rgb(0, 129, 0);
    margin: 1rem 1rem;
}

#quiz-question .mark-incorrect {
    color: rgb(211, 0, 0);
    background: #fff;
    border: 1px solid rgb(211, 0, 0);
    margin: 1rem 1rem;
}

#quiz-question .mark-correct {
    color: rgb(0, 129, 0);
    background: #fff;
    border: 1px solid rgb(0, 129, 0);
    margin: 1rem 1rem;
}

#quiz-question .mark-correct, .mark-incorrect:focus {
    outline: none;
}


#quiz-question .correction:focus {
    outline: none;
}

#quiz-question .correction:hover {
    color: #fff;
    background: rgb(0, 129, 0);
}

#quiz-question .sentence-correct {
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  height: 30px;
  width: 30px;
  background-color: rgb(15, 182, 0);
  border-radius: 50%;
  margin: 0.5rem 0;
}

#quiz-question .sentence-incorrect {
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  height: 30px;
  width: 30px;
  background-color: rgb(219, 0, 0);
  border-radius: 50%;
  margin: 0.5rem 0;

}

#quiz-question .comment-container {
  display: flex;
  margin: 2rem 0;
  margin-right: 1rem;
  flex: 2;
}

#quiz-question .comment {
    border: 1px solid rgb(146, 146, 146);
    border-radius: 10px;
    padding: 0.5rem 1rem;
    margin: 1rem 1rem;
}

#quiz-question .comment-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 2rem 0;
}

#quiz-question .comment-form input {
    display: block;
    margin: 1rem auto;
}

#quiz-question .comment-wrapper {
    display:flex;
    justify-content: space-between;
}

#quiz-question .student-sentence-form {
    margin: 0.5rem 1rem;
}

#quiz-question .student-sentence-form input[type=text] {
    padding: 0.25rem 0.5rem;
}

@media (max-width: 800px) {
    #quiz-question .comment-wrapper {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }
    #quiz-question .comment-container {
        width: 100%;
        margin: 0;
    }
    #quiz-question .comment-form {
        width: 100%;
    }
}


</style>


