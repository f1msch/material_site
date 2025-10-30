<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" to="/">素材网站</router-link>
        <div class="navbar-nav">
          <router-link class="nav-link" to="/">首页</router-link>
          <router-link class="nav-link" to="/materials">素材库</router-link>
        </div>
      </div>
    </nav>
    <main class="container mt-4">
      <router-view/>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>