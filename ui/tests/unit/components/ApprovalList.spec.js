import Vuetify from 'vuetify'
import Vue from 'vue'
import { mount } from '@vue/test-utils'
import { Workflow, State, Approval } from "@/models/models"
import ApprovalDetail from '@/components/ApprovalDetail.vue'
import ApprovalList from '@/components/ApprovalList.vue'

describe('ApprovalList.vue', () => {
    let vuetify

    beforeEach(() => {
        vuetify = new Vuetify()
        Vue.use(Vuetify)
    })

    it('should not render any approval when the list is empty', async () => {
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");

        const wrapper = mount(ApprovalList, {
            vuetify,
            sync: false,
            propsData: { workflow, approvals: [], editable: true }
        })
        await wrapper.vm.$nextTick();
        expect(wrapper.findAll(ApprovalDetail)).toHaveLength(0)
        expect(wrapper.find("div.container div.col").text()).toBe("No approval step")
        expect(wrapper.element).toMatchSnapshot()
    })


    it('should render approvals when the list is with one item', async () => {
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");

        var transition_id = "transition-1"
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount(ApprovalList, {
            vuetify,
            sync: false,
            propsData: { workflow, approvals: [approval], editable: true },
        })
        await wrapper.vm.$nextTick();
        expect(wrapper.findAll(ApprovalDetail)).toHaveLength(1)
        expect(wrapper.text()).not.toContain("No approval step")
        expect(wrapper.element).toMatchSnapshot()
    })

    it('should render approvals when the list is with more than one item', async () => {
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");

        var transition_id = "transition-1"
        var approval_1 = Approval.of("approval-1", workflow, transition_id, [], [], 0)
        var approval_2 = Approval.of("approval-2", workflow, transition_id, [], [], 1)
        var approval_3 = Approval.of("approval-3", workflow, transition_id, [], [], 2)

        const wrapper = mount(ApprovalList, {
            vuetify,
            sync: false,
            propsData: { workflow, approvals: [approval_1, approval_2, approval_3], editable: true },
        })
        await wrapper.vm.$nextTick();
        expect(wrapper.findAll(ApprovalDetail)).toHaveLength(3)
        expect(wrapper.text()).not.toContain("No approval step")
        expect(wrapper.element).toMatchSnapshot()
    })

    it('should emit event on order of the approvals change', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval_1 = Approval.of("approval-1", workflow, transition_id, [], [], 0)
        var approval_2 = Approval.of("approval-2", workflow, transition_id, [], [], 1)
        var approval_3 = Approval.of("approval-3", workflow, transition_id, [], [], 2)

        const wrapper = mount(ApprovalList, {
            vuetify,
            sync: false,
            propsData: { workflow, approvals: [approval_1, approval_2, approval_3], editable: false }
        })


        var re_prioritized_approvals = [approval_3, approval_1, approval_2]
        wrapper.setData({ items: re_prioritized_approvals })
        wrapper.vm.on_move()
        expect(wrapper.emitted('on-order-change')).toHaveLength(1)


        approval_3.priority = 1
        approval_1.priority = 2
        approval_2.priority = 3
        var expected_re_prioritized_approvals = [approval_3, approval_1, approval_2]
        var new_approvals = wrapper.emitted('on-order-change').map(args => args[0])

        expect(new_approvals).toContainEqual(expected_re_prioritized_approvals)
        expect(wrapper.element).toMatchSnapshot()
    })

    it('should update interanal items when approvals are updated', async () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval_1 = Approval.of("approval-1", workflow, transition_id, [], [], 0)
        var approval_2 = Approval.of("approval-2", workflow, transition_id, [], [], 1)

        var approvals = [approval_1, approval_2];
        const wrapper = mount(ApprovalList, {
            vuetify,
            sync: false,
            propsData: { workflow, approvals, editable: false }
        })
        expect(wrapper.vm.items).toHaveLength(2)

        var approval_3 = Approval.of("approval-3", workflow, transition_id, [], [], 2)
        var new_approvals = [approval_1, approval_2, approval_3];

        wrapper.setProps({ approvals: new_approvals })
        await wrapper.vm.$nextTick();

        expect(wrapper.vm.items).toHaveLength(3)
        expect(wrapper.element).toMatchSnapshot()
    })
})
