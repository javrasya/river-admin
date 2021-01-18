import random

from django.contrib.auth.models import Group, Permission

#custom user support patch
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from river.models import Workflow, State, Function

from examples.issue_tracker_example.management.commands.bootstrap_issue_tracker_example import IN_PROGRESS, RESOLVED, CLOSED as ISSUE_CLOSED, RE_OPENED
from examples.issue_tracker_example.models import Issue
from examples.shipping_example.management.commands.bootstrap_shipping_example import ARRIVED, SHIPPED, CLOSED as SHIPPING_CLOSED, RETURN_INITIALIZED, RETURNED, RE_INITIALIZED
from examples.shipping_example.models import Shipping


class Command(BaseCommand):
    help = 'Bootstrapping database with necessary items'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker("en_US")
        self.num_of_user_per_group = 4
        self.developers = []
        self.team_leaders = []
        self.testers = []
        self.warehouse_attendants = []
        self.delivery_persons = []
        self.courier_company_attendants = []
        self.finance_managers = []
        self.view_issue_permission = Permission.objects.get(codename="view_issue", content_type=ContentType.objects.get_for_model(Issue))
        self.view_shipping_permission = Permission.objects.get(codename="view_shipping", content_type=ContentType.objects.get_for_model(Shipping))
        self.view_workflow_permission = Permission.objects.get(codename="view_workflow", content_type=ContentType.objects.get_for_model(Workflow))

    def _new_user(self, *groups):
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        username = f"{first_name.lower()}.{last_name.lower()}"
        user = User.objects.filter(username=username).first() or User.objects.create_user(
            username=username,
            password="q1w2e3r4",
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )
        user.groups.set(groups)
        return user

    def _create_issue_tracking_users(self):
        developer = Group.objects.get(name="Developer")
        team_leader = Group.objects.get(name="Team Leader")
        tester = Group.objects.get(name="Tester")

        developer.permissions.set([self.view_issue_permission, self.view_workflow_permission])
        team_leader.permissions.set([self.view_issue_permission, self.view_workflow_permission])
        tester.permissions.set([self.view_issue_permission, self.view_workflow_permission])

        developer.user_set.filter(is_superuser=False).delete()
        team_leader.user_set.filter(is_superuser=False).delete()
        tester.user_set.filter(is_superuser=False).delete()

        self.developers = [self._new_user(developer) for _ in range(self.num_of_user_per_group)]
        self.team_leaders = [self._new_user(team_leader) for _ in range(self.num_of_user_per_group)]
        self.testers = [self._new_user(tester) for _ in range(self.num_of_user_per_group)]

    def _create_shipping_users(self):
        warehouse_attendant = Group.objects.get(name="Warehouse Attendant")
        delivery_person = Group.objects.get(name="Delivery Person")
        courier_company_attendant = Group.objects.get(name="Courier Company Attendant")
        finance_manager = Group.objects.get(name="Finance Person")

        warehouse_attendant.permissions.set([self.view_shipping_permission, self.view_workflow_permission])
        delivery_person.permissions.set([self.view_shipping_permission, self.view_workflow_permission])
        courier_company_attendant.permissions.set([self.view_shipping_permission, self.view_workflow_permission])
        finance_manager.permissions.set([self.view_shipping_permission, self.view_workflow_permission])

        warehouse_attendant.user_set.filter(is_superuser=False).delete()
        delivery_person.user_set.filter(is_superuser=False).delete()
        courier_company_attendant.user_set.filter(is_superuser=False).delete()
        finance_manager.user_set.filter(is_superuser=False).delete()

        self.warehouse_attendants = [self._new_user(warehouse_attendant) for _ in range(self.num_of_user_per_group)]
        self.delivery_persons = [self._new_user(delivery_person) for _ in range(self.num_of_user_per_group)]
        self.courier_company_attendants = [self._new_user(courier_company_attendant) for _ in range(self.num_of_user_per_group)]
        self.finance_managers = [self._new_user(finance_manager) for _ in range(self.num_of_user_per_group)]

    def _create_issues(self):
        in_progress = State.objects.get(label=IN_PROGRESS)
        resolved = State.objects.get(label=RESOLVED)
        closed = State.objects.get(label=ISSUE_CLOSED)
        re_opened = State.objects.get(label=RE_OPENED)

        Issue.objects.all().delete()
        Issue.river.issue_status.workflow.transitions.all().delete()
        Issue.river.issue_status.workflow.transition_approvals.all().delete()

        issue_1 = Issue.objects.create(title="Fix button look on the home page", reporter=random.choice(self.testers), assignee=random.choice(self.developers))
        issue_2 = Issue.objects.create(title="Send an email after a user signs up", reporter=random.choice(self.testers), assignee=random.choice(self.developers))
        issue_3 = Issue.objects.create(title="Log DB connection errors", reporter=random.choice(self.developers), assignee=random.choice(self.developers))
        issue_4 = Issue.objects.create(title="Investigate poor response times", reporter=random.choice(self.team_leaders), assignee=random.choice(self.developers))
        issue_5 = Issue.objects.create(title="Speed up user login", reporter=random.choice(self.testers), assignee=random.choice(self.developers))
        issue_6 = Issue.objects.create(title="Login component doesn't look good on small screens", reporter=random.choice(self.testers), assignee=random.choice(self.developers))

        ####
        issue_1.river.issue_status.approve(issue_1.assignee, next_state=in_progress)
        issue_1.river.issue_status.approve(issue_1.assignee, next_state=resolved)

        issue_1.river.issue_status.approve(random.choice(self.team_leaders), next_state=re_opened)

        issue_1.river.issue_status.approve(issue_1.assignee, next_state=in_progress)

        ####
        issue_2.river.issue_status.approve(issue_2.assignee, next_state=in_progress)

        ####
        issue_3.river.issue_status.approve(issue_3.assignee, next_state=in_progress)
        issue_3.river.issue_status.approve(issue_3.assignee, next_state=resolved)

        issue_3.river.issue_status.approve(random.choice(self.team_leaders), next_state=closed)

        ####
        issue_4.river.issue_status.approve(issue_4.assignee, next_state=in_progress)
        issue_4.river.issue_status.approve(issue_4.assignee, next_state=resolved)

        issue_4.river.issue_status.approve(random.choice(self.team_leaders), next_state=closed)

        issue_4.river.issue_status.approve(random.choice(self.testers), next_state=closed)

        ####
        issue_6.river.issue_status.approve(issue_6.assignee, next_state=in_progress)
        issue_6.river.issue_status.approve(issue_6.assignee, next_state=resolved)

        issue_6.river.issue_status.approve(random.choice(self.team_leaders), next_state=re_opened)

        issue_6.river.issue_status.approve(issue_6.assignee, next_state=in_progress)
        issue_6.river.issue_status.approve(issue_6.assignee, next_state=resolved)

        issue_6.river.issue_status.approve(random.choice(self.testers), next_state=re_opened)

        issue_6.river.issue_status.approve(issue_6.assignee, next_state=in_progress)
        issue_6.river.issue_status.approve(issue_6.assignee, next_state=resolved)

        issue_6.river.issue_status.approve(random.choice(self.team_leaders), next_state=closed)

        issue_6.river.issue_status.approve(random.choice(self.testers), next_state=closed)

    def _create_shippings(self):
        shipped = State.objects.get(label=SHIPPED)
        arrived = State.objects.get(label=ARRIVED)
        closed = State.objects.get(label=SHIPPING_CLOSED)
        return_initialized = State.objects.get(label=RETURN_INITIALIZED)
        returned = State.objects.get(label=RETURNED)
        re_initialized = State.objects.get(label=RE_INITIALIZED)

        Shipping.objects.all().delete()
        Shipping.river.shipping_status.workflow.transitions.all().delete()
        Shipping.river.shipping_status.workflow.transition_approvals.all().delete()
        shipping_1 = Shipping.objects.create(product="APPLE MacBook Pro (2019) 15.4` Laptop - Silver", customer="Hannah Dodd")
        shipping_2 = Shipping.objects.create(product="APPLE IPHONE 11 - 64GB - BLACK", customer="Alister Marks")
        shipping_3 = Shipping.objects.create(product="Catan (Settlers of Catan) - English", customer="Olaf Dorsey")
        shipping_4 = Shipping.objects.create(product="SAMSUNG Galaxy Note10 - 256GB - Aura Black", customer="Martyn Lutz")
        shipping_5 = Shipping.objects.create(product="Nike Air Max 90", customer="Zainab Nixon")
        shipping_6 = Shipping.objects.create(product="Bose Noise Canceling Headphones 700", customer="Amaya Avery")
        shipping_7 = Shipping.objects.create(product="Huawei Watch GT 2 46mm - Black", customer="Sahil Snyder")
        shipping_8 = Shipping.objects.create(product="SAMSUNG Galaxy S10e - Black", customer="Edison Berry")

        ####
        shipping_1.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=shipped)
        shipping_1.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=shipped)

        ####
        shipping_2.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=shipped)
        shipping_2.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=shipped)

        shipping_2.river.shipping_status.approve(random.choice(self.delivery_persons), next_state=arrived)
        shipping_2.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=arrived)

        shipping_2.river.shipping_status.approve(random.choice(self.finance_managers), next_state=closed)

        ####
        shipping_4.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=shipped)
        shipping_4.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=shipped)

        shipping_4.river.shipping_status.approve(random.choice(self.delivery_persons), next_state=arrived)

        ####
        shipping_5.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=shipped)
        shipping_5.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=shipped)

        shipping_5.river.shipping_status.approve(random.choice(self.delivery_persons), next_state=arrived)
        shipping_5.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=arrived)

        shipping_5.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=return_initialized)

        shipping_5.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=returned)

        ####
        shipping_6.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=shipped)
        shipping_6.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=shipped)

        shipping_6.river.shipping_status.approve(random.choice(self.delivery_persons), next_state=arrived)
        shipping_6.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=arrived)

        shipping_6.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=return_initialized)

        shipping_6.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=returned)

        shipping_6.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=re_initialized)

        shipping_6.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=shipped)

        ####
        shipping_7.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=shipped)
        shipping_7.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=shipped)

        shipping_7.river.shipping_status.approve(random.choice(self.delivery_persons), next_state=arrived)
        shipping_7.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=arrived)

        shipping_7.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=return_initialized)

        shipping_7.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=returned)

        shipping_7.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=re_initialized)

        shipping_7.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=shipped)
        shipping_7.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=shipped)

        shipping_7.river.shipping_status.approve(random.choice(self.delivery_persons), next_state=arrived)
        shipping_7.river.shipping_status.approve(random.choice(self.courier_company_attendants), next_state=arrived)

        shipping_7.river.shipping_status.approve(random.choice(self.finance_managers), next_state=closed)

        ####
        shipping_8.river.shipping_status.approve(random.choice(self.warehouse_attendants), next_state=shipped)

    @transaction.atomic()
    def handle(self, *args, **options):
        view_state_permission = Permission.objects.get(codename="view_state", content_type=ContentType.objects.get_for_model(State))
        view_function_permission = Permission.objects.get(codename="view_function", content_type=ContentType.objects.get_for_model(Function))

        demo_user = User.objects.filter(username="demo").first() or User.objects.create_user(username="demo", password="demo", is_staff=True)
        demo_user.user_permissions.set([
            self.view_workflow_permission,
            self.view_issue_permission,
            self.view_shipping_permission,
            view_state_permission,
            view_function_permission
        ])

        self._create_issue_tracking_users()
        self._create_shipping_users()

        self._create_issues()
        self._create_shippings()

        self.stdout.write(self.style.SUCCESS('Successfully bootstrapped the db '))
