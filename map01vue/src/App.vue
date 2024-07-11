<template>
  <div id="app">
    <h1>Vue Test</h1>
    <router-link to="/">Map Page</router-link> .
    <router-link to="/test">Maptest Page</router-link> .
    <router-link to="/MapFunction">MapFunction</router-link>

    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
