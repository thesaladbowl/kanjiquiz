<template>
  <div id="app">
    <router-view />
  </div>

</template>
<script>

export default {
  name: "app",
};
</script>

<style>

@import url('https://fonts.googleapis.com/css?family=Noto+Serif+JP|Gelasio|Roboto&display=swap');

html {
  	box-sizing: border-box;
    font-family: 'Roboto', sans-serif;
}

*,
*:before,
*:after {
	box-sizing: inherit;
}

body {
	margin: 0;
	padding: 0;
	border: 0;
}

a {
  text-decoration: none;
  color: black;
}

a:visited {
  color: black;
}

mt-1 { margin-top: 5rem;}

.container {
    max-width: 1100px;
    margin: 0 auto;
}

.logo-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Gelasio', serif;
    font-size: 2.5rem;
    margin-top: 0;
    margin-bottom: 2rem;
}

.logo-kanji {
    font-family: 'Noto Serif JP', serif;
    color: #fff;
    background: rgb(218, 31, 31);
    padding: 0.25rem;
    margin-right: 0.5rem;
    border-radius: 20%;
}

.btn {
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 10%;
    cursor: pointer;
    background: rgb(218, 31, 31);
    color: white;
    margin-top: 2rem;
    margin-bottom: 2rem;
}

text-center { text-align: center;}

</style>
