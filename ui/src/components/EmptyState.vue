<template>
  <v-container fluid>
    <v-row justify="center" align="center">
      <v-flex xs12 sm6 md4>
        <v-row justify="center" align="center">
          <v-icon style="font-size:150px">
            <slot name="icon"></slot>
          </v-icon>
        </v-row>
        <v-row v-if="label" justify="center" align="center">
          <v-col justify="center" align="center">
            <p class="subtitle-1">{{ label }}</p>
          </v-col>
        </v-row>
        <v-row v-if="description" justify="center" align="center">
          <v-col justify="center" align="center">
            <p class="subtitle-3">{{ description }}</p>
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-col justify="center" align="center">
            <slot name="content"></slot>
          </v-col>
        </v-row>
      </v-flex>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "EmptyState",
  props: ["label", "description"]
};
</script>