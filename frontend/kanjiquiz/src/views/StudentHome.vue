<template>
 <div id="student-main">
    <Navbar />
    <div class="container">
        <div class="grid-container">
            <div class="announcements card">
                <h3>Hi there, {{studentName}}</h3>
                <p>This is the student page of the KanjiQuiz Application</p>
                <p>A student can choose a quiz from the right and input an answer and can also view some statistics below the page</p>
                <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Minus cumque dignissimos reiciendis eveniet ipsam, omnis incidunt quam earum eius sit! Nulla amet, facilis doloremque perferendis cupiditate eligendi quod ipsa labore? Magnam magni dicta maiores nisi reprehenderit ipsum ea, quaerat nesciunt eum atque quidem expedita et cupiditate molestias obcaecati, provident perferendis mollitia culpa tenetur delectus beatae, labore illum. Consequuntur nobis culpa recusandae voluptatem reprehenderit, eum ipsum! Porro aut, qui recusandae similique quibusdam est beatae consectetur autem illo eum. Laborum harum minus voluptatem? Laudantium, ex facilis. Quo culpa eveniet molestias minima sed! Quas incidunt odit, quisquam possimus sapiente eius iste omnis nostrum!</p>

            </div>
            <div class="quiz-list card">
                <h2>My Quizes</h2>
                <div class="quiz-item" v-for="quiz in quizList" :key="quiz.id">
                    <router-link 
                        :to="{ name: 'student-quiz', params: { student_id: studentId , quiz_id: quiz.id }}"
                        > {{ quiz.quiz }}
                    </router-link>
                </div>
            </div>
            <div class="stats card">
                <h1>Your Stats</h1>
                <div class="stats-item-wrapper">
                    <StatsBox 
                    :title="`# of Quizes`"
                    :valueNumber = QuizTotal
                    />
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
   <Footer />
</div>
</template>

<script>
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import StatsBox from '../components/StatsBox.vue'
import apiservice from '../../services/apiservice.js'

export default {
    components: {
        Navbar,
        Footer,
        StatsBox
    },
    data(){
        return {
            quizList: [],
            perCorrect: 0,
            perIncorrect: 0,
            studentName: '',
            studentId: this.$store.getters.userId,
        }
    },
    computed: {
        QuizTotal(){
            return this.quizList.length
        },
        percentageCorrect(){
            return this.perCorrect / this.QuizTotal * 100 
        },
        percentageIncorrect(){
            return this.perIncorrect / this.QuizTotal * 100 
        },
    },
    methods: {
        getQuizes(){
            apiservice.getApiService(`/students/${this.$store.getters.userId}`)
            .then(response => {
                this.quizList = response.data.quizes
                this.studentName = response.data.full_name
            })
            .then(() => {
                let cortotal = 0;
                let incortotal = 0;

                this.quizList.forEach(e => {
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
        // getKanji(){
        //     axios.get('https://jisho.org/api/v1/search/words?keyword=house')
        //     .then(response => {
        //         console.log(response)
        //     })
        // },
    },

    created(){
        this.getQuizes()
    }
}
</script>

<style>

#student-main .grid-container {
    display: grid;
    grid-gap: 1rem;
    grid-template-areas: 
        'quiz announce announce'
        'quiz stats stats'
        'footer footer footer';
}

#student-main .announcements {
    grid-area: announce;
}

#student-main .card {
    margin-top: 1rem;
    padding: 1rem;
    box-shadow: 1px 1px 5px rgb(172, 172, 172);
}

#student-main .quiz-list {
    grid-area: quiz;
    display: flex;
    flex-direction: column;
    align-items: center;
}

#student-main .quiz-item {
    padding: 0.5rem 1rem;
    margin: 0.5rem 1rem;
    border: 1px solid rgb(168, 168, 168);
    border-radius: 1rem;
}

#student-main .stats {
    grid-area: stats;
    display: flex;
    flex-direction: column;
    align-items: center;
}

#student-main .stats-item-wrapper {
    display: flex;
    justify-content: space-around;
    width: 100%;
}

@media (max-width: 800px) {
    #student-main .grid-container {
            grid-template-areas: 
        'announce'
        'quiz'
        'stats'
        'footer';
    }

    #student-main .stats {
    flex-wrap: wrap;
    justify-content:center;
    }

    #student-main .quiz-list {
        display: flex;
        flex-direction: row;
        align-items: center;
        overflow: scroll;
    }
    #student-main .quiz-list h2 {
        display: none;
    }
    #student-main #footer {
        display: none;
    }
}

</style>
