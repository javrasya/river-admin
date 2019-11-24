<template>
  <v-card class="pa-5" :elevation="6">
    <v-card-title>New Approval Rule</v-card-title>
    <v-card-text>
      <v-container fluid>
        <v-row>
          <v-col>
            <v-autocomplete
              v-model="selected_permissions"
              :items="permissions"
              :loading="permissions_loading"
              :search-input.sync="search_permissions"
              hide-selected
              item-text="identifier"
              label="Search permissions"
              clearable
              chips
              multiple
              return-object
            >
              <template v-slot:no-data>
                <v-list-item>
                  <v-list-item-title>
                    Start typing to search for the
                    <strong>permissions</strong>
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
                  <v-icon left>mdi-lock</v-icon>
                  <span v-text="item.identifier"></span>
                </v-chip>
              </template>
              <template v-slot:item="{ item }">
                <v-list-item-content>
                  <v-list-item-title v-text="item.identifier"></v-list-item-title>
                </v-list-item-content>
              </template>
            </v-autocomplete>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-autocomplete
              v-model="selected_groups"
              :items="groups"
              :loading="groups_loading"
              :search-input.sync="search_groups"
              hide-selected
              item-text="name"
              label="Search groups"
              clearable
              chips
              multiple
              return-object
            >
              <template v-slot:no-data>
                <v-list-item>
                  <v-list-item-title>
                    Start typing to search for the
                    <strong>groups</strong>
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
                  <v-icon left>mdi-account-multiple</v-icon>
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
          <v-btn large color="primary" @click="createApproval">Create Approval</v-btn>
        </v-col>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
import { Approval } from "@/models/models";
import http from "@/helpers/http";

export default {
  name: "CreateApprovalForm",
  props: ["workflow", "transition_id"],
  data: () => ({
    permissions_loading: false,
    groups_loading: false,
    selected_permissions: [],
    selected_groups: [],
    groups: [],
    permissions: [],
    search_permissions: null,
    search_groups: null
  }),
  mounted() {},
  watch: {
    selected_permissions(val) {
      this.search_permissions = null;
    },
    search_permissions(searchTerm) {
      if (!searchTerm || (this.selected_permissions && this.selected_permissions.map(p => p.identifier).includes(searchTerm))) {
        return;
      }
      this.permissions_loading = true;
      http
        .get("/permission/list/", response => {
          this.permissions = response.data.map(permission => ({
            identifier: permission.codename + "." + permission.content_type.app_label + "." + permission.content_type.model,
            ...permission
          }));
        })
        .finally(() => (this.permissions_loading = false));
    },
    selected_groups(val) {
      this.search_groups = null;
    },
    search_groups(searchTerm) {
      if (!searchTerm || (this.selected_groups && this.selected_groups.map(p => p.name).includes(searchTerm))) {
        return;
      }
      this.groups_loading = true;
      http.get("/group/list/", response => (this.groups = response.data)).finally(() => (this.groups_loading = false));
    }
  },
  methods: {
    createApproval() {
      this.$emit("on-create", Approval.create(this.transition_id, this.workflow, this.selected_permissions, this.selected_groups, this.given_priority));
      this.selected_permissions = [];
      this.selected_groups = [];
      this.given_priority = 0;
    }
  }
};
</script>