# ---
# Default Configuration
# ---

# ---
# Flask
# ---
# This key MUST be changed before you make a site public, as it is used
# to sign the secure cookies used for sessions.
SECRET_KEY = 'ChangeMeOrGetHacked'

MAX_CONTENT_LENGTH = 8 * 1024 * 1024

try:
    from local_config import *
except ImportError:
    pass
