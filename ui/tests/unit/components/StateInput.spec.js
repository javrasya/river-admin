import Vuetify from 'vuetify'
import Vue from 'vue'
import { mount, shallowMount } from '@vue/test-utils'
import { auth } from "../../../src/helpers/auth"
import http from "../../../src/helpers/http"
import StateInput from '@/components/StateInput.vue'


describe('StateInput.vue', () => {
    let vuetify

    beforeEach(() => {
        vuetify = new Vuetify()
        Vue.use(Vuetify)
    })

    it('should not fetch states unless the typing starts', async () => {

        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation((operation, object_type, callback) => (Promise.resolve(callback())));

        const wrapper = mount(StateInput, {
            vuetify,
            sync: false
        })

        expect(wrapper.vm.items).toEqual([])
        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
    })

    it('should not show creating state option when user is not authorized', async () => {

        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation(() => (Promise.resolve()));
        var remote_states_spy = jest.spyOn(http, "get").mockImplementation((url, callback) => (Promise.resolve(callback(
            {
                data: [
                    { "id": 1, "label": "state-1" },
                    { "id": 2, "label": "state-2" }
                ]
            }
        ))));

        const wrapper = shallowMount(StateInput, {
            vuetify,
            sync: false,
            propsData: { value: null, placeholder: "Test state", disabled: false },
        })

        await wrapper.vm.$nextTick();

        wrapper.setData({ search: "sta" })

        await wrapper.vm.$nextTick();
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "id": 1, "label": "state-1" }))
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "id": 2, "label": "state-2" }))
        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        remote_states_spy.mockRestore()
    })

    it('should show creating state option when user is authorized', async () => {

        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation((operation, object_type, callback) => (Promise.resolve(callback())));
        var remote_states_spy = jest.spyOn(http, "get").mockImplementation((url, callback) => (Promise.resolve(callback(
            {
                data: [
                    { "id": 1, "label": "state-1" },
                    { "id": 2, "label": "state-2" }
                ]
            }
        ))));

        const wrapper = shallowMount(StateInput, {
            vuetify,
            sync: false,
            propsData: { value: null, placeholder: "Test state", disabled: false },
        })

        await wrapper.vm.$nextTick();

        wrapper.setData({ search: "sta" })

        await wrapper.vm.$nextTick();
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "id": 1, "label": "state-1" }))
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "id": 2, "label": "state-2" }))
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "final_label": "sta (Create)", "label": "sta" }))
        expect(wrapper.element).toMatchSnapshot()
        
        has_permission_spy.mockRestore()
        remote_states_spy.mockRestore()
    })

    it('should filter out those that doesnt match the search', async () => {

        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation((operation, object_type, callback) => (Promise.resolve(callback())));
        var remote_states_spy = jest.spyOn(http, "get").mockImplementation((url, callback) => (Promise.resolve(callback(
            {
                data: [
                    { "id": 1, "label": "Open" },
                    { "id": 2, "label": "In-Progress" }
                ]
            }
        ))));

        const wrapper = shallowMount(StateInput, {
            vuetify,
            sync: false,
            propsData: { value: null, placeholder: "Test state", disabled: false },
        })

        await wrapper.vm.$nextTick();

        wrapper.setData({ search: "Op" })

        await wrapper.vm.$nextTick();
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "id": 1, "label": "Open" }))
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "final_label": "Op (Create)", "label": "Op" }))
        expect(wrapper.element).toMatchSnapshot()
        
        has_permission_spy.mockRestore()
        remote_states_spy.mockRestore()
    })
})