import json
from typing import Any, Optional, Union

from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer


class GenericJSONRenderer(JSONRenderer):
    """
    Custom JSON renderer that wraps API responses in a consistent format.
    Extends DRF's JSONRenderer to provide standardized response structure.

    The rendered JSON will have the following structure:
    {
        "status_code": <http_status_code>,
        "<object_label>": <response_data>
    }
    """

    # Define default character encoding for JSON response
    charset = "utf-8"

    # Default label for the response data object
    # Can be overridden by individual views
    object_label = "object"

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[dict] = None,
    ) -> Union[bytes, str]:
        """
        Render the data into a consistent JSON format.

        Args:
            data: The response data to be rendered
            accepted_media_type: The media type accepted by the client
            renderer_context: Additional context for rendering

        Returns:
            JSON-encoded bytes or string containing the formatted response

        Raises:
            ValueError: If response object is not found in renderer context
        """
        # Initialize renderer context if None
        if renderer_context is None:
            renderer_context = {}

        # Check if view has custom object label
        view = renderer_context.get("view")
        if hasattr(view, "object_label"):
            object_label = view.object_label
        else:
            object_label = self.object_label

        # Get response object from context
        response = renderer_context.get("response")
        if not response:
            raise ValueError(_("Response not found in renderer context"))

        # Extract status code from response
        status_code = response.status_code

        # Check for errors in response data
        errors = data.get("errors", None)

        # If errors exist, return data without wrapping
        if errors is not None:
            return super(GenericJSONRenderer, self).render(data)

        # Wrap response data in standard format
        return json.dumps(
            {"status_code": status_code, object_label: data}
        ).encode(self.charset)
