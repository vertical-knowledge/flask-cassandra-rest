"""
Boring json which is just a basic
dump of the resource into json format.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo.adapters import AdapterBase

import json
import six

_CONTENT_TYPE = 'application/json'


class BasicJSONAdapter(AdapterBase):
    """
    Just a plain old JSON dump of the properties.
    Nothing exciting.

    Format:

    .. code-block:: javascript

        <resource_name>: {
            field1: "value"
            field2: "value"
            relationship: {
                relationship_field: "value"
            }
            list_relationship: [
                {
                    relationship_field: "value"
                }
                {
                    relationship_field: "value"
                }
            ]
        }
    """
    formats = ['json', _CONTENT_TYPE]
    extra_headers = {'Content-Type': _CONTENT_TYPE}

    @property
    def formatted_body(self):
        """
        Gets the formatted body of the response in unicode form.
        If ``self.status_code == 204`` then this will
        return an empty string.

        :return: The formatted body that should be returned.
            It's just a ``json.dumps`` of the properties and
            relationships
        :rtype: unicode
        """
        if self.status_code == 204:
            return ''
        response = dict()
        parent_properties = self.resource.properties.copy()
        self._append_relationships_to_list(response, self.resource.related_resources)
        self._append_relationships_to_list(response, self.resource.linked_resources)
        response.update(parent_properties)
        return json.dumps({self.resource.resource_name: response})

    @staticmethod
    def _append_relationships_to_list(rel_dict, relationships):
        """
        Dumps the relationship resources provided into
        a json ready list of dictionaries.  Side effect
        of updating the dictionary with the relationships

        :param dict rel_dict:
        :param list relationships:
        :return: A list of the resources in dictionary format.
        :rtype: list
        """
        for resource, name, embedded in relationships:
            if name not in rel_dict:
                rel_dict[name] = []
            if isinstance(resource, (list, tuple)):
                for res in resource:
                    rel_dict[name].append(res.properties)
                continue
            rel_dict[name].append(resource.properties)

    @classmethod
    def format_exception(cls, exc):
        """
        Takes an exception and appropriately formats
        the response.  By default it just returns a json dump
        of the status code and the exception message.
        Any exception that does not have a status_code attribute
        will have a status_code of 500.

        :param Exception exc: The exception to format.
        :return: A tuple containing: response body, format,
            http response code
        :rtype: tuple
        """
        status_code = getattr(exc, 'status_code', 500)
        body = json.dumps(dict(status=status_code, message=six.text_type(exc)))
        return body, cls.formats[0], status_code

    @classmethod
    def format_request(cls, request):
        """
        Simply returns request

        :param RequestContainer request: The request to handler
        :rtype: RequestContainer
        """
        return request
