<template>
  <div>
    <v-container v-if="initialized" fluid>
      <v-row>
        <v-col></v-col>
        <v-col justify="center" align="center">
          <h1>
            Workflow for
            <v-chip>{{ workflow.identifier }}</v-chip>
          </h1>
        </v-col>
        <v-col justify="center" align="end">
          <v-btn
            class="mr-5"
            :disabled="transitions.length==0"
            color="primary"
            @click="goToEditWorkflowRules"
          >Edit Workflow Rules</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <WorkflowIllustration
            :states="states"
            :transitions="transitions"
            :state_class_mapping="state_class_mapping"
            :editable="true"
            @on-transition-selected="onTransitionSelected"
            @on-state-clicked="onStateSelected"
          />
        </v-col>
      </v-row>
      <v-row justify="center" align="center">
        <v-col cols="6">
          <StateInput
            :disabled="!selected_state"
            v-model="new_transition_state"
            :placeholder="selected_state?`New state from '${selected_state.label}':`:'Select a state to creat a transition'"
          />
        </v-col>
        <v-col cols="1">
          <v-btn
            :disabled="!selected_state || !new_transition_state"
            large
            color="primary"
            @click="createState"
          >Create</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import WorkflowIllustration from "../../components/WorkflowIllustration";
import StateInput from "../../components/StateInput";
import { Woprkflow, Approval, Transition, State, Workflow } from "../../models/models";
import { emit_success } from "../../helpers/event_bus";
import http from "../../helpers/http";

export default {
  name: "CreateWorkflowPage",
  components: {
    WorkflowIllustration,
    StateInput
  },
  data: () => ({
    workflow: null,
    initialized: false,
    selected_transition: null,
    states: [],
    transitions: [],
    transition_approvals: {},
    selected_state: null,
    new_transition_state: null,
    state_class_mapping: {},
    selected_state_class: {
      rect: {
        fill: "deepskyblue"
      },
      label: {
        stroke: "white"
      }
    },
    default_state_class: {
      rect: {
        fill: "#dddd"
      },
      label: {
        stroke: "black"
      }
    }
  }),
  mounted() {
    var workflow_id = this.$route.params.id;
    this.workflow = http.get(`/workflow/get/${workflow_id}/`, result => {
      this.workflow = Workflow.of(result.data.id, result.data.content_type, result.data.initial_state, result.data.field_name);

      var state_fetcher = http.get(`/workflow/state/list/${workflow_id}/`, result => {
        this.states = result.data.map(state => State.of(state.id, state.label));
      });

      var transition_meta_fetcher = http.get(`/workflow/transition-meta/list/${workflow_id}/`, result => {
        this.transitions = result.data.map(transition => Transition.of(transition.id, this.workflow, transition.source_state, transition.destination_state));
      });

      Promise.all([state_fetcher, transition_meta_fetcher]).then(() => {
        this.initialized = true;

        var selected_state = JSON.parse(this.$route.query.selected_state || null);
        if (selected_state) {
          this._selected_state(selected_state);
        }
      });
    });
  },
  methods: {
    onStateSelected(state) {
      this._selected_state(state);
    },
    _selected_state(state) {
      if (this.selected_state) {
        this.$set(this.state_class_mapping, this.selected_state.id, this.default_state_class);
      }
      this.$set(this.state_class_mapping, state.id, this.selected_state_class);

      this.selected_state = state;

      this.updateQuery({
        selected_state: JSON.stringify(this.selected_state)
      });
    },
    createState() {
      if (this.new_transition_state) {
        var promise = Promise.resolve();
        var is_state_created = false;
        if (this.new_transition_state.is_new) {
          promise = http.post("/state/create/", this.new_transition_state.to_create_request(), response => {
            is_state_created = true;
            this.new_transition_state.is_new = false;
            this.new_transition_state.id = response.data.id;
            this.new_transition_state.final_label = this.new_transition_state.label;
          });
        }
        promise.then(response => {
          var parent = this.states.find(state => state.id == this.selected_state.id);
          var new_transition = Transition.create(this.workflow, parent.id, this.new_transition_state.id);
          http.post("/transition-meta/create/", new_transition.to_create_request(), response => {
            if (!this.states.find(state => state.id == this.new_transition_state.id)) {
              this.states.push(this.new_transition_state);
            }

            var source_state = this.states.find(state => state.id == new_transition.source_state_id);
            var destination_state = this.states.find(state => state.id == new_transition.destination_state_id);

            emit_success(`Transition meta ${source_state.label} -> ${destination_state.label}${is_state_created ? " ( New )" : ""} is created`, 2000);

            new_transition.is_new = false;
            new_transition.id = response.data.id;
            this.transitions.push(new_transition);
            this._selected_state(this.new_transition_state);
            this.new_transition_state = null;
          });
        });
      }
    },
    updateQuery(update) {
      var query = { ...this.$route.query, ...update };

      var that = this;
      if (Object.keys(query).some(queryKey => that.$route.query[queryKey] != query[queryKey])) {
        this.$router.push({ query });
      }
    },

    onTransitionSelected(transition_id) {
      this.selected_transition = this.transitions.find(transition => transition.id == transition_id);
    },

    goToEditWorkflowRules() {
      this.$router.push({ name: "edit-workflow-rules", params: { id: this.workflow.id } });
    }
  }
};
</script>
