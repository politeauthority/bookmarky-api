"""
    Bookmarky Migrate
    Data - Options

"""
import logging

from bookmarky.api.models.option import Option
# from bookmarky.api.utils import glow


class DataOptions:

    def create(self) -> bool:
        """Create the Options."""
        self.create_primary()
        return True

    def create_primary(self) -> bool:
        self.make_option("test-option", "str", "test-value")
        return True

    def make_option(self, option_name, option_type: str, option_value=None, ) -> bool:
        """Create an Option."""
        opt = Option()
        opt.name = option_name
        if opt.get_by_name():
            logging.debug("Option %s already exists, skipping." % option_name)
            return True
        opt.type = option_type
        opt.acl_write = ["write-all"]
        opt.acl_read = ["read-all"]
        if option_value:
            opt.value = option_value
        if not opt.save():
            logging.error("Could not create option: %s" % option_name)
            return False
        logging.debug("Saved option: %s" % option_name)
        return True


# End File: bookmarky/src/bookmarky/migrations/data/data_options.py
