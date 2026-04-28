
import yaml
import os
from voluptuous import Schema, Required, All, Any, Optional, ALLOW_EXTRA, MultipleInvalid

# Define the config schema
config_schema = Schema({
    Required('nzbgeek'): {
        Required('api_key'): str,
        Required('url'): str,
    },
    Required('sabnzbd'): {
        Required('api_key'): str,
        Required('url'): str,
        Optional('test_mode'): bool,
    },
    Required('filters'): {
        Optional('quality'): [str],
    },
    Optional('searches'): [str],
    Optional('jellyfin'): dict,
    Optional('postprocess'): dict,
    Optional('notify'): dict,
}, extra=ALLOW_EXTRA)

def validate_config(config: dict) -> dict:
    """
    Validate the loaded config against the schema.
    Raises voluptuous.MultipleInvalid if validation fails.
    Returns the validated config.
    """
    return config_schema(config)

def load_config(config_path=None):
    """
    Load and validate the YAML config file.
    Raises voluptuous.MultipleInvalid if validation fails.
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return validate_config(config)
