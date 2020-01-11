<template>
  <div id="app">
     <span v-if="isLoggedIn">
         <a @click="logout">Logout</a>
     </span>
    <router-view />
    
  </div>
</template>

<script>

export default {
  name: "app",
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

};
</script>

<style>
</style>
