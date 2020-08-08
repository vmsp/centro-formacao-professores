"""Reexports core Django functionality for easier access.

Usage:
>>> from visprof import core
>>> core.render_to_string('hello.html', {'name': 'Vitor'})
Hello, Vitor!
"""
# pylint: disable=unused-import
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
