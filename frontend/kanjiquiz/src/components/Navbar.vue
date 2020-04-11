<template>
    <div id="navbar">
        <router-link 
        v-if="isTeacher"
        :to="{ name: 'teacher-home'}" >
            <h1 class="logo-header"><span class="logo-kanji">漢字</span> Quiz</h1>
        </router-link>
        <router-link 
        v-else
        :to="{ name: 'student-home'}" >
            <h1 class="logo-header"><span class="logo-kanji">漢字</span> Quiz</h1>
        </router-link>
        <div class="navbar-links">
             <router-link
                v-if="isTeacher"
                :to="{ name: 'quiz-create'}"
                class="btn"
                >Create Quiz
             </router-link>
          <span v-if="!isTeacher">
            <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" class="avatar">
          </span>
          <span class="logout" v-if="isLoggedIn">
            <a @click="logout">Logout</a>
          </span>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return {
            isTeacher: this.$store.state.teacher 
        }
    },
  computed: {
    isLoggedIn: function() { return this.$store.getters.isLoggedIn }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
      .then(() => {
        this.$router.push('/login')
      })
    }
  }
}
</script>

<style>

#navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    background: #f8f8f8;
}

#navbar h1 {
    font-size: 1.5rem;
    margin-bottom: 0;
    padding: 0.5rem;
}

#navbar .logout a {
  color: #fff
}

#navbar .logout {
    color: #fff;
    margin: 0 0.75rem;
    border: 1px solid rgb(83, 83, 83);
    background: rgb(83, 83, 83);
    padding: 0.5rem 1rem;
    border-radius: 10%;
    cursor: pointer;
}

#navbar .navbar-links .btn {
    color: rgb(218, 31, 31);
    border-radius: 0;
    border: 1px solid rgb(218, 31, 31);
    background: #fff;
    margin: 0 0.75rem;
    padding: 0.5rem 1rem;
}

#navbar .navbar-links .btn:hover {
    background: rgb(218, 31, 31);
    color: #fff;
}

#navbar .avatar {
  vertical-align: middle;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin: 0.5rem 1rem;
}
</style>