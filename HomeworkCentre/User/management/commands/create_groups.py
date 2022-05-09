from django.core.management import BaseCommand
from django.contrib.auth.models import Group , Permission
import logging

GROUPS = {
    "Students": {
        "homework solution" : ["add","delete","change","view"],
        "homework solution rating" : ["view"],
        "students class" : ["view"],
    },

    "Teachers": {
        "homework" : ["add","delete","change","view"],
        "homework solution" : ["view"],
        "homework solution rating" : ["view", "add"],
        "students class" : ["view", "add", "change", "delete"],
    },
}


class Command(BaseCommand):

    help = "Creates read only default permission groups for users"

    def handle(self, *args, **options):

        for group_name in GROUPS:

            new_group, created = Group.objects.get_or_create(name=group_name)

            for app_model in GROUPS[group_name]:

                for permission_name in GROUPS[group_name][app_model]:

                    name = "Can {} {}".format(permission_name, app_model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)
