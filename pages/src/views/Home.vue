<template>
  <div>
    <hero></hero>
    <carousel></carousel>
  </div>
</template>
<script>
import Hero from "./components/Hero";
import Carousel from "./components/Carousel";

export default {
  name: "components",
  components: {
    Hero,
    Carousel
  }
};
</script>
