<template>
  <v-card>
    <v-card-title :class="hook.is_executed?'executed':(!editable?'not-editable':'')">
      <v-icon class="mb-1 mr-3">mdi-function-variant</v-icon>
      <span v-if="hook.is_executed" class="title font-weight-light">
        Executed function
        <v-chip class="black--text">{{ hook.callback_function.name }}</v-chip>
      </span>

      <span v-else class="title font-weight-light">
        Execute function
        <v-chip color="primary" class="white--text">{{ hook.callback_function.name }}</v-chip>
      </span>
      <div class="flex-grow-1" />
      <v-btn v-if="editable && !hook.is_executed" text icon color="warning" @click="deleteStep()">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-card-title>
  </v-card>
</template>


<script>
export default {
  name: "HookDetail",
  props: ["hook", "editable"],
  methods: {
    deleteStep() {
      this.$emit("on-delete", this.hook);
    }
  }
};
</script>

<style>
.executed {
  background-color: #4caf5069;
}

.not-editable {
  background-color: aliceblue;
}
</style>