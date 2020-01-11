<template>
  <div>
      <h1>Create Quiz</h1>
      <h1> {{ test }} </h1>
      <!-- Input and forms for creating a quiz -->
      <form @submit.prevent="submit">
          <input type="text" placeholder="kanji" v-model="kanji">
          <input type="text" placeholder="quiz name" v-model="quizName">
          <input type="text" placeholder="class ID" v-model="quizID">
          <input type="submit" value="submit">
      </form>
      <!-- Sentence, kanji, quiz name, class ID should be input  -->
  </div>
</template>

<script>
export default {
    name: 'quiz-create',
    data(){
        return {
            test: "",
            kanji: "",
            quizName: "",
            message: "",
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
            fetch(`http://127.0.0.1:5000/quiz`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.$store.getters.token
                },
                body: JSON.stringify(data)
            }).then(response => {
                if(response.ok){
                    this.message = "Quiz Created!"
                } else {
                    this.message = "Error creating quiz"
                }
            })
        }
    },
}
</script>

<style>

</style>