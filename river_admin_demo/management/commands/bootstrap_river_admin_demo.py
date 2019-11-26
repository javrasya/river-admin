from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction
from river.models import Workflow

from river_admin_issue_tracker_example.models import Issue
from river_admin_shipping_example.models import Shipping


class Command(BaseCommand):
    help = 'Bootstrapping database with necessary items'

    def _create_issue_tracking_users(self):
        view_issue_permission = Permission.objects.get(codename="view_issue", content_type=ContentType.objects.get_for_model(Issue))
        view_workflow_permission = Permission.objects.get(codename="view_workflow", content_type=ContentType.objects.get_for_model(Workflow))

        developer = Group.objects.get(name="Developer")
        team_leader = Group.objects.get(name="Team Leader")
        tester = Group.objects.get(name="Tester")

        developer.permissions.set([view_issue_permission, view_workflow_permission])
        team_leader.permissions.set([view_issue_permission, view_workflow_permission])
        tester.permissions.set([view_issue_permission, view_workflow_permission])

        developer_1 = User.objects.filter(username="developer_1").first() or User.objects.create_user(
            "developer_1",
            password="q1w2e3r4",
            first_name="Sonya",
            last_name="Evans",
            is_staff=True
        )

        developer_2 = User.objects.filter(username="developer_2").first() or User.objects.create_user(
            "developer_2",
            password="q1w2e3r4",
            first_name="June",
            last_name="Newton",
            is_staff=True
        )

        developer_1.groups.set([developer])
        developer_2.groups.set([developer])

        team_leader_1 = User.objects.filter(username="team_leader_1").first() or User.objects.create_user(
            "team_leader_1",
            password="q1w2e3r4",
            first_name="Gustavo",
            last_name="Mathis",
            is_staff=True
        )

        team_leader_2 = User.objects.filter(username="team_leader_1").first() or User.objects.create_user(
            "team_leader_2",
            password="q1w2e3r4",
            first_name="Luther",
            last_name="Howell",
            is_staff=True
        )

        team_leader_1.groups.set([team_leader])
        team_leader_2.groups.set([team_leader])

        tester_1 = User.objects.filter(username="tester_1").first() or User.objects.create_user(
            "tester_1",
            password="q1w2e3r4",
            first_name="Ellen",
            last_name="Williamson",
            is_staff=True
        )

        tester_2 = User.objects.filter(username="tester_2").first() or User.objects.create_user(
            "tester_2",
            password="q1w2e3r4",
            first_name="Harvey",
            last_name="Dawson",
            is_staff=True
        )
        tester_1.groups.set([tester])
        tester_2.groups.set([tester])

    def _create_shipping_users(self):
        view_shipping_permission = Permission.objects.get(codename="view_shipping", content_type=ContentType.objects.get_for_model(Shipping))
        view_workflow_permission = Permission.objects.get(codename="view_workflow", content_type=ContentType.objects.get_for_model(Workflow))

        warehouse_attendant = Group.objects.get(name="Warehouse Attendant")
        delivery_person = Group.objects.get(name="Delivery Person")
        courier_company = Group.objects.get(name="Courier Company")
        finance_manager = Group.objects.get(name="Finance Person")

        warehouse_attendant.permissions.set([view_shipping_permission, view_workflow_permission])
        delivery_person.permissions.set([view_shipping_permission, view_workflow_permission])
        courier_company.permissions.set([view_shipping_permission, view_workflow_permission])
        finance_manager.permissions.set([view_shipping_permission, view_workflow_permission])

        warehouse_attendant_1 = User.objects.filter(username="warehouse_attendant_1").first() or User.objects.create_user(
            "warehouse_attendant_1",
            password="q1w2e3r4",
            first_name="Sabrina",
            last_name="Stevens",
            is_staff=True
        )
        warehouse_attendant_1.groups.set([warehouse_attendant])

        delivery_person_1 = User.objects.filter(username="delivery_person_1").first() or User.objects.create_user(
            "delivery_person_1",
            password="q1w2e3r4",
            first_name="Ricky",
            last_name="Soto",
            is_staff=True
        )
        delivery_person_1.groups.set([delivery_person])

        courier_company_attendant_1 = User.objects.filter(username="courier_company_attendant_1").first() or User.objects.create_user(
            "courier_company_attendant_1",
            password="q1w2e3r4",
            first_name="Lena",
            last_name="Stanley",
            is_staff=True
        )

        courier_company_attendant_1.groups.set([courier_company])

        courier_company_attendant_2 = User.objects.filter(username="courier_company_attendant_2").first() or User.objects.create_user(
            "courier_company_attendant_2",
            password="q1w2e3r4",
            first_name="Bennie",
            last_name="Cobb",
            is_staff=True
        )
        courier_company_attendant_2.groups.set([courier_company])

        finance_manager_1 = User.objects.filter(username="finance_manager_1").first() or User.objects.create_user(
            "finance_manager_1",
            password="q1w2e3r4",
            first_name="Ann",
            last_name="Johnson",
            is_staff=True
        )

        finance_manager_1.groups.set([finance_manager])

    def _create_shippings(self):
        shipping_1 = Shipping.objects.get_or_create(product="APPLE MacBook Pro (2019) 15.4` Laptop - Silver", customer="Hannah Dodd")
        shipping_2 = Shipping.objects.get_or_create(product="APPLE IPHONE 11 - 64GB - BLACK", customer="Alister Marks")
        shipping_3 = Shipping.objects.get_or_create(product="Catan (Settlers of Catan) - English", customer="Olaf Dorsey")
        shipping_4 = Shipping.objects.get_or_create(product="SAMSUNG Galaxy Note10 - 256GB - Aura Black", customer="Martyn Lutz")
        shipping_5 = Shipping.objects.get_or_create(product="Nike Air Max 90", customer="Zainab Nixon")
        shipping_6 = Shipping.objects.get_or_create(product="Bose Noise Canceling Headphones 700", customer="Amaya Avery")
        shipping_7 = Shipping.objects.get_or_create(product="Huawei Watch GT 2 46mm - Black", customer="Sahil Snyder")
        shipping_8 = Shipping.objects.get_or_create(product="SAMSUNG Galaxy S10e - Black", customer="Edison Berry")

    @transaction.atomic()
    def handle(self, *args, **options):
        self._create_issue_tracking_users()
        self._create_shipping_users()

        self._create_shippings()

        self.stdout.write(self.style.SUCCESS('Successfully bootstrapped the db '))
