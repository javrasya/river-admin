<template>
  <div>
    <EmptyState
      label="Create your initial state"
      description="Creating your initial state, you'll be able to start designing your workflow."
    >
      <template v-slot:icon>mdi-file-tree</template>
      <template v-slot:content>
        <v-row justify="center" align="center">
          <v-col>
            <WorkflowInput v-model="workflow" />
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-col>
            <StateInput v-model="initial_state" placeholder="Search for initial state" />
          </v-col>
        </v-row>
        <v-row>
          <v-btn
            block
            color="primary"
            :disabled="!(workflow && initial_state)"
            @click="createWorkflow"
          >Create</v-btn>
        </v-row>
      </template>
    </EmptyState>
  </div>
</template>

<script>
import WorkflowInput from "@/components/WorkflowInput.vue";
import StateInput from "@/components/StateInput.vue";
import EmptyState from "@/components/EmptyState.vue";
import { Workflow } from "@/models/models";
import { emit_success } from "@/helpers/event_bus";
import http from "@/helpers/http";

export default {
  name: "CreateWorkflowPage",
  components: {
    WorkflowInput,
    StateInput,
    EmptyState
  },
  data: () => ({
    workflow: null,
    initial_state: null
  }),
  methods: {
    createWorkflow() {
      if (this.workflow && this.initial_state) {
        var promise = Promise.resolve();
        if (this.initial_state.is_new) {
          promise = http.post("/state/create/", this.initial_state.to_create_request(), response => {
            this.initial_state.is_new = false;
            this.initial_state.id = response.data.id;
            this.initial_state.final_label = this.initial_state.label;
          });
        }

        promise.then(response => {
          this.workflow.initial_state = this.initial_state;
          http.post("/workflow/create/", this.workflow.to_create_request(), response => {
            this.workflow.id = response.data.id;
            emit_success(`Workflow ${this.workflow.identifier} is created with initial state ${this.initial_state.label}`);
            this.$router.push({ name: "edit-workflow", params: { id: this.workflow.id } });
          });
        });
      }
    }
  }
};
</script>