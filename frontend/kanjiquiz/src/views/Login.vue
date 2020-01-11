<template>
  <div>
      <form @submit.prevent="login">
          <h1>Sign in</h1>
          <label>Username</label>
          <input type="text" required v-model="username" placeholder="Username">
          <label>Password</label>
          <input type="password" required v-model="password" placeholder="Password">
          <hr>
          <button type="submit">Login</button>
      </form>
  </div>
</template>

<script>
export default {
    data(){
        return {
            username: "",
            password: "",
        }
    },
    methods: {
        login: function() {
            let username = this.username;
            let password = this.password;

            this.$store.dispatch('login', {username, password})
            .then(response => {
                if(response.data.user){
                    this.$router.push('/')
                } else {
                    this.$router.push('/student-home')
                }
            })
        }
    }
}
</script>

<style>

</style>