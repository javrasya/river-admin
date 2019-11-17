
import Vuetify from 'vuetify'
import Vue from 'vue'
import { auth, WORKFLOW, STATE, VIEW, FUNCTION } from "../../../src/helpers/auth"

import http from "../../../src/helpers/http"
import { shallowMount } from '@vue/test-utils'
import LoggedInLayout from '@/layouts/LoggedInLayout.vue'

describe('LoggedInLayout.vue', () => {
    let vuetify

    beforeEach(() => {
        vuetify = new Vuetify()
        Vue.use(Vuetify)
    })
    it('Should render workflow list on the left panel if the user is authorized', async () => {
        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation(
            (operation, object_type, callback) =>
                (Promise.resolve((operation == VIEW && object_type == WORKFLOW) ? callback(true) : callback(false)))
        )

        var workflows_spy = jest.spyOn(http, "get").mockImplementation(
            (url, callback) =>
                (Promise.resolve((url == "/user/get/") ? callback({ data: { username: "testuser" } }) : callback({ data: [] })))
        );


        const wrapper = shallowMount(LoggedInLayout, {
            vuetify,
            sync: false,
        })



        await wrapper.vm.$nextTick();


        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ id: "workflow-list", disabled: false }))

        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        workflows_spy.mockRestore()
    })

    it('Should render workflow list as disabled on the left panel if the user is not authorized', async () => {
        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation(
            (operation, object_type, callback) =>
                (Promise.resolve(callback(false)))
        )

        var workflows_spy = jest.spyOn(http, "get").mockImplementation(
            (url, callback) =>
                (Promise.resolve((url == "/user/get/") ? callback({ data: { username: "testuser" } }) : callback({ data: [] })))
        );


        const wrapper = shallowMount(LoggedInLayout, {
            vuetify,
            sync: false,
        })



        await wrapper.vm.$nextTick();


        expect(wrapper.vm.items).not.toContainEqual(expect.objectContaining({ id: "workflow-list", disabled: false }))

        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        workflows_spy.mockRestore()
    })

    it('Should render state list on the left panel if the user is authorized', async () => {
        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation(
            (operation, object_type, callback) =>
                (Promise.resolve((operation == VIEW && object_type == STATE) ? callback(true) : callback(false)))
        )

        var workflows_spy = jest.spyOn(http, "get").mockImplementation(
            (url, callback) =>
                (Promise.resolve((url == "/user/get/") ? callback({ data: { username: "testuser" } }) : callback({ data: [] })))
        );


        const wrapper = shallowMount(LoggedInLayout, {
            vuetify,
            sync: false,
        })



        await wrapper.vm.$nextTick();


        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ id: "state-list", disabled: false }))

        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        workflows_spy.mockRestore()
    })

    it('Should render state list as disabled on the left panel if the user is not authorized', async () => {
        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation(
            (operation, object_type, callback) =>
                (Promise.resolve(callback(false)))
        )

        var workflows_spy = jest.spyOn(http, "get").mockImplementation(
            (url, callback) =>
                (Promise.resolve((url == "/user/get/") ? callback({ data: { username: "testuser" } }) : callback({ data: [] })))
        );


        const wrapper = shallowMount(LoggedInLayout, {
            vuetify,
            sync: false,
        })



        await wrapper.vm.$nextTick();


        expect(wrapper.vm.items).not.toContainEqual(expect.objectContaining({ id: "state-list", disabled: false }))

        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        workflows_spy.mockRestore()
    })

    it('Should render function list on the left panel if the user is authorized', async () => {
        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation(
            (operation, object_type, callback) =>
                (Promise.resolve((operation == VIEW && object_type == FUNCTION) ? callback(true) : callback(false)))
        )

        var workflows_spy = jest.spyOn(http, "get").mockImplementation(
            (url, callback) =>
                (Promise.resolve((url == "/user/get/") ? callback({ data: { username: "testuser" } }) : callback({ data: [] })))
        );


        const wrapper = shallowMount(LoggedInLayout, {
            vuetify,
            sync: false,
        })



        await wrapper.vm.$nextTick();

        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ id: "function-list" }))

        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        workflows_spy.mockRestore()
    })

    it('Should render state list as disabled on the left panel if the user is not authorized', async () => {
        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation(
            (operation, object_type, callback) =>
                (Promise.resolve(callback(false)))
        )

        var workflows_spy = jest.spyOn(http, "get").mockImplementation(
            (url, callback) =>
                (Promise.resolve((url == "/user/get/") ? callback({ data: { username: "testuser" } }) : callback({ data: [] })))
        );


        const wrapper = shallowMount(LoggedInLayout, {
            vuetify,
            sync: false,
        })



        await wrapper.vm.$nextTick();


        expect(wrapper.vm.items).not.toContainEqual(expect.objectContaining({ id: "function-list", disabled: false }))

        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        workflows_spy.mockRestore()
    })

    it('Should render workflow object list on the left panel if the user is authorized', async () => {
        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation(
            (operation, object_type, callback) =>
                (Promise.resolve((operation == VIEW && object_type == WORKFLOW) ? callback(true) : callback(false)))
        )

        var workflows_spy = jest.spyOn(http, "get").mockImplementation(
            (url, callback) =>
                (Promise.resolve((url == "/user/get/") ? callback({ data: { username: "testuser" } }) :
                    ((url == "/workflow/metadata") ? callback({ data: [{ id: 1, name: "Transportation Flow", icon: "mdi-truck" }] })
                        : callback({ data: [] }))))
        );


        const wrapper = shallowMount(LoggedInLayout, {
            vuetify,
            sync: false,
        })



        await wrapper.vm.$nextTick();


        expect(wrapper.vm.workflow_items).toContainEqual(expect.objectContaining({ id: 1, title: "Transportation Flow" }))

        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        workflows_spy.mockRestore()
    })


    it('Should not render state list on the left panel if the user is not authorized', async () => {
        var has_permission_spy = jest.spyOn(auth, "_has_permission").mockImplementation(
            (operation, object_type, callback) =>
                (Promise.resolve(callback(false)))
        )

        var workflows_spy = jest.spyOn(http, "get").mockImplementation(
            (url, callback) =>
                (Promise.resolve((url == "/user/get/") ? callback({ data: { username: "testuser" } }) : callback({ data: [] })))
        );


        const wrapper = shallowMount(LoggedInLayout, {
            vuetify,
            sync: false,
        })



        await wrapper.vm.$nextTick();


        expect(wrapper.vm.workflow_items).not.toContainEqual(expect.objectContaining({ id: 1, title: "Transportation Flow" }))

        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        workflows_spy.mockRestore()
    })
})