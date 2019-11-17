import VueRouter from 'vue-router'
import LoginPage from './pages/LoginPage'
import ListWorkflowPage from './pages/workflow/ListWorkflowPage'
import CreateWorkflowPage from './pages/workflow/CreateWorkflowPage'
import EditWorkflowPage from './pages/workflow/EditWorkflowPage'
import EditWorkflowRulesPage from './pages/workflow/EditWorkflowRulesPage'
import ListCallbackFunctionPage from './pages/callbackfunction/ListCallbackFunctionPage'
import CreateCallbackFunctionPage from './pages/callbackfunction/CreateCallbackFunctionPage'
import ViewCallbackFunctionPage from './pages/callbackfunction/ViewCallbackFunctionPage'
import EditCallbackFunctionPage from './pages/callbackfunction/EditCallbackFunctionPage'
import ListWorkflowObjectsPage from './pages/workflow_object/ListWorkflowObjectsPage'
import EditWorkflowObjectTimelinePage from './pages/workflow_object/EditWorkflowObjectTimelinePage'
import ListStatePage from './pages/state/ListStatePage'
import Vue from 'vue'
import store from './store.js'
import { auth, WORKFLOW } from './helpers/auth'
import { emit_error, emit_logout } from './helpers/event_bus'

store.commit('initialiseStore')

Vue.use(VueRouter);

var router = new VueRouter({
    routes: [
        {
            path: '/login',
            name: 'login',
            component: LoginPage,
            meta: {
                layout: "NotLoggedInLayout",
                allowGuest: true
            }
        },
        {
            path: '/',
            name: 'home',
            component: ListWorkflowPage,
        },
        {
            path: '/workflows',
            name: 'list-workflows',
            component: ListWorkflowPage,
        },
        {
            path: '/workflow/view/:id',
            name: 'view-workflow',
            component: EditWorkflowRulesPage,
            props: { readonly: true }
        },
        {
            path: '/workflows/create',
            name: 'create-workflow',
            component: CreateWorkflowPage,
        },
        {
            path: '/workflow/edit/:id',
            name: 'edit-workflow',
            component: EditWorkflowPage,
            props: { readonly: false }

        },
        {
            path: '/workflow/edit/rules/:id',
            name: 'edit-workflow-rules',
            component: EditWorkflowRulesPage,
            props: { readonly: false }

        },
        {
            path: '/callback-functions',
            name: 'list-callback-functions',
            component: ListCallbackFunctionPage,
        },
        {
            path: '/callback-functions/create',
            name: 'create-callback-function',
            component: CreateCallbackFunctionPage,
        },
        {
            path: '/callback-functions/view/:id',
            name: 'view-callback-function',
            component: ViewCallbackFunctionPage,
        },
        {
            path: '/callback-functions/edit/:id',
            name: 'edit-callback-function',
            component: EditCallbackFunctionPage,
        },
        {
            path: '/workflow-object/:workflow_id',
            name: 'list-workflow-objects',
            component: ListWorkflowObjectsPage,
        },
        {
            path: '/workflow-object/timeline/:workflow_id/:object_id',
            name: 'edit-workflow-object-timeline',
            component: EditWorkflowObjectTimelinePage,
        },
        {
            path: '/states',
            name: 'list-states',
            component: ListStatePage,
        },
    ]
});

router.beforeEach((to, from, next) => {
    var authToken = store.state.user.token;
    if (to.matched.some(record => record.meta.allowGuest)) {
        if (authToken != null && to.name == "login") {
            next({ name: "home" })
        } else {
            next()
        }
    }
    else if (authToken != null) {
        auth.has_view_permission(WORKFLOW, yes => {
            if (yes) {
                next()
            } else {
                emit_error(["You must have the permission to view the workflows!"], 10000);
                emit_logout()
            }
        })

    }
    else {
        next({
            name: 'login',
            params: { nextUrl: to.fullPath }
        })
    }

})

export default router;