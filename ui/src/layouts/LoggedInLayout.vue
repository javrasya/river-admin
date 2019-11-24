<template>
  <v-app id="inspire" v-if="initialized">
    <v-app-bar @click.stop="mini = true" app clipped-right color="blue" dark>
      <v-toolbar-title :style="{ cursor: 'pointer'}" @click="goToHomePage">
        <v-row justify="center" align="center">
          <v-col>
            <img class="mt-2 toolbar-logo" src="@/assets/logo.svg" />
          </v-col>
          <v-col>
            <span class="app-title">River Admin</span>
          </v-col>
        </v-row>
      </v-toolbar-title>
      <div class="flex-grow-1"></div>

      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-icon class="mr-2" v-on="on">mdi-account</v-icon>
        </template>
        <span>{{ user_profile.username }}</span>
      </v-tooltip>
      <v-btn icon @click="logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-content>
      <v-container align="start" justify="start" class="pa-0" fluid>
        <v-row no-gutters align="start" justify="start">
          <v-col xl="auto" lg="auto" md="auto" sm="auto" xs="auto">
            <div :class="mini?'mini-drawer-shadow':'drawer-shadow'" />
            <v-navigation-drawer
              v-model="drawer"
              :mini-variant="mini"
              permanent
              fixed
              class="drawer"
            >
              <v-list-item jusitfy="center" align="center">
                <v-list-item-title>Menu</v-list-item-title>
              </v-list-item>

              <v-divider />

              <v-list dense>
                <v-list-item
                  :disabled="item.disabled"
                  :id="item.id"
                  v-for="item in items"
                  :key="item.title"
                  @click="goTo(item)"
                  link
                >
                  <v-list-item-icon>
                    <v-icon :disabled="item.disabled">{{ item.icon }}</v-icon>
                  </v-list-item-icon>

                  <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>

              <v-divider />

              <v-list dense>
                <v-list-item
                  :id="item.id"
                  v-for="item in workflow_items"
                  :key="item.title"
                  @click="goTo(item)"
                  link
                >
                  <v-list-item-icon>
                    <v-icon>{{ item.icon }}</v-icon>
                  </v-list-item-icon>

                  <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
              <v-divider />

              <v-divider />
              <v-row>
                <div class="flex-grow-1"></div>
                <v-col>
                  <v-btn icon @click.stop="mini = !mini">
                    <v-icon v-if="mini">mdi-chevron-double-right</v-icon>
                    <v-icon v-else>mdi-chevron-double-left</v-icon>
                  </v-btn>
                </v-col>
                <div class="flex-grow-1"></div>
              </v-row>
            </v-navigation-drawer>
          </v-col>
          <v-col>
            <slot></slot>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { emit_logout } from "@/helpers/event_bus";
import { auth, WORKFLOW, FUNCTION, STATE } from "@/helpers/auth";
import http from "@/helpers/http";

export default {
  name: "LoggedInLayout",
  data: () => ({
    initialized: false,
    drawer: false,
    mini: true,
    items: [],
    workflow_items: [],
    user_profile: null,
    raw_items: [
      { id: "workflow-list", title: "Workflows", icon: "mdi-file-tree", name: "list-workflows", authorization_object_type: WORKFLOW },
      { id: "state-list", title: "States", icon: "mdi-label-variant-outline", name: "list-states", authorization_object_type: STATE },
      { id: "function-list", title: "Functions", icon: "mdi-function-variant", name: "list-callback-functions", authorization_object_type: FUNCTION }
    ]
  }),
  mounted() {
    if (!this.initialized) {
      var user_profile_fetcher = http.get("/user/get/", response => {
        this.user_profile = response.data;
      });

      var workflow_fetchers = auth.has_view_permission(WORKFLOW, yes => {
        if (yes) {
          return http.get("/workflow/metadata", response => {
            this.workflow_items = response.data.map(workflow_metadata => ({
              id: workflow_metadata.id,
              title: workflow_metadata.name,
              icon: workflow_metadata.icon,
              name: "list-workflow-objects",
              params: { workflow_id: workflow_metadata.id }
            }));
          });
        }
      });

      Promise.all(
        this.raw_items
          .map((raw_item, index) => {
            if (raw_item.authorization_object_type) {
              return auth.has_view_permission(raw_item.authorization_object_type, yes => {
                this.items.push({ id: raw_item.id, title: raw_item.title, icon: raw_item.icon, name: raw_item.name, index, disabled: !yes });
              });
            }
          })
          .concat([user_profile_fetcher, workflow_fetchers])
      ).then(() => {
        this.items = this.items.sort((i1, i2) => i1.index - i2.index);
        this.initialized = true;
      });
    }
  },
  methods: {
    logout() {
      emit_logout();
    },
    goToHomePage() {
      this.$router.push({ name: "home" });
    },
    goTo(item) {
      this.$router.push({ name: item.name, params: item.params || {} });
    }
  }
};
</script>

<style>
.toolbar-logo {
  width: 45px;
}

.drawer {
  top: 65px !important;
}

.drawer-shadow {
  width: 250px !important;
}

.mini-drawer-shadow {
  width: 80px;
}

.app-title {
  font-weight: bolder;
}
</style>