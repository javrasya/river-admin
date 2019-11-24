<template>
  <v-container>
    <v-card>
      <v-card-title class="approved" v-if="approval.status=='approved'">
        <span class="title font-weight-light">Approved by &nbsp;</span>
        <v-chip class="black--text">
          <v-icon left>mdi-account</v-icon>
          <span v-text="approval.transactioner.username"></span>
        </v-chip>
      </v-card-title>
      <v-card-title v-else>
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
        </v-speed-dial>
      </v-card-title>
      <v-card-text v-if="approval.status=='approved' && approval.hooks.length>0">
        <v-container fluid>
          <v-divider></v-divider>
          <div class="approved my-2" v-for="hook in approval.hooks" :key="hook.id">
            <HookDetail :hook="hook" :editable="editable" @on-delete="()=>on_hook_deleted(hook)" />
          </div>
        </v-container>
      </v-card-text>
      <v-card-text v-else-if="approval.status!='approved'">
        <v-row>
          <v-col>
            <v-row v-if="approval.permissions.length">
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
            <v-row v-if="approval.groups.length">
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
                    :editable="!hook.is_from_upstream() && editable"
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
        :transition_approval_meta_id="approval.transition_approval_meta"
        :transition_approval_id="approval.id"
        :object_id="object_id"
        :excluded_function_ids="approval.hooks.map(hook => hook.callback_function.id)"
        @on-create="on_hook_created"
      />
    </v-dialog>
  </v-container>
</template>

<script>
import { ObjectApproval } from "@/models/models";
import HookDetail from "@/components/HookDetail.vue";
import CreateApprovalHookForm from "@/components/CreateApprovalHookForm.vue";

export default {
  name: "ObjectApprovalDetail",
  components: {
    HookDetail,
    CreateApprovalHookForm
  },
  props: ["workflow", "approval", "object_id", "editable"],
  data: () => ({
    fab: false,
    newHookDialog: false
  }),
  methods: {
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


<style>
.approved {
  background-color: #4caf50;
  color: white;
}
</style>