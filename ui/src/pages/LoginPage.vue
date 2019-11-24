<template>
  <v-content>
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12" pa-5>
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title>River Admin</v-toolbar-title>
              <div class="flex-grow-1"></div>
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field
                  v-model="username"
                  label="Login"
                  name="login"
                  prepend-icon="mdi-account"
                  type="text"
                ></v-text-field>

                <v-text-field
                  v-model="password"
                  id="password"
                  label="Password"
                  name="password"
                  prepend-icon="mdi-lock"
                  type="password"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <div class="flex-grow-1"></div>
              <v-btn color="primary" @click="login">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import { auth, WORKFLOW } from "@/helpers/auth";
import { emit_error } from "@/helpers/event_bus";
import axios from "axios";
export default {
  props: {
    source: String
  },
  data: () => ({
    username: null,
    password: null
  }),
  methods: {
    login() {
      this.error_message = null;
      this.alert = false;
      axios
        .post("/api-token-auth/", { username: this.username, password: this.password })
        .then(response => {
          this.$store.commit("setAuthToken", response.data.token);
          auth.has_view_permission(WORKFLOW, yes => {
            if (yes) {
              if (this.$route.params.nextUrl) {
                this.$router.push({ path: this.$route.params.nextUrl });
              } else {
                this.$router.push({ name: "home" });
              }
            } else {
              this.$store.commit("unSetAuthToken");
              emit_error(["You has to have the permission to view the workflows!"], 10000);
            }
          });
        })
        .catch(err => {
          emit_error(["Authentication failed with given credentials!"], 10000);
        });
    }
  }
};
</script>