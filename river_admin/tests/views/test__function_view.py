from django.test import TestCase
from hamcrest import equal_to, assert_that, has_entry, has_length, has_item, all_of, not_none, is_, none
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
from river.models import Function


class FunctionViewTest(TestCase):

    def test__shouldReturnNotFoundWhenAnInexistentFunctionIsRequested(self):
        response = self.client.get('/function/get/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldReturnFunction(self):
        function = Function.objects.create(name="test-function", body="function-body")
        response = self.client.get('/function/get/%d/' % function.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(function.id)))
        assert_that(response.data, has_entry("name", equal_to(function.name)))
        assert_that(response.data, has_entry("body", equal_to(function.body)))

    def test__shouldReturnEmptyListWhenThereIsNoStates(self):
        response = self.client.get('/function/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfStates(self):
        function_1 = Function.objects.create(name="test-function-1", body="function-body")
        function_2 = Function.objects.create(name="test-function-2", body="function-body")

        response = self.client.get('/function/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(function_1.id)),
                    has_entry("name", equal_to(function_1.name)),
                    has_entry("body", equal_to(function_1.body))
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(function_2.id)),
                    has_entry("name", equal_to(function_2.name)),
                    has_entry("body", equal_to(function_2.body))
                )
            )
        )

    def test__shouldNotCreateFunctionWhenNameIsMissing(self):
        response = self.client.post('/function/create/', data={"body": "function-body"})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldNotCreateFunctionWhenBodyIsMissing(self):
        response = self.client.post('/function/create/', data={"name": "test-function"})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldCreateFunction(self):
        response = self.client.post('/function/create/', data={"name": "test-function", "body": "function-body"})
        created_function = Function.objects.first()
        assert_that(created_function, not_none())
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(created_function.pk)))

    def test__shouldNotCreateFunctionWhenNameIsDuplicate(self):
        function = Function.objects.create(name="test-function", body="function-body")
        response = self.client.post('/function/create/', data={"name": function.name, "body": "test-body"})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldReturnNotFoundWhenAnInexistentFunctionIsRequestedToDelete(self):
        response = self.client.delete('/function/delete/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldDeleteState(self):
        function = Function.objects.create(name="test-function", body="function-body")
        response = self.client.delete('/function/delete/%d/' % function.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(Function.objects.filter(name=function.name).first(), is_(none()))
