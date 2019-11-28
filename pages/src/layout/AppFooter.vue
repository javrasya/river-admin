<template>
    <footer class="footer has-cards">
        <div class="container">
            <div class="row row-grid align-items-center my-md">
                <div class="col-lg-6">
                    <h3 class="text-primary font-weight-light mb-2">Thank you for supporting us!</h3>
                    <h4 class="mb-0 font-weight-light">You can be our sponsor to make River Admin better every day. Please contact us on any of these platforms</h4>
                </div>
                <div class="col-lg-6 text-lg-center btn-wrapper">
                    <a target="_blank" rel="noopener" href="mailto:ceahmetdal@gmail.com"
                       class="btn btn-neutral btn-icon-only btn-dribbble btn-lg btn-round" data-toggle="tooltip"
                       data-original-title="Mail us">
                        <i class="fa fa-envelope"></i>
                    </a>
                    <a target="_blank" rel="noopener" href="https://twitter.com/ceahmetdal"
                       class="btn btn-neutral btn-icon-only btn-twitter btn-round btn-lg" data-toggle="tooltip"
                       data-original-title="Follow us">
                        <i class="fa fa-twitter"></i>
                    </a>
                    <a target="_blank" rel="noopener" href="https://www.facebook.com/ceahmetdal"
                       class="btn btn-neutral btn-icon-only btn-facebook btn-round btn-lg" data-toggle="tooltip"
                       data-original-title="Like us">
                        <i class="fa fa-facebook-square"></i>
                    </a>
                    <a target="_blank" rel="noopener" href="https://github.com/javrasya"
                       class="btn btn-neutral btn-icon-only btn-github btn-round btn-lg" data-toggle="tooltip"
                       data-original-title="Star on Github">
                        <i class="fa fa-github"></i>
                    </a>
                </div>
            </div>
            <hr>
            <div class="row align-items-center justify-content-md-between">
                <div class="col-md-6">
                    <div class="copyright">
                        &copy; {{year}}
                        Ahmet Dal & <a href="https://github.com/javrasya/river-admin/blob/master/CONTRIBUTORS" target="_blank" rel="noopener">Contributors</a>
                    </div>
                </div>
                <div class="col-md-6">
                    <ul class="nav nav-footer justify-content-end">
                        <li class="nav-item">
                            <a href="https://github.com/javrasya/river-admin/blob/master/LICENSE"
                               class="nav-link" target="_blank" rel="noopener">New BSD License</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </footer>
</template>
<script>
export default {
  name: 'app-footer',
  data() {
    return {
      year: new Date().getFullYear()
    }
  }
};
</script>
<style>
</style>
