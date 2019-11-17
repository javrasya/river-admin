<template>
  <v-container fluid>
    <v-row justify="center" align="center">
      <v-col justify="center" align="center">
        <h1>
          <v-icon class="mb-2" style="font-size:35px">mdi-label-variant-outline</v-icon>&nbsp;States
        </h1>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col>
        <v-data-table :headers="headers" :items="items" :items-per-page="10" class="elevation-1">
          <template v-slot:item.action="{ item }">
            <v-icon
              class="mr-1"
              color="warning"
              @click="showDeletingDialog(item)"
              :disabled="!has_delete_state_permission"
            >mdi-delete</v-icon>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <v-dialog v-if="this.deletingState" v-model="deleteDialog" max-width="50%">
      <v-card>
        <v-card-title class="headline">
          Delete state
          <v-chip color="primary" class="white--text">
            <v-icon left>mdi-label-variant</v-icon>
            {{ deletingState.label }}
          </v-chip>?
        </v-card-title>

        <v-card-actions>
          <div class="flex-grow-1"></div>

          <v-btn large color="primary" @click="deleteDialog = false">Close</v-btn>

          <v-btn large color="warning" @click="deleteState()">Agree</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { emit_success } from "../../helpers/event_bus";
import { auth, STATE } from "../../helpers/auth";
import http from "../../helpers/http";
export default {
  name: "ListStatePage",
  data: () => ({
    deletingState: null,
    deleteDialog: false,
    headers: [
      { text: "Slug", value: "slug", align: "left" },
      { text: "Label", value: "label", align: "left" },
      { text: "Actions", value: "action", sortable: false }
    ],
    items: [],
    has_delete_state_permission: false
  }),
  mounted() {
    this.fetchStates();
  },
  methods: {
    fetchStates() {
      var states_fetcher = http.get("/state/list/", response => {
        this.items = response.data;
      });

      var delete_state_permission_checker = auth.has_delete_permission(STATE, answer => {
        this.has_delete_state_permission = answer;
      });

      Promise.all([states_fetcher, delete_state_permission_checker]).then(() => (this.initialized = true));
    },
    showDeletingDialog(_state) {
      this.deletingState = _state;
      this.deleteDialog = true;
    },
    deleteState() {
      if (this.deletingState) {
        http.delete(`/state/delete/${this.deletingState.id}/`, () => {
          this.fetchStates();
          this.deleteDialog = false;
          emit_success(`State '${this.deletingState.label}' is deleted`);
        });
      }
    }
  }
};
</script>

<style>
.fab_container {
  position: fixed;
  bottom: 45px;
  right: 30px;
}
</style>