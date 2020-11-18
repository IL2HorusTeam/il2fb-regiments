from il2fb.commons.exceptions import IL2FBException

from ._utils import export


@export
class IL2FBRegimentException(IL2FBException):
  ...


@export
class IL2FBRegimentAttributeError(AttributeError, IL2FBException):
  ...


@export
class IL2FBRegimentLookupError(LookupError, IL2FBException):
  ...


@export
class IL2FBRegimentDataSourceNotFound(IL2FBRegimentLookupError):
  ...
