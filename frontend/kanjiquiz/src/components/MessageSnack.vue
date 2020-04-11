<template>
    <div class="message-container">
        <transition name="bounce">
            <div class="success-message" v-if="success"><slot name="success"></slot></div> 
        </transition>
        <transition name="shake">
            <div class="error-message" v-if="error"><slot name="error"></slot></div>    
        </transition>   
    </div>  
</template>

<script>
export default {
    props: {
        success: {
            type: Boolean,
            required: false
        },
        error: {
            type: Boolean,
            required: false
        }
    }
}
</script>

<style scoped>
.success-message {
    border-radius: 1rem;
    padding: 1rem 5rem;
    background: rgb(64, 192, 59);
    color: white;
    font-weight: 900;
    box-shadow: 2px 2px 8px #888888;
    margin-top: 1rem;
}

.error-message {
    border-radius: 1rem;
    padding: 1rem 5rem;
    background: rgb(192, 59, 59);
    color: white;
    font-weight: 900;
    box-shadow: 2px 2px 8px #888888;
    margin-top: 1rem;
}

.message-container {
    display: flex;
    justify-content: center;
}
.bounce-enter-active {
  animation: bounce-in .5s;
}
.bounce-leave-active {
  animation: bounce-in .5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.shake-enter-active {
    animation: shake .75s ease-in-out
}

@keyframes shake {
  from,
  to {
    -webkit-transform: translate3d(0, 0, 0);
    transform: translate3d(0, 0, 0);
  }

  10%,
  30%,
  50%,
  70%,
  90% {
    -webkit-transform: translate3d(-10px, 0, 0);
    transform: translate3d(-10px, 0, 0);
  }

  20%,
  40%,
  60%,
  80% {
    -webkit-transform: translate3d(10px, 0, 0);
    transform: translate3d(10px, 0, 0);
  }
}
</style>