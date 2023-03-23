<template>
  <div>
    <h1>We are at HelloWorld.vue</h1>
    <p>Todo id: {{ itemId }}</p>
    <button @click="itemId++">Fetch next item</button>
    <p v-if="!msg">Loading...</p>
    <pre v-else>{{ msg }}</pre>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      itemId: 1,
      msg: null,
    };
  },
  methods: {
    getItem() {
      axios.get(`items/${this.itemId}`)
          .then((res) => {
            this.msg = res.data;
            console.log(res.data)
            console.log(res)
          })
          .catch((error) => {
            console.error(error)
          });
    },
  },
  mounted() {
    this.getItem()
  },
  watch: {
    itemId() {
      this.getItem()
    }
  },
};
</script>
