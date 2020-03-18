<template>
  <div id="total-quiz">
      <h3>{{ title }}</h3>
      <span class="value" v-if="valueNumber">{{ number }}<slot></slot></span>
      <span class="value" v-else>{{ valueString }}</span>
  </div>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            required: true
        },
        valueNumber: {
            type: Number,
            required: false
        },
        valueString: {
            type: String,
            required: false
        }
    },
    computed: {
        totalQ() {
            return this.value
        },
        number(){
            return Math.floor(this.valueNumber)
        }
    },
}
</script>

<style>

#total-quiz h3 {
    margin: 1rem 0;
}

#total-quiz .value {
    font-size: 3.5rem;
}

#total-quiz {
    display: flex;
    color: rgb(85, 85, 85);
    /* color: #fff; */
    /* background: rgb(95, 241, 81); */
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 150px;
    margin: 0.5rem 1rem;
    padding: 0 1rem;
    border: 2px solid rgb(231, 231, 231);
    border-radius: 0.5rem;
}
</style>