<template>
 <div id="main">
    <Navbar />
    <div class="container">
        <div class="grid-container">
            <div class="announcements card">
                <h3>Welcome to Kanji Quiz!</h3>
                <p>This is a demonstration site for an e-learning quiz app.</p>
                <p>Teachers can create quizes, find useful stats on their students' progress, suggest corrections, and directly answer questions that a student may have.</p>
                <p>To get started, create a quiz above or take a look at some of the sample students on the left!</p>
            </div>
            <div class="stats card">
                <PieChart 
                v-if="loaded"
                :chartdata="chartdata"
                :options="options"
                />
                <div class="stats-container">
                    <StatsBox 
                    :title="totalQuizTitle"
                    :valueNumber="getTotalNumber"
                    />
                    <StatsBox 
                    :title="easiestQuizTitle"
                    :valueString="easiestKanji"
                    />
                    <StatsBox 
                    :title="difficultQuizTitle"
                    :valueString="hardestKanji"
                    />
                </div>
            </div>
                <div class="student-list card">
                    <h3>Student List</h3>
                    <div class="student-item" v-for="student in studentList" :key="student.id">
                        <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" class="avatar">
                            <router-link 
                                class="student-quiz"
                                :to="{ name: 'student', params: { student_id: student.id }}"
                                > {{ truncateName(student.full_name) }}
                            </router-link>
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
import PieChart from '../components/PieChart.vue'
import StatsBox from '../components/StatsBox.vue'
import apiservice from '../../services/apiservice.js'

export default {
    name: "TeacherHome",
    components: {
        Navbar,
        Footer,
        PieChart,
        StatsBox
    },
    data() {
        return {
            loaded: false,
            chartdata: {
                labels: ['Correct', 'Incorrect'],
                datasets: [{
                    label: 'Correct',
                    backgroundColor: [
                        '#21de67',
                        '#ff525a'
                    ],
                    data: []
                },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
          },
          totalQuizTitle: "Total number of Quizes:",
          easiestQuizTitle: "Easiest Kanji: ",
          difficultQuizTitle: "Most Difficult Kanji: ",
          easiestKanji: "",
          hardestKanji: "",

        }
    },
    computed: {
        studentList(){
            return this.$store.getters.teacherHomeData
        },
        getTotalNumber(){
            return this.$store.getters.totalQuizNumber
        },
    },
    methods: {
        setChartData(){
            apiservice.getApiService(`/stats/${this.$store.getters.classId}/qcorrect`)
            .then(response => {
                this.chartdata.datasets[0].data.push(response.data["correct"])
                this.chartdata.datasets[0].data.push(response.data["incorrect"])
                this.loaded = true
            })
        },
        truncateName(name){
            if(name.length > 15){
                const trunName = name.slice(0,15) + '...'
                return trunName
            } else {
                return name
            }
        },
        getEasyHardKanji(){
            let arr = []
            let correct_obj = {}
            let incorrect_obj = {}

            apiservice.getApiService(`/student_list/${this.$store.getters.classId}`)
            .then(response => {
                response.data.forEach(e => {
                    arr.push(...e.quizes)
                })
            })
            .then(() => {
                arr.forEach(e => {
                    if(e.question_correct){
                        correct_obj[e.quiz] = (correct_obj[e.quiz] || 0) + 1
                    } else {
                        incorrect_obj[e.quiz] = (incorrect_obj[e.quiz] || 0) + 1
                    }
                })                
            })
            .then(() => {
                const highestCorrectQuiz = Object.keys(correct_obj).reduce((a,b) => correct_obj[a] > correct_obj[b] ? a : b)
                const highestCorrectKanji = arr.filter(q => q.quiz === highestCorrectQuiz)[0].kanji


                const highestIncorrectQuiz = Object.keys(incorrect_obj).reduce((a,b) => incorrect_obj[a] > incorrect_obj[b] ? a : b)
                const highestIncorrectKanji = arr.filter(q => q.quiz === highestIncorrectQuiz)[0].kanji
                
                this.hardestKanji = highestIncorrectKanji
                this.easiestKanji = highestCorrectKanji
            })
        }
    },
    mounted(){
        this.$store.dispatch('teacherHomeData')
        this.setChartData()
        this.getEasyHardKanji()
    }
}
</script>

<style>

#main canvas {
    width: 100px;
}

#main .grid-container {
    display: grid;
    grid-gap: 1rem;
    grid-template-areas: 
        'student student announce'
        'student student stats'
        'footer footer footer';
}

#main .container {
    max-width: 1100px;
    margin: 2rem auto;
    height: 100vh;
}

#main .announcements {
    grid-area: announce;
}

#main .card {
    padding: 1rem;
    box-shadow: 1px 1px 5px rgb(172, 172, 172);
}

#main .student-list {
    grid-area: student;
    text-align: center;
}
#main .student-item {
    display: flex;
    width: 250px;
    /* justify-content: center; */
    align-items: center;
}

#main .student-item .avatar {
  vertical-align: middle;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin: 0.5rem 0;
}

#main .student-item .student-quiz {
    margin: 1rem 1.5rem;
}

#main .student-item:hover {
    background: rgb(248, 248, 248);
}

#main .stats {
    grid-area: stats;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

#main .btn {
    color: rgb(218, 31, 31);
    border-radius: 0;
    border: 1px solid rgb(218, 31, 31);
    background: #fff;
}

#main .btn:hover {
    background: rgb(218, 31, 31);
    color: #fff;
}



@media (max-width: 800px) {
    #main .grid-container {
            grid-template-areas: 
        'announce'
        'student'
        'stats'
        'footer';
    }

    #main .student-list {
    display: flex;
    grid-area: student;
    text-align: center;
    overflow: scroll;
    }

    #main .student-list h3 {
        display: none;
    }

    #main .stats {
    flex-wrap: wrap;
    justify-content:center;
    }

    #main .stats > div {
        width: auto;
    }

    #main #footer {
        display: none;
    }
}
</style>

