<template>
  <v-card class="pa-5" :elevation="6">
    <v-card-title>New Hook</v-card-title>
    <v-card-text>
      <v-container fluid>
        <v-row>
          <v-col>
            <v-autocomplete
              v-model="selected_function"
              :items="functions"
              :loading="functions_loading"
              :search-input.sync="search_functions"
              hide-selected
              item-text="name"
              label="Search functions"
              clearable
              chips
              return-object
            >
              <template v-slot:no-data>
                <v-list-item>
                  <v-list-item-title>
                    Start typing to search for the
                    <strong>callback functions</strong>
                  </v-list-item-title>
                </v-list-item>
              </template>
              <template v-slot:selection="{ attr, on, item, selected }">
                <v-chip
                  v-bind="attr"
                  :input-value="selected"
                  color="primary"
                  class="white--text"
                  v-on="on"
                >
                  <v-icon left>mdi-function-variant</v-icon>
                  <span v-text="item.name"></span>
                </v-chip>
              </template>
              <template v-slot:item="{ item }">
                <v-list-item-content>
                  <v-list-item-title v-text="item.name"></v-list-item-title>
                </v-list-item-content>
              </template>
            </v-autocomplete>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
    <v-card-actions>
      <v-row>
        <v-col justify="center" align="right">
          <v-btn large color="primary" @click="createHook">Create Hook</v-btn>
        </v-col>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
import { TransitionHook, Function } from "../models/models";
import http from "../helpers/http";

export default {
  name: "CreateTransitionHookForm",
  props: ["workflow", "transition_meta", "transition", "object_id", "excluded_function_ids"],
  data: () => ({
    functions_loading: false,
    selected_function: null,
    functions: [],
    search_functions: null
  }),
  mounted() {},
  watch: {
    selected_function(val) {
      this.search_functions = null;
    },
    search_functions(searchTerm) {
      if (!searchTerm || (this.selected_function && this.selected_function.name.includes(searchTerm))) {
        return;
      }
      this.functions_loading = true;
      http
        .get(
          "/function/list/",
          response => (this.functions = response.data.map(f => Function.of(f.id, f.name, f.body)).filter(f => !this.excluded_function_ids.includes(f.id)))
        )
        .finally(() => (this.functions_loading = false));
    }
  },
  methods: {
    createHook() {
      var hook = TransitionHook.create(this.workflow, this.selected_function, this.transition_meta, this.transition, this.object_id);
      this.$emit("on-create", hook);
      this.selected_function = null;
    }
  }
};
</script>