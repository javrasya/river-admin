<template>
  <div>
    <v-container fluid v-if="initialized">
      <v-row>
        <v-col justify="center" align="center">
          <h1>
            Workflow for
            <v-chip>{{ workflow.identifier }}</v-chip>
          </h1>
        </v-col>
      </v-row>
      <v-row>
        <v-flex xs12 sm12 md6>
          <v-container>
            <WorkflowIllustration
              :states="states"
              :transitions="transitions"
              :editable="true"
              @on-transition-selected="on_transition_selected"
            />
          </v-container>
        </v-flex>
        <v-flex xs12 sm12 md6>
          <v-container v-if="selected_transition">
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
                      <v-col v-if="!readonly">
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

                          <v-tooltip top>
                            <template v-slot:activator="{ on }">
                              <v-btn
                                fab
                                dark
                                small
                                v-on="on"
                                color="green"
                                @click="newApprovalDialog=true"
                              >
                                <v-icon>mdi-account-multiple-check</v-icon>
                              </v-btn>
                            </template>
                            <span>Create Approval Step</span>
                          </v-tooltip>
                        </v-speed-dial>
                      </v-col>
                    </v-row>
                  </v-card-title>
                  <v-card-text>
                    <ApprovalList
                      :workflow="workflow"
                      :approvals="selected_transition.approvals"
                      :editable="!readonly"
                      @on-delete="on_approval_deleted"
                      @on-order-change="on_approvals_order_change"
                      @on-hook-create="on_approval_hook_created"
                      @on-hook-delete="on_approval_hook_deleted"
                    />
                    <div v-if="selected_transition.hooks.length>0">
                      <v-divider />
                      <span class="title font-weight-light">Right before the transition happens</span>
                      <div v-for="(hook,index) in selected_transition.hooks" :key="hook.id">
                        <HookDetail
                          :hook="hook"
                          :editable="!readonly"
                          @on-delete="on_transition_hook_deleted"
                        />
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
          <v-container v-else-if="!readonly">
            <EmptyState
              label="Select a transition"
              description="Selecting a transition by clicking the arrow, you'll be able to create the rules."
            >
              <template v-slot:icon>mdi-mouse</template>
            </EmptyState>
          </v-container>
        </v-flex>
      </v-row>
    </v-container>
    <v-dialog v-model="newApprovalDialog" max-width="800" v-if="!readonly && selected_transition">
      <CreateApprovalForm
        :workflow="workflow"
        :transition_id="selected_transition.id"
        @on-create="on_approval_created"
      />
    </v-dialog>
    <v-dialog
      v-model="newTransitionHookDialog"
      max-width="800"
      v-if="!readonly && selected_transition"
    >
      <CreateTransitionHookForm
        :workflow="workflow"
        :transition_meta="selected_transition.id"
        :excluded_function_ids="selected_transition.hooks.map(hook => hook.callback_function.id)"
        @on-create="on_transition_hook_created"
      />
    </v-dialog>
  </div>
</template>

<script>
import EmptyState from "@/components/EmptyState.vue";
import CreateApprovalForm from "@/components/CreateApprovalForm.vue";
import CreateTransitionHookForm from "@/components/CreateTransitionHookForm.vue";
import HookDetail from "@/components/HookDetail.vue";
import WorkflowIllustration from "@/components/WorkflowIllustration.vue";
import ApprovalList from "@/components/ApprovalList.vue";
import { emit_success } from "@/helpers/event_bus";
import http from "@/helpers/http";
import { Workflow, Approval, Transition, State, TransitionHook, ApprovalHook } from "@/models/models";

export default {
  name: "EditWorkflowRulesPage",
  components: {
    EmptyState,
    CreateApprovalForm,
    CreateTransitionHookForm,
    WorkflowIllustration,
    ApprovalList,
    HookDetail
  },
  props: ["readonly"],
  data: () => ({
    newApprovalDialog: false,
    newTransitionHookDialog: false,
    fab: false,
    workflow: null,
    initialized: false,
    selected_transition: null,
    states: [],
    transitions: [],
    alert_timeout: 2000
  }),
  mounted() {
    var workflow_id = this.$route.params.id;
    this.workflow = http.get(`/workflow/get/${workflow_id}/`, response => {
      this.workflow = Workflow.of(response.data.id, response.data.content_type, response.data.initial_state, response.data.field_name);

      var state_fetcher = this.get_states(workflow_id).then(states => (this.states = states));
      var transitions_meta_fetcher = this.get_transition_metas(workflow_id).then(transitions => (this.transitions = transitions));

      Promise.all([state_fetcher, transitions_meta_fetcher]).then(() => {
        var selected_transition_id = this.$route.query.selected_transition_id;
        if (selected_transition_id) {
          this.on_transition_selected(selected_transition_id);
        }
        this.initialized = true;
      });
    });
  },
  methods: {
    get_states(workflow_id) {
      return http.get(`/workflow/state/list/${workflow_id}/`, response => {
        return response.data.map(state => State.of(state.id, state.label).of_description(state.description));
      });
    },

    get_transition_metas(workflow_id) {
      var that = this;
      return http.get(`/workflow/transition-meta/list/${workflow_id}/`, response => {
        return Promise.all(
          response.data.map(transition_meta => {
            var transition = Transition.of(transition_meta.id, this.workflow, transition_meta.source_state, transition_meta.destination_state);

            var transition_approval_metas_fetcher = that.get_transition_approval_metas(transition.id).then(transition_approval_metas => {
              transition.approvals = transition_approval_metas;
            });

            var transition_hooks_fetcher = that.get_transition_hooks(transition.id).then(transition_hooks => {
              transition.hooks = transition_hooks;
            });

            return Promise.all([transition_approval_metas_fetcher, transition_hooks_fetcher]).then(() => transition);
          })
        );
      });
    },

    get_transition_hooks(transition_id) {
      return http.get(`/transition-meta/transition-hook/list/${transition_id}/`, response => {
        return response.data.map(transition_hook =>
          TransitionHook.of(
            transition_hook.id,
            this.workflow,
            transition_hook.callback_function,
            transition_hook.transition_meta,
            transition_hook.transition,
            transition_hook.object_id,
            false
          )
        );
      });
    },

    get_transition_approval_metas(transition_id) {
      var that = this;
      return http.get(`/transition-meta/transition-approval-meta/list/${transition_id}/`, response => {
        return Promise.all(
          response.data.map(transition_approval_meta => {
            var approval = Approval.of(
              transition_approval_meta.id,
              this.workflow,
              transition_approval_meta.transition,
              transition_approval_meta.permissions,
              transition_approval_meta.groups
            );

            return that
              .get_transition_approval_hooks(approval.id)
              .then(transition_approval_hooks => {
                approval.hooks = transition_approval_hooks;
              })
              .then(() => approval);
          })
        );
      });
    },
    get_transition_approval_hooks(transition_approval_meta_id) {
      return http.get(`/transition-approval-meta/approval-hook/list/${transition_approval_meta_id}/`, response => {
        return response.data.map(transition_approval_hook =>
          ApprovalHook.of(
            transition_approval_hook.id,
            this.workflow,
            transition_approval_hook.callback_function,
            transition_approval_hook.transition_approval_meta,
            transition_approval_hook.transition_approval,
            transition_approval_hook.object_id,
            false
          )
        );
      });
    },

    on_approval_created(created_approval) {
      if (this.selected_transition) {
        var max_priority = this.selected_transition.approvals.reduce((max, approval) => Math.max(max, approval.priority), 0);
        created_approval.priority = max_priority + 1;
        http.post("/transition-approval-meta/create/", created_approval.to_create_request(), response => {
          created_approval.id = response.data.id;
          this.selected_transition.approvals.push(created_approval);
          this._update_transition(this.selected_transition);
          this.newApprovalDialog = false;
          emit_success(`The transition approval meta is created`, this.alert_timeout);
        });
      }
    },
    on_approval_deleted(deleted_approval) {
      if (this.selected_transition) {
        http.delete(`/transition-approval-meta/delete/${deleted_approval.id}/`, response => {
          this.selected_transition.approvals = this.selected_transition.approvals.filter(approval => approval.id != deleted_approval.id);
          this._update_transition(this.selected_transition);
          emit_success(`The transition approval meta is deleted`, this.alert_timeout);
        });
      }
    },
    on_approvals_order_change(newApprovals) {
      http
        .post(
          `/transition-approval-meta/re-prioritize/`,
          newApprovals.map(new_aproval => ({ transition_approval_meta_id: new_aproval.id, priority: new_aproval.priority }))
        )
        .then(response => {
          this.selected_transition.approvals = newApprovals;
          this._update_transition(this.selected_transition);
          emit_success(`Re-prioritization has been applied`, this.alert_timeout);
        });
    },
    on_transition_hook_created(created_hook) {
      if (this.selected_transition && !this.selected_transition.hooks.find(hook => hook.id == created_hook.id)) {
        http.post("/transition-hook/create/", created_hook.to_create_request(), response => {
          created_hook.id = response.data.id;
          this.selected_transition.hooks.push(created_hook);
          this._update_transition(this.selected_transition);
          this.newTransitionHookDialog = false;
          emit_success(`The transition hook is created`, this.alert_timeout);
        });
      }
    },
    on_transition_hook_deleted(deleted_hook) {
      if (this.selected_transition) {
        http.delete(`/transition-hook/delete/${deleted_hook.id}/`, response => {
          this.selected_transition.hooks = this.selected_transition.hooks.filter(hook => hook.id != deleted_hook.id);
          this._update_transition(this.selected_transition);
          emit_success(`The transition hook is deleted`, this.alert_timeout);
        });
      }
    },
    on_approval_hook_created(created_hook) {
      if (this.selected_transition) {
        var approval = this.selected_transition.approvals.find(approval => approval.id == created_hook.transition_approval_meta_id);
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
      if (this.selected_transition) {
        var approval = this.selected_transition.approvals.find(approval => approval.id == deleted_hook.transition_approval_meta_id);
        if (approval) {
          http.delete(`/approval-hook/delete/${deleted_hook.id}/`, response => {
            approval.hooks = approval.hooks.filter(hook => hook.id != deleted_hook.id);
            this._update_approval(this.selected_transition, approval);
            this._update_transition(this.selected_transition);
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
      // this._repriotise_approvals(transition);
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
    },
    _repriotise_approvals(transition) {
      var that = this;
      transition.approvals = transition.approvals
        .sort((a1, a2) => a1.priority - a2.priority)
        .map((approval, index) => {
          var newApproval = { ...approval, priority: index + 1 };
          return newApproval;
        });
    }
  }
};
</script>



<style>
.fab_container {
  position: fixed;
  bottom: 45px;
  right: 30px;
  z-index: 10;
}
</style>