<template>
  <component :is="layout" id="app">
    <v-row align="center">
      <v-col>
        <router-view />
      </v-col>
    </v-row>

    <v-snackbar
      class="mt-10"
      v-model="show_snackbar"
      :color="snackbar_color"
      :top="true"
      :timeout="snackbar_timeout"
    >
      <v-icon color="white" left>{{ snackbar_icon }}</v-icon>
      <v-container>
        <v-row v-for="(snackbar_text,index) in snackbar_texts" v-bind:key="index">
          <v-col>{{ snackbar_text }}</v-col>
        </v-row>
      </v-container>
      <v-btn dark text @click="show_snackbar = false">Close</v-btn>
    </v-snackbar>
  </component>
</template>

<script>
import NotLoggedInLayout from "@/layouts/NotLoggedInLayout.vue";
import LoggedInLayout from "@/layouts/LoggedInLayout.vue";
import { on_logout, on_error, on_success } from "@/helpers/event_bus";
import { CAN_NOT_DELETE_DUE_TO_PROTECTION } from "@/helpers/errors";

const defaultLayout = "LoggedInLayout";

export default {
  name: "app",
  components: {
    LoggedInLayout,
    NotLoggedInLayout
  },
  computed: {
    layout() {
      return this.$route.meta.layout || defaultLayout;
    }
  },
  mounted() {
    var that = this;

    on_logout(() => {
      this.$store.commit("unSetAuthToken");
      this.$router.push({ name: "login" });
    });

    on_error((errors, timeout) => {
      if (timeout) {
        this.snackbar_timeout = timeout;
      } else {
        this.snackbar_timeout = this.default_snackbar_timeout;
      }
      that.error(errors);
    });

    on_success((message, timeout) => {
      if (timeout) {
        this.snackbar_timeout = timeout;
      } else {
        this.snackbar_timeout = this.default_snackbar_timeout;
      }
      that.success([message]);
    });
  },
  data: () => ({
    show_snackbar: false,
    snackbar_icon: null,
    snackbar_timeout: null,
    snackbar_color: "grey",
    snackbar_texts: null,
    default_snackbar_timeout: 4000
  }),
  methods: {
    success(messages) {
      this.snackbar_icon = "mdi-check-all";
      this.snackbar_texts = messages;
      this.snackbar_color = "success";
      this.show_snackbar = true;
    },

    error(messages) {
      this.snackbar_icon = "mdi-shield-half-full";
      this.snackbar_texts = messages;
      this.snackbar_color = "error";
      this.show_snackbar = true;
    },
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
