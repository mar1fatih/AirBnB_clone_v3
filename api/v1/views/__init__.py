#!/usr/bin/python3
"""This module initializes the Blueprint for the v1 API."""

from flask import Blueprint

app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")

# Import views after the Blueprint object is created to avoid circular imports
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places_reviews import *
