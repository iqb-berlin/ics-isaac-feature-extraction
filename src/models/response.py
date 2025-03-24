# coding: utf-8

"""
    Coding-Service-API

    Coding-Service-API

    The version of the OpenAPI document: 0.0.2
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from pydantic import BaseModel, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from models.response_value import ResponseValue
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class Response(BaseModel):
    """
    Data structure produced by verona players
    """ # noqa: E501
    set_id: StrictStr = Field(description="Identifier of the set. Typically a user-id.", alias="setId")
    id: Annotated[str, Field(strict=True)] = Field(description="Identifier for the data source (variable)")
    status: StrictStr = Field(description="Status as stage in the workflow of creating and coding a variable's value")
    value: Optional[ResponseValue]
    subform: Optional[StrictStr] = Field(default=None, description="If variables i. e. data source ids are not unique in the unit, 'subform' can specify the sub object related to the specific variable.")
    code: Optional[StrictInt] = Field(default=None, description="Code representing the category of the value after coding process.")
    score: Optional[StrictInt] = Field(default=None, description="This value represents the result evaluation of the code after coding process.")
    __properties: ClassVar[List[str]] = ["setId", "id", "status", "value", "subform", "code", "score"]

    @field_validator('id')
    def id_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[0-9a-zA-Z_-]+$", value):
            raise ValueError(r"must validate the regular expression /^[0-9a-zA-Z_-]+$/")
        return value

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('UNSET', 'NOT_REACHED', 'DISPLAYED', 'PARTLY_DISPLAYED', 'VALUE_CHANGED', 'DERIVE_PENDING', 'DERIVE_ERROR', 'NO_CODING', 'INVALID', 'CODING_INCOMPLETE', 'CODING_ERROR', 'CODING_COMPLETE', 'INTENDED_INCOMPLETE'):
            raise ValueError("must be one of enum values ('UNSET', 'NOT_REACHED', 'DISPLAYED', 'PARTLY_DISPLAYED', 'VALUE_CHANGED', 'DERIVE_PENDING', 'DERIVE_ERROR', 'NO_CODING', 'INVALID', 'CODING_INCOMPLETE', 'CODING_ERROR', 'CODING_COMPLETE', 'INTENDED_INCOMPLETE')")
        return value

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": ()
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of Response from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of value
        if self.value:
            _dict['value'] = self.value.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of Response from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "setId": obj.get("setId"),
            "id": obj.get("id"),
            "status": obj.get("status"),
            "value": ResponseValue.from_dict(obj.get("value")) if obj.get("value") is not None else None,
            "subform": obj.get("subform"),
            "code": obj.get("code"),
            "score": obj.get("score")
        })
        return _obj


    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if "value" not in data:
            data["value"] = None
        return data
