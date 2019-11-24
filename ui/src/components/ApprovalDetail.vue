<template>
  <v-container>
    <v-card>
      <v-card-title>
        <v-icon class="column-drag-handle mb-1 mr-3" v-if="editable">mdi-menu</v-icon>
        <v-icon class="mb-1 mr-3">mdi-account-multiple-check</v-icon>
        <span class="title font-weight-light">Should be approved by the users who</span>
        <div class="flex-grow-1" />

        <v-speed-dial
          v-if="editable"
          class="mt-5"
          v-model="fab"
          :bottom="true"
          :right="true"
          direction="left"
          :open-on-hover="true"
        >
          <template v-slot:activator>
            <v-btn v-model="fab" small color="primary" dark fab>
              <v-icon v-if="fab">mdi-close</v-icon>
              <v-icon v-else>mdi-settings</v-icon>
            </v-btn>
          </template>

          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-btn fab dark small v-on="on" color="green" @click="newHookDialog=true">
                <v-icon>mdi-function-variant</v-icon>
              </v-btn>
            </template>
            <span>Create Approval Hook</span>
          </v-tooltip>

          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-btn fab dark small v-on="on" color="warning" @click="delete_approval()">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <span>Delete Approval Step</span>
          </v-tooltip>
        </v-speed-dial>
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col>
            <v-row class="permissions-lane" v-if="approval.permissions.length>0">
              <v-col cols="4">
                <label>have permissions:</label>
              </v-col>
              <v-col>
                <span v-bind:key="permission.id" v-for="(permission,index) in approval.permissions">
                  <v-chip color="primary" class="white--text">
                    <v-icon left>mdi-lock</v-icon>
                    <span v-text="permission.identifier"></span>
                  </v-chip>
                  <span v-if="index != approval.permissions.length-1">or</span>
                </span>
              </v-col>
            </v-row>
            <v-row class="groups-lane" v-if="approval.groups.length>0">
              <v-col cols="4">
                <label>are in groups:</label>
              </v-col>
              <v-col>
                <span v-bind:key="group.id" v-for="(group,index) in approval.groups">
                  <v-chip color="primary" class="white--text">
                    <v-icon left>mdi-account-multiple</v-icon>
                    <span v-text="group.name"></span>
                  </v-chip>
                  <span v-if="index != approval.groups.length-1">or</span>
                </span>
              </v-col>
            </v-row>
            <v-row>
              <v-container v-if="approval.hooks.length>0" fluid>
                <v-divider></v-divider>
                <span class="title font-weight-light">Right after this is approved</span>
                <div class="my-2" v-for="hook in approval.hooks" :key="hook.id">
                  <HookDetail
                    :hook="hook"
                    :editable="editable"
                    @on-delete="()=>on_hook_deleted(hook)"
                  />
                </div>
              </v-container>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-dialog v-model="newHookDialog" max-width="800">
      <CreateApprovalHookForm
        :workflow="workflow"
        :transition_approval_meta_id="approval.id"
        :excluded_function_ids="approval.hooks.map(hook => hook.callback_function.id)"
        @on-create="on_hook_created"
      />
    </v-dialog>
  </v-container>
</template>

<script>
import { Approval } from "@/models/models";
import HookDetail from "@/components/HookDetail.vue";
import CreateApprovalHookForm from "@/components/CreateApprovalHookForm.vue";

export default {
  name: "ApprovalDetail",
  components: {
    HookDetail,
    CreateApprovalHookForm
  },
  props: ["workflow", "approval", "editable"],
  data: () => ({
    fab: false,
    newHookDialog: false
  }),
  methods: {
    delete_approval() {
      this.$emit("on-delete", this.approval);
    },
    on_hook_created(created_hook) {
      this.$emit("on-hook-create", created_hook);
      this.newHookDialog = false;
    },
    on_hook_deleted(deleted_hook) {
      this.$emit("on-hook-delete", deleted_hook);
    }
  }
};
</script>
