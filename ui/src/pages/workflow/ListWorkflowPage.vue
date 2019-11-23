<template>
  <v-container fluid v-if="initialized">
    <v-container v-if="items.length==0" fluid>
      <EmptyState
        label="You don't seem to have any workflow"
        description="Why don't you create your first workflow?"
      >
        <template v-slot:icon>mdi-sitemap</template>
        <template v-slot:content>
          <v-row justify="center" align="center">
            <v-col>
              <v-btn block color="primary" @click="goToCreateWorkflowPage">Begin</v-btn>
            </v-col>
          </v-row>
        </template>
      </EmptyState>
    </v-container>
    <v-container v-else fluid>
      <v-flex>
        <v-alert
          type="success"
          class="transition-swing"
          transition="scale-transition"
          v-model="messageAlert"
          v-if="message"
        >{{message}}</v-alert>
      </v-flex>
      <v-row justify="center" align="center">
        <v-col justify="center" align="center">
          <h1>
            <v-icon class="mb-2" style="font-size:35px">mdi-sitemap</v-icon>&nbsp;Workflows
          </h1>
        </v-col>
      </v-row>
      <v-row>
        <v-col v-for="item in items" :key="item.id" xl="2" lg="3" md="4" sm="12" xs="12">
          <v-hover>
            <template v-slot="{ hover }">
              <v-card :elevation="hover ? 24 : 6" height="300" min-width="200">
                <v-card-text class="card-text">
                  <v-row class="fill-height">
                    <v-col v-if="item.admin_name">
                      <v-row
                        class="mt-5 mb-10"
                        align="center"
                        justify="center"
                        v-if="item.admin_icon"
                      >
                        <v-icon color="primary" x-large>{{ item.admin_icon}}</v-icon>
                      </v-row>
                      <v-row class="mt-5 mb-10" align="center" justify="center">
                        <H5Max v-model="item.admin_name" max="16" />
                      </v-row>
                    </v-col>
                    <v-col v-else>
                      <v-row class="mt-5 mb-10" align="center" justify="center">
                        <H5Max v-model="item.content_type.app_label" max="16" />
                      </v-row>
                      <v-row class="mb-10" align="center" justify="center">
                        <H5Max v-model="item.content_type.model" max="16" />
                      </v-row>
                      <v-row align="center" justify="center">
                        <H5Max v-model="item.field_name" max="16" />
                      </v-row>
                    </v-col>
                  </v-row>
                </v-card-text>
                <v-divider></v-divider>

                <v-card-actions>
                  <div class="flex-grow-1" />
                  <v-tooltip top>
                    <template v-slot:activator="{ on }">
                      <v-btn icon color="primary" v-on="on" @click="goToViewWorkflowPage(item.id)">
                        <v-icon>mdi-details</v-icon>
                      </v-btn>
                    </template>
                    <span>View Workflow</span>
                  </v-tooltip>
                  <v-tooltip top>
                    <template v-slot:activator="{ on }">
                      <v-btn
                        icon
                        color="primary"
                        v-on="on"
                        @click="goToEditWorkflowPage(item.id)"
                        :disabled="!has_change_workflow_permission"
                      >
                        <v-icon>mdi-pencil</v-icon>
                      </v-btn>
                    </template>
                    <span>Edit Workflow</span>
                  </v-tooltip>
                  <v-tooltip top>
                    <template v-slot:activator="{ on }">
                      <v-btn
                        icon
                        color="primary"
                        v-on="on"
                        @click="goToEditWorkflowRulePage(item.id)"
                        :disabled="!has_change_workflow_permission"
                      >
                        <v-icon>mdi-axis-arrow-lock</v-icon>
                      </v-btn>
                    </template>
                    <span>Edit Workflow Rules</span>
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
                    <span>Delete Workflow</span>
                  </v-tooltip>
                  <div class="flex-grow-1" />
                </v-card-actions>
              </v-card>
            </template>
          </v-hover>
        </v-col>
      </v-row>
      <div class="fab_container" v-if="has_add_workflow_permission">
        <v-btn large color="primary" @click="goToCreateWorkflowPage" dark fab>
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </div>
      <v-dialog v-if="this.deletingWorkflow" v-model="deleteDialog" max-width="50%">
        <v-card>
          <v-card-title class="headline">
            Delete workflow &nbsp;
            <v-chip color="primary">{{ deletingWorkflow.identifier }}</v-chip>&nbsp; ?
          </v-card-title>

          <v-card-text>Deleting the workflow will delete all transitions and approval meta data belongs to it.</v-card-text>

          <v-card-actions>
            <div class="flex-grow-1"></div>

            <v-btn large color="primary" @click="deleteDialog = false">Close</v-btn>

            <v-btn large color="warning" @click="deleteWorkflow()">Agree</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </v-container>
</template>

<script>
import http from "../../helpers/http";
import EmptyState from "../../components/EmptyState";
import H5Max from "../../components/H5Max";
import { emit_success } from "../../helpers/event_bus";
import { auth, WORKFLOW } from "../../helpers/auth";
import { Workflow } from "../../models/models";

export default {
  name: "ListWorkflowPage",
  components: {
    EmptyState,
    H5Max
  },
  computed: {
    deletingWorkflowDialogTitle() {
      return `Delete workflow ${this.deletingWorkflow.identifier}?`;
    }
  },
  mounted() {
    this.fetchWorkflows();
    this.message = this.$route.query.message;
    if (this.$route.query.message) {
      this.setAlertMessage(this.$route.query.message);
    }
  },
  data: () => ({
    initialized: false,
    messageAlert: true,
    message: null,
    deletingWorkflow: null,
    deleteDialog: false,
    has_add_workflow_permission: false,
    has_delete_workflow_permission: false,
    has_change_workflow_permission: false,
    items: []
  }),
  methods: {
    setAlertMessage(message) {
      this.message = message;
      this.messageAlert = true;
      var that = this;
      setTimeout(() => (that.messageAlert = false), 3000);
    },
    fetchWorkflows() {
      var workflow_fetcher = http.get("/workflow/list/", response => {
        this.items = response.data.map(workflow => {
          var workflow_model = Workflow.of(workflow.id, workflow.content_type, workflow.initial_state, workflow.field_name);
          workflow_model.admin_name = workflow.admin_name;
          workflow_model.admin_icon = workflow.admin_icon;
          return workflow_model;
        });
      });

      var add_workflow_permission_checker = auth.has_add_permission(WORKFLOW, answer => {
        this.has_add_workflow_permission = answer;
      });

      var change_workflow_permission_checker = auth.has_change_permission(WORKFLOW, answer => {
        this.has_change_workflow_permission = answer;
      });

      var delete_workflow_permission_checker = auth.has_delete_permission(WORKFLOW, answer => {
        this.has_delete_workflow_permission = answer;
      });

      Promise.all([workflow_fetcher, add_workflow_permission_checker, change_workflow_permission_checker, delete_workflow_permission_checker]).then(
        () => (this.initialized = true)
      );
    },
    goToCreateWorkflowPage() {
      this.$router.push({ name: "create-workflow" });
    },
    goToViewWorkflowPage(workflowId) {
      this.$router.push({
        name: "view-workflow",
        params: { id: workflowId }
      });
    },
    goToEditWorkflowPage(workflowId) {
      this.$router.push({
        name: "edit-workflow",
        params: { id: workflowId }
      });
    },

    goToEditWorkflowRulePage(workflowId) {
      this.$router.push({
        name: "edit-workflow-rules",
        params: { id: workflowId }
      });
    },

    showDeletingDialog(workflow) {
      this.deletingWorkflow = workflow;
      this.deleteDialog = true;
    },
    deleteWorkflow() {
      if (this.deletingWorkflow) {
        http.delete(`/workflow/delete/${this.deletingWorkflow.id}/`, () => {
          this.fetchWorkflows();
          this.deleteDialog = false;
          emit_success(`Workflow ${this.deletingWorkflow.identifier} is deleted.`);
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

.card-text {
  height: 80%;
  font-size: 30px;
}
</style>