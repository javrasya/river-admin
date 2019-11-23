<template>
  <v-container fluid class="py-4">
    <v-row v-if="object_approvals.length ==0">
      <v-col>No approval step</v-col>
    </v-row>
    <v-row v-else>
      <v-col>
        <div v-for="(element) in items" :key="element.priority">
          <ObjectApprovalDetail
            :workflow="workflow"
            :object_id="object_id"
            :approval="element"
            :editable="editable"
            @on-hook-create="(hook)=>on_hook_created(hook)"
            @on-hook-delete="(hook)=>on_hook_deleted(hook)"
          />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ObjectApproval } from "../models/models";
import ObjectApprovalDetail from "./ObjectApprovalDetail";
import HookDetail from "./HookDetail";
import http from "../helpers/http";

export default {
  name: "ObjectApprovalList",
  components: {
    ObjectApprovalDetail,
    HookDetail
  },
  props: ["workflow", "object_id", "object_approvals", "editable"],
  data: () => ({
    drag: false,
    items: []
  }),
  computed: {},
  watch: {
    object_approvals(val) {
      if (val != this.items) {
        this.update_items();
      }
    }
  },
  mounted() {
    this.update_items();
  },
  methods: {
    update_items() {
      this.items = this.object_approvals.map((approval, index) => ({
        ...approval,
        priority: index + 1
      }));
    },
    on_hook_created(hook) {
      this.$emit("on-hook-create", hook);
    },
    on_hook_deleted(hook) {
      this.$emit("on-hook-delete", hook);
    }
  }
};
</script>

<style>
.list-group {
  width: 100%;
}
</style>