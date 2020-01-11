<template>
 <div>
    <router-link
    :to="{ name: 'quiz-create'}"
    >Create Quiz
    </router-link>
     <div v-for="student in students" :key="student.id">
         <p>{{ student.first_name }}
            <router-link 
                :to="{ name: 'student', params: { student_id: student.id }}"
                >See Quizes
            </router-link>
         </p> 
     </div>

 </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "TeacherHome",
    data() {
        return {
            students: [],
        }
    },
    methods: {
        // 
    },
    created(){
        axios.get('http://127.0.0.1:5000/students', {
            headers: {
                'Access-Control-Allow-Origin': '*',
            }
        })
        .then(response => {
            this.students = response.data
        })
    }
}
</script>

<style>

</style>

