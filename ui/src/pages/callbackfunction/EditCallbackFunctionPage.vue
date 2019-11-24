<template>
  <v-container fluid>
    <v-form ref="form" v-model="valid">
      <v-row justify="center" align="center">
        <v-col justify="center" align="center">
          <h1>
            <v-icon class="mb-2" style="font-size:35px">mdi-function-variant</v-icon>Edit Callback Function
          </h1>
        </v-col>
      </v-row>
      <v-row justify="center" align="center">
        <v-col>
          <v-row>
            <v-col>
              <v-text-field
                v-model="callback_function_name"
                label="Callback function name"
                prepend-icon="mdi-function-variant"
                :rules="functionNameRules"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <CodeEditor v-model="callback_function_body" />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <v-col justify="center" align="right">
          <v-btn large color="primary" @click="publish">
            <v-icon>mdi-content-save</v-icon>Update
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import CodeEditor from "@/components/CodeEditor.vue";
import { emit_success } from "@/helpers/event_bus";
import http from "@/helpers/http";

export default {
  name: "CreateCallbackFunctionPage",
  components: {
    CodeEditor
  },
  data: () => ({
    valid: true,
    callback_function_name: null,
    callback_function_body: null,
    functionNameRules: [v => !!v || "Function name is required", v => (v && v.length <= 200) || "Name must be less than 200 characters"]
  }),
  mounted() {
    var function_id = this.$route.params.id;
    http.get(`/function/get/${function_id}/`, response => {
      console.log(response);
      this.callback_function_name = response.data.name;
      this.callback_function_body = response.data.body;
    });
  },
  methods: {
    publish() {
      if (this.$refs.form.validate()) {
        var function_id = this.$route.params.id;
        http.put(
          `/function/update/${function_id}/`,
          {
            name: this.callback_function_name,
            body: this.callback_function_body
          },
          () => {
            emit_success(`Function '${this.callback_function_name}' is updated`);
            this.$router.push({ name: "list-callback-functions" });
          }
        );
      }
    }
  }
};
</script>