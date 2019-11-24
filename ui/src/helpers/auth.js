

import http from "@/helpers/http"

export const ADD = "add"
export const CHANGE = "change"
export const DELETE = "delete"
export const VIEW = "view"

export const WORKFLOW = "workflow"
export const STATE = "state"
export const FUNCTION = "function"
export const TRANSITION_META = "transitionmeta"
export const TRANSITION_APPROVAL_META = "transitionapprovalmeta"
export const TRANSITION_HOOK = "ontransithook"
export const APPROVAL_HOOK = "onapprovedhook"
export const TRANSITION = "transition"
export const TRANSITION_APPROVAL = "transitionapproval"



class Auth {

    _has_permission(operation, object_type, callback) {
        return http.get(`/user/has_river_permission/${operation}/${object_type}`, response => {
            if (response.data) {
                callback(true)
            } else {
                callback(false)
            }
        })
    }

    has_add_permission(object_type, callback) {
        return this._has_permission(ADD, object_type, callback)
    }

    has_change_permission(object_type, callback) {
        return this._has_permission(CHANGE, object_type, callback)
    }

    has_delete_permission(object_type, callback) {
        return this._has_permission(DELETE, object_type, callback)
    }

    has_view_permission(object_type, callback) {
        return this._has_permission(VIEW, object_type, callback)
    }
}

export var auth = new Auth();