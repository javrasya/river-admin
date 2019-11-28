
export class Workflow {
    constructor(id, content_type, initial_state, field_name) {
        this.id = id
        this.content_type = content_type
        this.initial_state = initial_state
        this.field_name = field_name
        this.identifier = `${this.content_type.app_label}.${this.content_type.model}.${this.field_name}`
    }

    static of(id, content_type, initial_state, field_name) {
        return new Workflow(id, content_type, initial_state, field_name)
    }

    static create(content_type, initial_state, field_name) {
        var id = '_' + Math.random().toString(36).substr(2, 9);
        return new Workflow(id, content_type, initial_state, field_name)
    }

    to_create_request() {
        return {
            content_type: this.content_type.id,
            field_name: this.field_name,
            initial_state: this.initial_state.id
        }
    }
}

export class Function {
    constructor(id, name, body) {
        this.id = id
        this.name = name
        this.body = body
    }

    static of(id, name, body) {
        return new Function(id, name, body)
    }
}

export class State {
    constructor(id, label, is_new) {
        this.id = id
        this.label = label
        this.is_new = is_new
    }

    of_description(description) {
        this.description = description;
        return this;
    }

    static of(id, label) {
        return new State(id, label, false)
    }

    static create(label) {
        var id = '_' + Math.random().toString(36).substr(2, 9);
        return new State(id, label, true)
    }

    to_create_request() {
        return {
            label: this.label
        }
    }
}

export class Transition {
    constructor(id, workflow, source_state_id, destination_state_id, is_new) {
        this.id = id
        this.workflow = workflow
        this.source_state_id = source_state_id
        this.destination_state_id = destination_state_id
        this.hooks = []
        this.is_new = is_new
    }

    static of(id, workflow, source_state_id, destination_state_id) {
        return new Transition(id, workflow, source_state_id, destination_state_id, false)
    }

    static create(workflow, source_state_id, destination_state_id) {
        var id = source_state_id + "+" + destination_state_id
        return new Transition(id, workflow, source_state_id, destination_state_id, true)
    }

    to_create_request() {
        return {
            workflow: this.workflow.id,
            source_state: this.source_state_id,
            destination_state: this.destination_state_id,
        }
    }
}

export class Approval {
    constructor(id, workflow, transition_id, permissions, groups, priority) {
        this.id = id
        this.workflow = workflow
        this.transition_id = transition_id
        this.permissions = permissions
        this.groups = groups || []
        this.priority = priority || []
        this.hooks = []
    }

    static of(id, workflow, transition_id, permissions, groups, priority) {
        return new Approval(id, workflow, transition_id, permissions, groups, priority)
    }

    static create(transition_id, workflow, permissions, groups, priority) {
        var id = '_' + Math.random().toString(36).substr(2, 9);
        return new Approval(id, workflow, transition_id, permissions, groups, priority)
    }

    to_create_request() {
        return {
            workflow: this.workflow.id,
            transition_meta: this.transition_id,
            source_state: this.source_state_id,
            destination_state: this.destination_state_id,
            permissions: this.permissions.map(permission => permission.id),
            groups: this.groups.map(group => group.id),
            priority: this.priority
        }
    }
}

export class TransitionHook {
    constructor(id, workflow, callback_function, transition_meta, transition, workflow_object_id, is_executed) {
        this.id = id
        this.workflow = workflow
        this.callback_function = callback_function
        this.workflow_object_id = workflow_object_id
        this.transition_meta = transition_meta
        this.transition = transition
        this.is_executed = is_executed
    }

    static of(id, workflow, callback_function, transition_meta_id, transition_id, workflow_object_id, is_executed) {
        return new TransitionHook(id, workflow, callback_function, transition_meta_id, transition_id, workflow_object_id, is_executed)
    }

    static create(workflow, callback_function, transition_meta_id, transition_id, workflow_object_id) {
        var id = '_' + Math.random().toString(36).substr(2, 9);
        return new TransitionHook(id, workflow, callback_function, transition_meta_id, transition_id, workflow_object_id, false)
    }

    is_from_upstream() {
        return this.workflow_object_id == null
    }

    to_create_request() {
        return {
            workflow: this.workflow.id,
            callback_function: this.callback_function.id,
            transition_meta: this.transition_meta || null,
            transition: this.transition || null,
            object_id: parseInt(this.workflow_object_id) || null,
            content_type: this.workflow_object_id ? this.workflow.content_type.id : null
        }
    }
}

export class ApprovalHook {
    constructor(id, workflow, callback_function, transition_approval_meta_id, transition_approval_id, workflow_object_id, is_executed) {
        this.id = id
        this.workflow = workflow
        this.transition_approval_meta_id = transition_approval_meta_id
        this.callback_function = callback_function
        this.workflow_object_id = workflow_object_id
        this.transition_approval_id = transition_approval_id
        this.is_executed = is_executed
    }

    static of(id, workflow, callback_function, transition_approval_meta_id, transition_approval_id, workflow_object_id, is_executed) {
        return new ApprovalHook(id, workflow, callback_function, transition_approval_meta_id, transition_approval_id, workflow_object_id, is_executed)
    }

    static create(workflow, callback_function, transition_approval_meta_id, transition_approval_id, workflow_object_id) {
        var id = '_' + Math.random().toString(36).substr(2, 9);
        return new ApprovalHook(id, workflow, callback_function, transition_approval_meta_id, transition_approval_id, workflow_object_id, false)
    }

    is_from_upstream() {
        return this.workflow_object_id == null
    }

    to_create_request() {
        return {
            workflow: this.workflow.id,
            callback_function: this.callback_function.id,
            transition_approval_meta: this.transition_approval_meta_id,
            transition_approval: this.transition_approval_id || null,
            object_id: parseInt(this.workflow_object_id) || null,
            content_type: this.workflow_object_id ? this.workflow.content_type.id : null
        }
    }
}

export class ObjectTransition {
    constructor(id, workflow, source_state_id, destination_state_id, transition_meta, object_id, iteration, is_cancelled, is_done) {
        this.id = id
        this.workflow = workflow
        this.transition_meta = transition_meta
        this.source_state_id = source_state_id
        this.destination_state_id = destination_state_id
        this.object_id = object_id
        this.iteration = iteration
        this.approvals = []
        this.hooks = []
        this.is_cancelled = is_cancelled
        this.is_done = is_done
    }

    static of(id, workflow, source_state_id, destination_state_id, transition_meta, object_id, iteration, is_cancelled, is_done) {
        return new ObjectTransition(id, workflow, source_state_id, destination_state_id, transition_meta, object_id, iteration, is_cancelled, is_done)
    }
}

export class ObjectApproval {
    constructor(id, workflow, transition_meta, transition_approval_meta, object_id, permissions, groups, priority, status, transactioner) {
        this.id = id
        this.workflow = workflow
        this.transition_meta = transition_meta
        this.transition_approval_meta = transition_approval_meta
        this.object_id = object_id
        this.permissions = permissions
        this.groups = groups
        this.priority = priority
        this.hooks = []
        this.status = status
        this.transactioner = transactioner
        this.is_approved = this.status == "approved"
    }

    static of(id, workflow, transition_meta, transition_approval_meta, object_id, permissions, groups, priority, status, transactioner) {
        return new ObjectApproval(id, workflow, transition_meta, transition_approval_meta, object_id, permissions, groups, priority, status, transactioner)
    }
}
