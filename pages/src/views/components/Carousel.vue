<template>
  <section class="section section-lg section-shaped overflow-hidden my-0">
    <div class="shape shape-style-1 shape-default shape-skew">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="container py-0 pb-lg">
      <div class="row justify-content-between align-items-center">
        <div class="col-lg-4 mb-4 mb-lg-0">
          <h1 class="text-white font-weight-light">Modern Design</h1>
          <p class="lead text-white mt-4">
            River Admin powerful design is built with
            Vue & Vuetify
          </p>
        </div>
        <div class="col-lg-8 mb-lg-auto">
          <div class="rounded shadow-lg overflow-hidden transform-perspective-right">
            <b-carousel id="carousel1" controls indicators>
              <!-- Text slides with image -->
              <b-carousel-slide img-src="img/theme/home.png"></b-carousel-slide>
              <b-carousel-slide img-src="img/theme/reprio.png"></b-carousel-slide>
              <b-carousel-slide img-src="img/theme/timeline.png"></b-carousel-slide>
            </b-carousel>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
import { BCarousel } from "bootstrap-vue/esm/components/carousel/carousel";
import { BCarouselSlide } from "bootstrap-vue/esm/components/carousel/carousel-slide";

export default {
  components: {
    BCarousel,
    BCarouselSlide
  }
};
</script>
<style>
</style>
