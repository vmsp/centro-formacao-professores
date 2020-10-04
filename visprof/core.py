"""Reexports core Django functionality for easier access.

Usage:
>>> from visprof import core
>>> core.render_to_string('hello.html', {'name': 'Vitor'})
Hello, Vitor!
"""
# pylint: disable=unused-import
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
