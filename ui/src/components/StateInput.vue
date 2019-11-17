<template>
  <v-autocomplete
    v-model="model"
    :items="items"
    :loading="loading"
    :search-input.sync="search"
    hide-selected
    item-text="final_label"
    :label="placeholder"
    :disabled="disabled"
    v-if="initialized"
    clearable
    return-object
  >
    <template v-slot:no-data>
      <v-list-item>
        <v-list-item-title>
          Start typing to search for the
          <strong>state</strong>
        </v-list-item-title>
      </v-list-item>
    </template>
    <template v-slot:selection="{ attr, on, item, selected }">{{ item.label }}</template>
    <template v-slot:item="{ item }">
      <v-list-item-content>
        <v-list-item-title v-text="item.final_label"></v-list-item-title>
      </v-list-item-content>
    </template>
  </v-autocomplete>
</template>

<script>
import http from "../helpers/http";
import { auth, STATE } from "../helpers/auth";
import { State } from "../models/models";

export default {
  name: "StateInput",
  props: ["value", "placeholder", "disabled"],
  data: () => ({
    initialized: false,
    loading: false,
    items: [],
    search: null,
    model: null,
    has_add_state_permission: false
  }),
  mounted() {
    auth
      .has_add_permission(STATE, answer => {
        this.has_add_state_permission = answer;
      })
      .finally(() => (this.initialized = true));
  },
  watch: {
    model(val) {
      this.$emit("input", val);
    },
    value(val) {
      if (val == null) {
        this.model = null;
      }
    },
    search(searchTerm) {
      if (!searchTerm || (this.model && searchTerm === this.model.final_label)) {
        return;
      }
      this.loading = true;
      this._getRemoteStates()
        .then(remoteStates => {
          var newState = null;
          if (this.has_add_state_permission && searchTerm && !remoteStates.find(state => state.label == searchTerm)) {
            newState = State.create(searchTerm);
          }

          var allStates = newState ? [newState].concat(remoteStates) : remoteStates;

          var result = Object.values(
            allStates.reduce((agg, state) => {
              agg[state.label] = state;
              return agg;
            }, {})
          ).sort((s1, s2) => (s1.is_new || s1.id < s2.id ? -1 : 1));
          this.items = result
            .filter(state => state.label.includes(searchTerm))
            .map(state => {
              state.final_label = state.is_new ? state.label + " (Create)" : state.label;
              return state;
            });
        })
        .finally(() => (this.loading = false));
    }
  },
  methods: {
    _getRemoteStates() {
      return http.get("/state/list/", response => {
        return response.data.map(remoteState => State.of(remoteState.id, remoteState.label));
      });
    }
  }
};
</script>