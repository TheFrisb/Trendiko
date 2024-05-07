"""Monkey-patch for django>5.0 for `nested_admin`.

In Django>=5.0 was removed module `django.utils.topological_sort`
(see https://github.com/django/django/commit/1282b5e4207440af659ef0e0e0c486fdfba8e7b7)
And this module is used by `django-nested-admin` to backport media ordering
for old Django versions:
https://github.com/theatlantic/django-nested-admin/blob/master/nested_admin/compat.py

While proper fix is not added to `django-nested-admin`, this monkey patch may
be used to make `nested-admin` work with Django 5.0.

More info: https://github.com/theatlantic/django-nested-admin/issues/244

"""
import sys
import types


def mock(*args, **kwargs):
    raise NotImplementedError("This is just mock and not actual implementation")


dynamic_module = types.ModuleType("dynamic_topological_sort")
dynamic_module.CyclicDependencyError = mock
dynamic_module.stable_topological_sort = mock

sys.modules.setdefault("django.utils.topological_sort", dynamic_module)
