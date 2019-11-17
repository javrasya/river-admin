<template>
  <v-container fluid>
    <v-row justify="center" align="center">
      <v-col justify="center" align="center">
        <h1>
          <v-icon class="mb-2" style="font-size:35px">mdi-function-variant</v-icon>&nbsp;Functions
        </h1>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col>
        <v-data-table :headers="headers" :items="items" :items-per-page="10" class="elevation-1">
          <template v-slot:item.action="{ item }">
            <v-icon class="mr-1" color="primary" @click="goToViewFunctionPage(item.id)">mdi-details</v-icon>
            <v-icon
              class="mr-1"
              color="primary"
              @click="goToEditFunctionPage(item.id)"
              :disabled="!has_change_function_permission"
            >mdi-pencil</v-icon>
            <v-icon
              class="mr-1"
              color="warning"
              @click="showDeletingDialog(item)"
              :disabled="!has_delete_function_permission"
            >mdi-delete</v-icon>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <div class="fab_container" v-if="has_add_function_permission">
      <v-btn large color="primary" @click="goToCreateFunctionPage" dark fab>
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </div>
    <v-dialog v-if="this.deletingFunction" v-model="deleteDialog" max-width="50%">
      <v-card>
        <v-card-title class="headline">
          Delete function
          <v-chip color="primary" class="white--text">
            <v-icon left>mdi-function-variant</v-icon>
            {{ deletingFunction.name }}
          </v-chip>?
        </v-card-title>

        <v-card-actions>
          <div class="flex-grow-1"></div>

          <v-btn large color="primary" @click="deleteDialog = false">Close</v-btn>

          <v-btn large color="warning" @click="deleteFunction()">Agree</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { emit_success } from "../../helpers/event_bus";
import { auth, FUNCTION } from "../../helpers/auth";
import http from "../../helpers/http";
export default {
  name: "ListCallbackFunctionPage",
  data: () => ({
    deletingFunction: null,
    deleteDialog: false,
    headers: [
      { text: "Name", value: "name", align: "left" },
      { text: "Version", value: "version", align: "left" },
      { text: "Created At", value: "date_created", align: "left" },
      { text: "Last Updated At", value: "date_updated", align: "left" },
      { text: "Actions", value: "action", sortable: false }
    ],
    items: [],
    has_add_function_permission: false,
    has_delete_function_permission: false,
    has_change_function_permission: false
  }),
  mounted() {
    this.fetchFunctions();
  },
  methods: {
    setAlertMessage(message) {
      this.message = message;
      this.messageAlert = true;
      var that = this;
      setTimeout(() => (that.messageAlert = false), 3000);
    },
    fetchFunctions() {
      var functions_fetcher = http.get("/function/list/", response => {
        this.items = response.data.map(item => ({
          ...item,
          version: `v${item.version}`
        }));
      });

      var add_function_permission_checker = auth.has_add_permission(FUNCTION, answer => {
        this.has_add_function_permission = answer;
      });

      var change_function_permission_checker = auth.has_change_permission(FUNCTION, answer => {
        this.has_change_function_permission = answer;
      });

      var delete_function_permission_checker = auth.has_delete_permission(FUNCTION, answer => {
        this.has_delete_function_permission = answer;
      });

      Promise.all([functions_fetcher, add_function_permission_checker, change_function_permission_checker, delete_function_permission_checker]).then(
        () => (this.initialized = true)
      );
    },
    goToCreateFunctionPage() {
      this.$router.push({ name: "create-callback-function" });
    },
    goToViewFunctionPage(functionId) {
      this.$router.push({
        name: "view-callback-function",
        params: { id: functionId }
      });
    },
    goToEditFunctionPage(functionId) {
      this.$router.push({
        name: "edit-callback-function",
        params: { id: functionId }
      });
    },
    showDeletingDialog(_function) {
      this.deletingFunction = _function;
      this.deleteDialog = true;
    },
    deleteFunction() {
      if (this.deletingFunction) {
        http.delete(`/function/delete/${this.deletingFunction.id}/`, () => {
          this.fetchFunctions();
          this.deleteDialog = false;
          emit_success(`Function '${this.deletingFunction.name}' is deleted`);
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