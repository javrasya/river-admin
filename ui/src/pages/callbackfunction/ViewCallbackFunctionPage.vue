<template>
  <v-container fluid v-if="callback_function">
    <v-row justify="center" align="center">
      <v-col justify="center" align="center">
        <h1>
          <v-icon class="mb-2" style="font-size:35px">mdi-function-variant</v-icon>Callback Function Detail
        </h1>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col>
        <v-row>
          <v-col cols="auto">
            <label>
              <h3>Name:</h3>
            </label>
          </v-col>
          <v-col>
            <v-chip color="primary" class="white--text">
              <v-icon left>mdi-function-variant</v-icon>
              <span v-text="callback_function.name"></span>
            </v-chip>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <CodeEditor v-model="callback_function.body" :read_only="true" />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CodeEditor from "../../components/CodeEditor";
import http from "../../helpers/http";

export default {
  name: "CreateCallbackFunctionPage",
  components: {
    CodeEditor
  },
  data: () => ({
    callback_function: null
  }),
  mounted() {
    var function_id = this.$route.params.id;
    http.get(`/function/get/${function_id}/`, response => (this.callback_function = response.data));
  },
  methods: {}
};
</script>