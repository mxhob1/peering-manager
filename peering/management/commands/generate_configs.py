import logging

from django.core.management.base import BaseCommand
from django.template.defaultfilters import pluralize

from peering.models import Router


class Command(BaseCommand):
    help = "Export configuration for routers."
    logger = logging.getLogger("peering.manager.peering")

    def handle(self, *args, **options):
        configured = []
        self.logger.info("Generating configurations...")

        for router in Router.objects.all():
            # Configuration can be applied only if there is a template and the router
            # is running on a supported platform
            if router.configuration_template and router.platform:
                self.logger.info("Generating {}".format(router.hostname))
                # Generate configuration and export if something has changed
                configuration = router.generate_configuration()
                print(configuration)
                if not error and changes:
                    router.set_napalm_configuration(configuration, commit=True)
                    configured.append(router)
            else:
                self.logger.info(
                    "Ignoring {}, no configuration to apply".format(router.hostname)
                )

        if configured:
            self.logger.info(
                "Configurations exported for {} router{}".format(
                    len(configured), pluralize(len(configured))
                )
            )
        else:
            self.logger.info("No configuration changes to apply")
