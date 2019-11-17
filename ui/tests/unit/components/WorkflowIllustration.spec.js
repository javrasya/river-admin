import Vuetify from 'vuetify'
import Vue from 'vue'
import { mount } from '@vue/test-utils'
import { Workflow, State, Transition } from "../../../src/models/models"
import WorkflowIllustration from '@/components/WorkflowIllustration.vue'

describe('WorkflowIllustration.vue', () => {
    let vuetify

    beforeEach(() => {
        vuetify = new Vuetify()
        Vue.use(Vuetify)

        window.SVGElement.prototype.getBBox = () => ({
            x: Math.floor(Math.random() * Math.floor(100)),
            y: Math.floor(Math.random() * Math.floor(100)),
        });

    })

    afterEach(() => {
        delete window.SVGElement.prototype.getBBox;
    });

    it('should render even with one state', async () => {
        var state_1 = State.of(1, "state-1")
        var states = [state_1]
        const wrapper = mount_component({ states, transitions: [], editable: true, state_class_mapping: {} })
        expect(wrapper.find(`svg g#state_${state_1.id}`).exists()).toBeTruthy()
        expect(wrapper.find(`svg g#state_${state_1.id}`).classes()).toContainEqual("node-default")
        expect(wrapper.find(`svg g#state_${state_1.id} > rect`).exists()).toBeTruthy()
        expect(wrapper.find(`svg g#state_${state_1.id} > g.label tspan`).exists()).toBeTruthy()
        expect(wrapper.find(`svg g#state_${state_1.id} > g.label tspan`).text()).toBe(state_1.label)

        expect(wrapper.element).toMatchSnapshot()
    })

    it('should render with more than one state', async () => {
        var state_1 = State.of(1, "state-1")
        var state_2 = State.of(2, "state-2")
        var state_3 = State.of(3, "state-3")
        var states = [state_1, state_2, state_3]
        const wrapper = mount_component({ states, transitions: [], editable: true, state_class_mapping: {} })
        expect(wrapper.find(`svg g#state_${state_1.id}`).exists()).toBeTruthy()
        expect(wrapper.find(`svg g#state_${state_2.id}`).exists()).toBeTruthy()
        expect(wrapper.find(`svg g#state_${state_3.id}`).exists()).toBeTruthy()

        expect(wrapper.element).toMatchSnapshot()
    })


    it.skip('(library doesnt work in test)should render with one transition', async () => {
        var state_1 = State.of("1", "state-1")
        var state_2 = State.of("2", "state-2")
        var states = [state_1, state_2]

        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, state_1, "test_field");
        var transition_1 = Transition.of("1", workflow, state_1.id, state_2.id)
        var transitions = [transition_1]

        const wrapper = mount_component({ states, transitions, editable: true, state_class_mapping: {} })
        expect(wrapper.find(`svg g#state_${state_1.id}`).exists()).toBeTruthy()
        expect(wrapper.find(`svg g#state_${state_2.id}`).exists()).toBeTruthy()

        expect(wrapper.find(`svg g.edgePaths > g.edgePath > path.path`).exists()).toBeTruthy()

        expect(wrapper.element).toMatchSnapshot()
    })


    function mount_component(propsData) {
        return mount(WorkflowIllustration, {
            vuetify,
            sync: false,
            propsData,
        })
    }
})