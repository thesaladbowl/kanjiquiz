<template>
  <footer id="footer">
      <div class="footer-container">
          <p>&copy; All Rights Reserved, Joseph Scutella 2020</p>
          <p class="portfolio-link">Check out my other projects</p>
      </div>
  </footer>
</template>

<script>
export default {

}
</script>

<style>
    #footer {
        background: rgb(77, 77, 77);
        color: #fff;
        grid-area: footer;
    }

    #footer .footer-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    #footer .footer-container .portfolio-link {
        border: 1px solid white;
        padding: 0.5rem 1rem;
    }

    #footer .footer-container .portfolio-link:hover {
        background: #fff;
        color: rgb(77, 77, 77);
        cursor: pointer;
        font-weight: 700;
    }
</style>