<template>
  <v-container fluid v-if="initialized">
    <v-container fluid>
      <v-row justify="center" align="center">
        <v-col justify="center" align="center">
          <h1>
            Workflow objects of
            <v-chip color="primary" class="white--text">
              <v-icon left>mdi-sitemap</v-icon>
              <span v-text="workflow.identifier"></span>
            </v-chip>
          </h1>
        </v-col>
      </v-row>
      <v-row justify="center" align="center">
        <v-col>
          <v-data-table
            :headers="headers"
            :items="workflow_objects"
            :items-per-page="10"
            class="elevation-1"
          >
            <template v-slot:item.action="{ item }">
              <v-tooltip top>
                <template v-slot:activator="{ on }">
                  <v-icon
                    class="mr-1"
                    v-on="on"
                    color="primary"
                    @click="goToTimeline(item)"
                    :disabled="!has_change_workflow_permission"
                  >mdi-timeline-text</v-icon>
                </template>
                <span>View Timeline</span>
              </v-tooltip>
              <v-tooltip top>
                <template v-slot:activator="{ on }">
                  <v-btn
                    icon
                    color="warning"
                    v-on="on"
                    @click="showDeletingDialog(item)"
                    :disabled="!has_delete_workflow_permission"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>
                <span>Delete Workflow Object</span>
              </v-tooltip>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-container>
    <v-dialog v-if="this.deletingWorkflowObject" v-model="deleteDialog" max-width="50%">
      <v-card>
        <v-card-title class="headline">
          Delete workflow object &nbsp;
          <v-chip color="primary">{{ deletingWorkflowObject.identifier }}</v-chip>&nbsp; ?
        </v-card-title>

        <v-card-actions>
          <div class="flex-grow-1"></div>

          <v-btn large color="primary" @click="deleteDialog = false">Close</v-btn>

          <v-btn large color="warning" @click="deleteWorkflowObject()">Agree</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>



<script>
import EmptyState from "../../components/EmptyState";
import WorkflowIllustration from "../../components/WorkflowIllustration";

import { Workflow } from "../../models/models";
import { emit_success } from "../../helpers/event_bus";
import { auth, WORKFLOW } from "../../helpers/auth";
import http from "../../helpers/http";

export default {
  name: "ListWorkflowObjectsPage",
  components: {
    EmptyState,
    WorkflowIllustration
  },
  data: () => ({
    initialized: false,
    workflow_loading: false,
    workflow: null,
    headers: null,
    deletingWorkflowObject: null,
    deleteDialog: false,
    workflow_objects: [],
    has_delete_workflow_permission: false,
    has_change_workflow_permission: false
  }),
  watch: {
    $route(to, from) {
      if (to.params.workflow_id != from.params.workflow_id) {
        this.load();
      }
    }
  },
  mounted() {
    this.load();
  },
  methods: {
    load() {
      this.initialized = false;
      var workflow_id = this.$route.params.workflow_id;
      var workflow_fetcher = http.get(
        `/workflow/get/${workflow_id}/`,
        response => (this.workflow = Workflow.of(response.data.id, response.data.content_type, response.data.initial_state, response.data.field_name))
      );

      var change_workflow_permission_checker = auth.has_change_permission(WORKFLOW, answer => {
        this.has_change_workflow_permission = answer;
      });

      var delete_workflow_permission_checker = auth.has_delete_permission(WORKFLOW, answer => {
        this.has_delete_workflow_permission = answer;
      });

      Promise.all([workflow_fetcher, change_workflow_permission_checker, delete_workflow_permission_checker])
        .then(() => this.fetchWorkflowObjects())
        .then(() => (this.initialized = true))
        .finally(() => (this.workflow_loading = false));
    },
    goToCreateWorkflowPage() {
      this.$router.push({ name: "create-workflow" });
    },
    fetchWorkflowObjects() {
      this.workflow_object_loading = true;
      return http
        .get(`/workflow/object/list/${this.workflow.id}/`, response => {
          this.headers = response.data.headers
            .map(key => ({ text: key, value: key, align: "left" }))
            .concat([{ text: "Actions", value: "action", sortable: false }]);
          this.workflow_objects = response.data.workflow_objects.map(workflow_object => ({ ...workflow_object, identifier: workflow_object.__str }));
        })
        .finally(() => (this.workflow_object_loading = false));
    },
    goToTimeline(item) {
      this.$router.push({
        name: "edit-workflow-object-timeline",
        params: { workflow_id: this.workflow.id, object_id: item.pk }
      });
    },
    showDeletingDialog(workflow_object) {
      this.deletingWorkflowObject = workflow_object;
      this.deleteDialog = true;
    },
    deleteWorkflowObject() {
      if (this.deletingWorkflowObject) {
        http.delete(`/workflow-object/delete/${this.workflow.id}/${this.deletingWorkflowObject.id}/`, () => {
          this.fetchWorkflowObjects();
          this.deleteDialog = false;
          emit_success(`Workflow object ${this.deletingWorkflowObject.identifier} is deleted.`);
        });
      }
    },
    _updateQuery(update) {
      var query = { ...this.$route.query, ...update };

      var that = this;
      if (Object.keys(query).some(queryKey => that.$route.query[queryKey] != query[queryKey])) {
        this.$router.push({ query });
      }
    }
  }
};
</script>