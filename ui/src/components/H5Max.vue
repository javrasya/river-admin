<template>
  <h5 v-if="value.length<=max">{{value}}</h5>
  <v-tooltip v-else top>
    <template v-slot:activator="{ on }">
      <h5 v-on="on">{{value.substring(0, max) + '...'}}</h5>
    </template>
    <span>{{ value }}</span>
  </v-tooltip>
</template>


<script>
export default {
  name: "H5Max",
  props: ["value", "max"]
};
</script>