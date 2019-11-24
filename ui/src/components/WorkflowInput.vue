<template>
  <v-autocomplete
    v-model="model"
    :items="items"
    :loading="loading"
    :search-input.sync="search"
    hide-selected
    item-text="identifier"
    label="Search for a workflow..."
    clearable
    return-object
  >
    <template v-slot:no-data>
      <v-list-item>
        <v-list-item-title>
          Start typing to search for the
          <strong>workflows</strong>
        </v-list-item-title>
      </v-list-item>
    </template>
    <template v-slot:selection="{ attr, on, item, selected }">{{ item.identifier }}</template>
    <template v-slot:item="{ item }">
      <v-list-item-content>
        <v-list-item-title v-text="item.identifier"></v-list-item-title>
      </v-list-item-content>
    </template>
  </v-autocomplete>
</template>

<script>
import { Workflow } from "@/models/models";
import http from "@/helpers/http";

export default {
  name: "WorkflowInput",
  props: ["value"],
  data: () => ({
    loading: false,
    items: [],
    search: null,
    model: null
  }),
  watch: {
    model(val) {
      this.$emit("input", val);
    },
    search(val) {
      if (this.items.length > 0) return;
      this.loading = true;

      http
        .get("/workflow/state-field/list/", response => {
          var that = this;
          this.items = response.data.map(result => Workflow.create(result.content_type, null, result.field_name));
        })
        .finally(() => (this.loading = false));
    }
  }
};
</script>