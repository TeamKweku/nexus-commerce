import json
from typing import Any, Dict, Optional, Union

from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class GenericJSONRenderer(JSONRenderer):
    """
    Custom JSON renderer that wraps API responses in a consistent format.
    Extends DRF's JSONRenderer to provide standardized response structure.

    The rendered JSON will have the following structure:
    {
        "status_code": <http_status_code>,
        "<object_label>": <response_data>
    }

    Example:
        {
            "status_code": 200,
            "products": [{"id": 1, "name": "Product 1"}, ...]
        }

    Attributes:
        charset: Character encoding for JSON response
        object_label: Default label for the response data object,
                     can be overridden by setting object_label on views
    """

    charset: str = "utf-8"
    object_label: str = "object"

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> Union[bytes, str]:
        """
        Render the data into a consistent JSON format.

        This method wraps the response data in a standardized format unless
        errors are present in the data. For error responses, the original
        data is returned without wrapping.

        Args:
            data: The response data to be rendered
            accepted_media_type: The media type accepted by the client
            renderer_context: Additional context for rendering, must contain
                            'response' key with Response object

        Returns:
            JSON-encoded bytes or string containing the formatted response

        Raises:
            ValueError: If response object is not found in renderer_context
            TypeError: If json.dumps fails to serialize the data
        """
        # Initialize renderer context if None
        renderer_context = renderer_context or {}

        # Check if view has custom object label
        view: Any = renderer_context.get("view")
        object_label: str = (
            getattr(view, "object_label", None) or self.object_label
        )

        # Get response object from context
        response: Optional[Response] = renderer_context.get("response")
        if not response:
            raise ValueError(_("Response not found in renderer context"))

        # Extract status code from response
        status_code: int = response.status_code

        # Check for errors in response data
        errors: Optional[Any] = data.get("errors", None)

        # If errors exist, return data without wrapping
        if errors is not None:
            return super().render(data, accepted_media_type, renderer_context)

        # Wrap response data in standard format
        try:
            return json.dumps(
                {"status_code": status_code, object_label: data}
            ).encode(self.charset)
        except (TypeError, ValueError) as e:
            raise TypeError(f"Failed to serialize response data: {str(e)}")
