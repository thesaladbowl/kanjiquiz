<template>
  <div id="login">
        <div class="container">
            <form @submit.prevent="login" class="form">
                <h1 class="logo-header"><span class="logo-kanji">漢字</span> Quiz</h1>
                <h2 class="l-heading">Sign in</h2>
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" required v-model="username">
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" required v-model="password">
                </div>
                <input type="submit" class="btn" value="Login">
                <span class="error">{{ error }}</span>
            </form>
        </div>
      </div>
</template>

<script>
export default {
    data(){
        return {
            username: "",
            password: "",
            error: "",
        }
    },
    methods: {
        login: function() {
            let username = this.username;
            let password = this.password;

            this.$store.dispatch('login', {username, password})
            .then(response => {
                if(response.data.user){
                    this.$router.push('/teacher-home')
                } else {
                    this.$router.push('/student-home')
                }
            })
            .catch(err => {
                this.error = err
            })
        }
    },
    created(){
        this.error = "";
    }
}
</script>

<style>

#login {
    background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)),
    url('/img/background-1.jpg') no-repeat center center/cover; 
    height: 100vh;
}

#login input {
    margin: 0 auto;
    display: block;
    font-weight: bold;
    padding: 0.5rem;
    border-radius: 10px;
    border: none;
    outline: none;
}

#login input:focus {
    border-color: rgba(229, 103, 23, 0.8);
    box-shadow: 0 1px 1px rgba(229, 103, 23, 0.075) inset, 0 0 8px rgba(229, 103, 23, 0.6);
    outline: 0 none;
}

#login label {
    display: block;
    text-align: center;
    margin: 0.75rem;
}

#login h1, h2{
    text-align: center;
    font-size: 800;
    margin: 1rem;
}

#login .container {
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: 1100px;
    margin: auto;
    height: 100vh;
}

#login .error {
    margin-top: 50rem;
    color: red;
}

#login .form {
    border-radius: 30px;
    background: #f4f4f4;
    padding: 4rem;
    border: 1px solid rgb(83, 83, 83);
}

#login .form-group {
    margin: 0.75rem;
}

#login .btn {
    margin-top: 25px;
    padding: 0.75rem 1rem;
}


</style>