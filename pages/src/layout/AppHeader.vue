<template>
  <header class="header-global">
    <base-nav class="navbar-main" transparent type effect="light" expand>
      <router-link slot="brand" class="navbar-brand mr-lg-5" to="/">
        <img src="img/brand/logo.png" alt="logo" />
      </router-link>

      <div class="row" slot="content-header" slot-scope="{closeMenu}">
        <div class="col-6 collapse-brand">
          <a href="/">
            River Admin
          </a>
        </div>
        <div class="col-6 collapse-close">
          <close-button @click="closeMenu"></close-button>
        </div>
      </div>

      <ul class="navbar-nav navbar-nav-hover align-items-lg-center">
        <base-dropdown class="nav-item" menu-classes="dropdown-menu-xl">
          <a slot="title" href="#" class="nav-link" data-toggle="dropdown" role="button">
            <i class="ni ni-ui-04 d-lg-none"></i>
            <span class="nav-link-inner--text">Examples</span>
          </a>
          <div class="dropdown-menu-inner">
            <a
              href="https://github.com/javrasya/river-admin#shipping-flow"
              class="media d-flex align-items-center"
            >
              <div class="icon icon-shape bg-gradient-primary rounded-circle text-white">
                <i class="fa fa-ship"></i>
              </div>
              <div class="media-body ml-3">
                <h6 class="heading text-primary mb-md-1">Shipping</h6>
                <p class="description d-none d-md-inline-block mb-0">
                  An example of a shipping workflow with River Admin
                </p>
              </div>
            </a>
            <a
              href="https://github.com/javrasya/river-admin#issue-tracking-flow"
              class="media d-flex align-items-center"
            >
              <div class="icon icon-shape bg-gradient-warning rounded-circle text-white">
                <i class="fa fa-ticket"></i>
              </div>
              <div class="media-body ml-3">
                <h5 class="heading text-warning mb-md-1">Issue Tracking</h5>
                <p class="description d-none d-md-inline-block mb-0">
                  A simple issue tracking workflow with River Admin
                </p>
              </div>
            </a>
          </div>
        </base-dropdown>

        <a
          href="https://github.com/javrasya/river-admin#live-demo"
          class="nav-link media d-flex align-items-center"
        >Live Demo</a>
      </ul>
      <ul class="navbar-nav align-items-lg-center ml-lg-auto">
        <li class="nav-item">
          <a
            class="nav-link nav-link-icon"
            href="mailto:ceahmetdal@gmail.com"
            target="_blank"
            rel="noopener"
            data-toggle="tooltip"
            title="Mail Us"
          >
            <i class="fa fa-envelope"></i>
            <span class="nav-link-inner--text d-lg-none">Mail</span>
          </a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link nav-link-icon"
            href="https://twitter.com/ceahmetdal"
            target="_blank"
            rel="noopener"
            data-toggle="tooltip"
            title="Follow us on Twitter"
          >
            <i class="fa fa-twitter-square"></i>
            <span class="nav-link-inner--text d-lg-none">Twitter</span>
          </a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link nav-link-icon"
            href="https://github.com/javrasya/river-admin"
            target="_blank"
            rel="noopener"
            data-toggle="tooltip"
            title="Star us on Github"
          >
            <i class="fa fa-github"></i>
            <span class="nav-link-inner--text d-lg-none">Github</span>
          </a>
        </li>
      </ul>
    </base-nav>
  </header>
</template>
<script>
import BaseNav from "@/components/BaseNav";
import BaseDropdown from "@/components/BaseDropdown";
import CloseButton from "@/components/CloseButton";

export default {
  components: {
    BaseNav,
    CloseButton,
    BaseDropdown
  }
};
</script>
<style>
</style>
