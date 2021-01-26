"""Parcello Integration"""

from .const import (
    DOMAIN,
    VERSION,
    ISSUE_URL,
    PLATFORM
)
import logging
from homeassistant.core import (
    callback
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config_entry):
    """ Disallow configuration via YAML """

    return True

async def async_setup_entry(hass, config):
    """Load the saved entities."""
    _LOGGER.info(
        "Version %s is starting, if you have any issues please report" " them here: %s",
        VERSION,
        ISSUE_URL,
    )
    config.options = config.data
    config.add_update_listener(update_listener)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config, PLATFORM)
    )

    return True


async def async_unload_entry(hass, config):
    """Handle removal of an entry."""
    try:
        await hass.config_entries.async_forward_entry_unload(config, PLATFORM)
        _LOGGER.info("Successfully removed sensor from the " + DOMAIN + " integration")
    except ValueError:
        pass
    return True


async def update_listener(hass, entry):
    """Update listener."""
    entry.data = entry.options
    await hass.config_entries.async_forward_entry_unload(entry, PLATFORM)
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, PLATFORM))