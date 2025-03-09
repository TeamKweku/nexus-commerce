from typing import Any, List, Optional

from django.core import checks
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Model


class OrderField(models.PositiveIntegerField):
    """
    Custom field for handling ordering within a specific scope
    (unique_for_field).
    Automatically assigns the next available order number when not specified.

    This field ensures that order values are unique within a specified scope,
    defined by unique_for_field. When a new instance is created without an
    order value, it automatically assigns the next available number.

    Attributes:
        description: Human-readable field description
        unique_for_field: Name of the field that defines the uniqueness scope
    """

    description: str = "Ordering field on a unique field"

    def __init__(
        self, unique_for_field: Optional[str] = None, *args: Any, **kwargs: Any
    ) -> None:
        """
        Initialize the OrderField.

        Args:
            unique_for_field: Field name to scope the uniqueness of order values
            *args: Additional positional arguments for PositiveIntegerField
            **kwargs: Additional keyword arguments for PositiveIntegerField
        """
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs: Any) -> List[checks.Error]:
        """
        Perform field validation checks.

        Args:
            **kwargs: Additional validation parameters

        Returns:
            List of validation errors if any
        """
        return [
            *super().check(**kwargs),
            *self._check_for_field_attribute(**kwargs),
        ]

    def _check_for_field_attribute(self, **kwargs: Any) -> List[checks.Error]:
        """
        Validate the unique_for_field attribute.

        Args:
            **kwargs: Additional validation parameters

        Returns:
            List of validation errors if any
        """
        if self.unique_for_field is None:
            return [
                checks.Error(
                    "OrderField must define a 'unique_for_field' attribute"
                )
            ]
        elif self.unique_for_field not in [
            f.name for f in self.model._meta.get_fields()
        ]:
            return [
                checks.Error(
                    "OrderField entered does not match an existing model field"
                )
            ]
        return []

    def pre_save(self, model_instance: Model, add: bool) -> int:
        """
        Process the field value before saving.

        If no order value is set, automatically assigns the next available
        order number within the scope defined by unique_for_field.

        Args:
            model_instance: The model instance being saved
            add: Whether this is a new instance being created

        Returns:
            The order value to be saved
        """
        if getattr(model_instance, self.attname) is None:
            qs = self.model.objects.all()
            try:
                query = {
                    self.unique_for_field: getattr(
                        model_instance, self.unique_for_field
                    )
                }
                qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 1
            return value
        else:
            return super().pre_save(model_instance, add)
