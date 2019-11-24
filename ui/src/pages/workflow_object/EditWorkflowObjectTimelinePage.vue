<template>
  <div v-if="initialized">
    <v-container v-if="states && transitions" fluid>
      <v-row justify="center" align="center" class="mb-6">
        <h1>
          Active Workflow for
          <v-chip>{{ object_identifier }}</v-chip>
        </h1>
      </v-row>
      <v-row>
        <v-flex xs12 sm12 md6>
          <v-container>
            <WorkflowIllustration
              :states="states"
              :transitions="transitions"
              :editable="false"
              :state_class_mapping="state_class_mapping"
              @on-transition-selected="on_transition_selected"
            />
          </v-container>
        </v-flex>
        <v-flex xs12 sm12 md6>
          <v-container v-if="selected_transition && !selected_transition.is_cancelled">
            <v-row>
              <v-col>
                <v-card class="pa-5" :elevation="6">
                  <v-card-title>
                    <v-row>
                      <v-col cols="9">
                        Transition steps from
                        <v-chip color="primary" class="white--text">
                          <span v-text="get_state_by(selected_transition.source_state_id).label"></span>
                        </v-chip>to
                        <v-chip color="primary" class="white--text">
                          <span
                            v-text="get_state_by(selected_transition.destination_state_id).label "
                          ></span>
                        </v-chip>
                      </v-col>
                      <div class="flex-grow-1" />
                      <v-col v-if="!selected_transition.is_done && !readonly">
                        <v-speed-dial
                          v-model="fab"
                          :bottom="true"
                          :right="true"
                          direction="left"
                          :open-on-hover="true"
                        >
                          <template v-slot:activator>
                            <v-btn v-model="fab" color="primary" dark fab>
                              <v-icon v-if="fab">mdi-close</v-icon>
                              <v-icon v-else>mdi-plus</v-icon>
                            </v-btn>
                          </template>

                          <v-tooltip top>
                            <template v-slot:activator="{ on }">
                              <v-btn
                                fab
                                dark
                                small
                                v-on="on"
                                color="green"
                                @click="newTransitionHookDialog=true"
                              >
                                <v-icon>mdi-function-variant</v-icon>
                              </v-btn>
                            </template>
                            <span>Create Transition Hook</span>
                          </v-tooltip>
                        </v-speed-dial>
                      </v-col>
                    </v-row>
                  </v-card-title>
                  <v-card-text>
                    <ObjectApprovalList
                      :workflow="workflow"
                      :object_id="$route.params.object_id"
                      :object_approvals="selected_transition.approvals"
                      :editable="!readonly"
                      @on-hook-create="on_approval_hook_created"
                      @on-hook-delete="on_approval_hook_deleted"
                    />
                    <div v-if="selected_transition.hooks.length>0">
                      <v-divider />
                      <span class="title font-weight-light">Right before the transition happens</span>
                      <div v-for="(hook) in selected_transition.hooks" :key="hook.id">
                        <HookDetail
                          class="my-1"
                          :hook="hook"
                          :editable="!hook.is_from_upstream() && !readonly"
                          @on-delete="on_transition_hook_deleted"
                        />
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
          <v-container v-else>
            <EmptyState
              label="Select an uncancelled transition"
              description="Selecting a transition by clicking the arrow, you'll be able to create transition steps."
            >
              <template v-slot:icon>mdi-mouse</template>
            </EmptyState>
          </v-container>
        </v-flex>
      </v-row>
    </v-container>

    <v-dialog
      v-model="newTransitionHookDialog"
      max-width="800"
      v-if="!readonly && selected_transition"
    >
      <CreateTransitionHookForm
        :workflow="workflow"
        :transition_meta="selected_transition.transition_meta"
        :transition="selected_transition.id"
        :object_id="$route.params.object_id"
        :excluded_function_ids="selected_transition.hooks.map(hook => hook.callback_function.id)"
        @on-create="on_transition_hook_created"
      />
    </v-dialog>

    <v-dialog v-if="deletingApprovalHook" v-model="deletingApprovalHookDialog" max-width="50%">
      <v-card>
        <v-card-title class="headline">Delete approval hook?</v-card-title>

        <v-card-actions>
          <div class="flex-grow-1"></div>

          <v-btn large color="primary" @click="deletingApprovalHookDialog = false">Close</v-btn>

          <v-btn large color="warning" @click="delete_approval_hook()">Agree</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-if="deletingTransitionHook" v-model="deletingTransitionHookDialog" max-width="50%">
      <v-card>
        <v-card-title class="headline">Delete transition hook?</v-card-title>

        <v-card-actions>
          <div class="flex-grow-1"></div>

          <v-btn large color="primary" @click="deletingTransitionHookDialog = false">Close</v-btn>

          <v-btn large color="warning" @click="delete_transition_hook()">Agree</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import EmptyState from "@/components/EmptyState.vue";
import CreateTransitionHookForm from "@/components/CreateTransitionHookForm.vue";
import HookDetail from "@/components/HookDetail.vue";
import WorkflowIllustration from "@/components/WorkflowIllustration.vue";
import ObjectApprovalList from "@/components/ObjectApprovalList.vue";
import { emit_success } from "@/helpers/event_bus";
import http from "@/helpers/http";
import { Workflow, State, ObjectTransition, ObjectApproval, TransitionHook, ApprovalHook } from "../../models/models";

export default {
  name: "EditWorkflowObjectTimelinePage",
  components: {
    EmptyState,
    CreateTransitionHookForm,
    WorkflowIllustration,
    ObjectApprovalList,
    HookDetail
  },
  props: ["readonly"],
  data: () => ({
    initialized: false,
    fab: null,
    workflow: null,
    object_identifier: null,
    selected_transition: null,
    transition_approvals: {},
    transitions: null,
    states: null,
    current_state: null,
    alert_timeout: 2000,
    current_iteration: null,
    newTransitionHookDialog: false,
    state_class_mapping: {},
    deletingTransitionHook: null,
    deletingTransitionHookDialog: false,
    deletingApprovalHook: null,
    deletingApprovalHookDialog: false,
    pending_state_class: {
      rect: {
        "stroke-dasharray": "10 5",
        fill: "white"
      }
    },
    done_state_class: {
      rect: {
        fill: "#4caf50"
      },
      label: {
        stroke: "white"
      }
    },
    cancelled_state_class: {
      rect: {
        fill: "rgb(195, 189, 189)"
      },
      label: {
        stroke: "white"
      }
    },
    current_state_class: {
      rect: {
        fill: "deepskyblue"
      },
      label: {
        stroke: "white"
      }
    }
  }),
  mounted() {
    var workflow_id = this.$route.params.workflow_id;
    var workflow_object_id = this.$route.params.object_id;
    http.get(`/workflow/get/${workflow_id}/`, response => {
      this.workflow = Workflow.of(response.data.id, response.data.content_type, response.data.initial_state, response.data.field_name);

      var object_identifier_fetcher = http.get(`/workflow-object/identify/${this.workflow.id}/${workflow_object_id}/`, response => {
        this.object_identifier = response.data;
      });

      var current_state_fetcher = http.get(`/workflow-object/current-state/${this.workflow.id}/${workflow_object_id}/`, response => {
        this.current_state = State.of(response.data.id, response.data.label);
      });

      var current_iteration_fetcher = http.get(`/workflow-object/current-iteration/${this.workflow.id}/${workflow_object_id}/`, response => {
        this.current_iteration = response.data;
      });

      var state_fetcher = this.get_states(workflow_id, workflow_object_id).then(states => (this.states = states));
      var transitions_fetcher = this.get_transitions(workflow_id, workflow_object_id)
        .then(transitions => (this.transitions = transitions))
        .then(() => {
          var that = this;
          this.transitions.forEach(transition => {
            if (transition.is_done) {
              that.state_class_mapping[transition.source_state_id] = that.done_state_class;
              that.state_class_mapping[transition.destination_state_id] = that.done_state_class;
            } else if (transition.is_cancelled) {
              that.state_class_mapping[transition.destination_state_id] = that.cancelled_state_class;
            } else {
              that.state_class_mapping[transition.destination_state_id] = that.pending_state_class;
            }
          });
        });

      Promise.all([state_fetcher, transitions_fetcher, current_state_fetcher, current_iteration_fetcher]).then(() => {
        this.state_class_mapping[this.to_state_id(this.current_iteration - 1, this.current_state.id)] = this.current_state_class;

        var selected_transition_id = this.$route.query.selected_transition_id;
        if (selected_transition_id) {
          this.on_transition_selected(selected_transition_id);
        }

        this.initialized = true;
      });
    });
  },
  methods: {
    to_state_id(iteration, state_id) {
      return `${iteration}-${state_id}`;
    },

    get_states(workflow_id, workflow_object_id) {
      return http.get(`/workflow-object/state/list/${workflow_id}/${workflow_object_id}/`, response => {
        return response.data.map(workflow_object_state =>
          State.of(this.to_state_id(workflow_object_state.iteration, workflow_object_state.state.id), workflow_object_state.state.label)
        );
      });
    },

    get_transitions(workflow_id, workflow_object_id) {
      var that = this;
      return http.get(`/workflow-object/transition/list/${workflow_id}/${workflow_object_id}/`, response => {
        return Promise.all(
          response.data.map(transition => {
            var transition = ObjectTransition.of(
              transition.id,
              this.workflow,
              this.to_state_id(transition.iteration - 1, transition.source_state),
              this.to_state_id(transition.iteration, transition.destination_state),
              transition.meta,
              transition.object_id,
              transition.iteration,
              transition.is_cancelled,
              transition.is_done
            );

            var transition_approvals_fetcher = that.get_transition_approvals(transition.id).then(transition_approvals => {
              transition.approvals = transition_approvals;
            });

            var transition_hooks_fetcher = that.get_transition_hooks(transition).then(transition_hooks => {
              transition.hooks = transition_hooks;
            });

            return Promise.all([transition_approvals_fetcher, transition_hooks_fetcher]).then(() => transition);
          })
        );
      });
    },

    get_transition_hooks(transition) {
      return http.get(`/transition/transition-hook/list/${transition.id}/`, response => {
        return response.data.map(transition_hook =>
          TransitionHook.of(
            transition_hook.id,
            this.workflow,
            transition_hook.callback_function,
            transition_hook.transition_meta,
            transition_hook.transition,
            transition_hook.object_id,
            transition.is_done
          )
        );
      });
    },

    get_transition_approvals(transition_id) {
      var that = this;
      return http.get(`/transition/transition-approval/list/${transition_id}/`, response => {
        return Promise.all(
          response.data.map(transition_approval => {
            var approval = ObjectApproval.of(
              transition_approval.id,
              this.workflow,
              transition_approval.transition,
              transition_approval.meta,
              transition_approval.object_id,
              transition_approval.permissions,
              transition_approval.groups,
              transition_approval.priority,
              transition_approval.status,
              transition_approval.transactioner
            );

            return that
              .get_transition_approval_hooks(approval)
              .then(transition_approval_hooks => {
                approval.hooks = transition_approval_hooks;
              })
              .then(() => approval);
          })
        );
      });
    },
    get_transition_approval_hooks(transition_approval) {
      return http.get(`/transition-approval/approval-hook/list/${transition_approval.id}/`, response => {
        return response.data.map(transition_approval_hook =>
          ApprovalHook.of(
            transition_approval_hook.id,
            this.workflow,
            transition_approval_hook.callback_function,
            transition_approval_hook.transition_approval_meta,
            transition_approval_hook.transition_approval,
            transition_approval_hook.object_id,
            transition_approval.is_approved
          )
        );
      });
    },
    on_transition_hook_created(created_hook) {
      if (this.selected_transition && !this.selected_transition.hooks.find(hook => hook.id == created_hook.id)) {
        http.post("/transition-hook/create/", created_hook.to_create_request(), response => {
          created_hook.id = response.data.id;
          this.selected_transition.hooks.push(created_hook);
          this._update_transition(this.selected_transition);
        });
        this.newTransitionHookDialog = false;
        emit_success(`The transition hook is created`, this.alert_timeout);
      }
    },
    on_transition_hook_deleted(deleted_hook) {
      this.deletingTransitionHook = deleted_hook;
      this.deletingTransitionHookDialog = true;
    },
    delete_transition_hook() {
      if (this.selected_transition) {
        http.delete(`/transition-hook/delete/${this.deletingTransitionHook.id}/`, response => {
          this.selected_transition.hooks = this.selected_transition.hooks.filter(hook => hook.id != this.deletingTransitionHook.id);
          this._update_transition(this.selected_transition);
          this.deletingTransitionHook = null;
          this.deletingTransitionHookDialog = true;
          emit_success(`The transition hook is deleted`, this.alert_timeout);
        });
      }
    },

    on_approval_hook_created(created_hook) {
      if (this.selected_transition) {
        var approval = this.selected_transition.approvals.find(approval => approval.id == created_hook.transition_approval_id);
        if (approval && !approval.hooks.find(hook => hook.id == created_hook.id)) {
          http.post("/approval-hook/create/", created_hook.to_create_request(), response => {
            created_hook.id = response.data.id;
            approval.hooks.push(created_hook);
            this._update_approval(this.selected_transition, approval);
            this._update_transition(this.selected_transition);
            emit_success(`The approval hook is created`, this.alert_timeout);
          });
        }
      }
    },
    on_approval_hook_deleted(deleted_hook) {
      this.deletingApprovalHook = deleted_hook;
      this.deletingApprovalHookDialog = true;
    },
    delete_approval_hook() {
      if (this.selected_transition) {
        var approval = this.selected_transition.approvals.find(approval => approval.id == this.deletingApprovalHook.transition_approval_id);
        if (approval) {
          http.delete(`/approval-hook/delete/${this.deletingApprovalHook.id}`, response => {
            approval.hooks = approval.hooks.filter(hook => hook.id != this.deletingApprovalHook.id);
            this._update_approval(this.selected_transition, approval);
            this._update_transition(this.selected_transition);

            this.deletingApprovalHook = null;
            this.deletingApprovalHookDialog = true;

            emit_success(`The approval hook is deleted`, this.alert_timeout);
          });
        }
      }
    },
    on_transition_selected(transition_id) {
      this.selected_transition = this.transitions.find(transition => transition.id == transition_id);

      this._update_query({
        selected_transition_id: JSON.stringify(transition_id)
      });
    },
    get_state_by(id) {
      return this.states.find(state => state.id == id);
    },
    _update_transition(transition) {
      this.transitions = this.transitions.map(t => (t.id == transition.id ? transition : t));
    },
    _update_approval(transition, approval) {
      transition.approvals = transition.approvals.map(a => (a.id == approval.id ? approval : a));
    },
    _update_query(update) {
      var query = { ...this.$route.query, ...update };

      var that = this;
      if (Object.keys(query).some(queryKey => that.$route.query[queryKey] != query[queryKey])) {
        this.$router.push({ query });
      }
    }
  }
};
</script>