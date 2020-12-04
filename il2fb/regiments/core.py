import sys

if sys.version_info >= (3, 9):
  from collections.abc import Callable

  Dict = dict
  List = list

else:
  from typing import Callable
  from typing import Dict
  from typing import List

from pathlib import Path

from typing import Any
from typing import Optional

from verboselib import get_language

from il2fb.commons.air_forces import AirForceConstant
from il2fb.commons.air_forces import AIR_FORCES

from il2fb.commons.supported_languages import SUPPORTED_LANGUAGES

from .exceptions import IL2FBRegimentAttributeError
from .exceptions import IL2FBRegimentDataSourceNotFound
from .exceptions import IL2FBRegimentLookupError

from ._utils import export


__here__ = Path(__file__).absolute().parent


DEFAULT_LANGUAGE_NAME = SUPPORTED_LANGUAGES.get_default().name

DEFAULT_DATA_DIR_PATH = __here__ / "data"
DEFAULT_DATA_MISSING_VALUE = None
DEFAULT_DATA_FILE_ENCODING = "cp1251"
DEFAULT_VALUE_ENCODING = "unicode-escape"

DEFAULT_CATALOG_FILE_NAME = "regiments.ini"

DEFAULT_NAMES_FILE_NAME_FORMAT        = "regShort_{language}.properties"
DEFAULT_DESCRIPTIONS_FILE_NAME_FORMAT = "regInfo_{language}.properties"

DEFAULT_REGIMENTS_IDS = frozenset(AIR_FORCES.get_default_regiment_ids())


@export
class RegimentInfoLoader:

  def __init__(
    self,
    data_dir_path: Path=DEFAULT_DATA_DIR_PATH,
    data_file_encoding: str=DEFAULT_DATA_FILE_ENCODING,
    data_value_encoding: str=DEFAULT_VALUE_ENCODING,
    data_missing_value: str=DEFAULT_DATA_MISSING_VALUE,
    names_file_name_format: str=DEFAULT_NAMES_FILE_NAME_FORMAT,
    descriptions_file_name_format: str=DEFAULT_DESCRIPTIONS_FILE_NAME_FORMAT,
  ):
    self._data_dir_path = data_dir_path
    self._data_file_encoding = data_file_encoding
    self._data_value_encoding = data_value_encoding
    self._data_missing_value = data_missing_value
    self._names_file_name_format = names_file_name_format
    self._descriptions_file_name_format = descriptions_file_name_format

  def get_name(self, regiment_id: str, language: Any) -> str:
    return self._get_value(regiment_id, self._names_file_name_format, language)

  def get_description(self, regiment_id: str, language: Any) -> str:
    return self._get_value(regiment_id, self._descriptions_file_name_format, language)

  def _get_value(self, regiment_id: str, file_name_format: str, language: Any) -> str:
    language  = language and language.lower()
    file_name = file_name_format.format(language=language)
    file_path = self._data_dir_path / file_name
    try:
      return self._load_value_or_raise(regiment_id, file_path)
    except IL2FBRegimentLookupError:
      return self._data_missing_value

  def _load_value_or_raise(self, regiment_id: str, file_path: Path) -> str:
    if not file_path.exists():
      raise IL2FBRegimentDataSourceNotFound

    with file_path.open(mode="rb") as f:
      regiment_id = regiment_id.encode(self._data_file_encoding)
      for line in f:
        if line.startswith(regiment_id):
          key, value = line.split(maxsplit=1)
          return value.decode(self._data_value_encoding).strip()
      else:
        raise IL2FBRegimentLookupError


@export
class Regiment:

  def __init__(
    self,
    id:          str,
    air_force:   AirForceConstant,
    info_loader: Optional[RegimentInfoLoader]=None,
  ):
    self.id        = id
    self.air_force = air_force

    self._info_loader = info_loader or RegimentInfoLoader()
    self._text_attribute_loaders = {
      'verbose_name': self._info_loader.get_name,
      'help_text':    self._info_loader.get_description,
    }

  def __getattr__(self, name: str) -> str:
    loader = self._text_attribute_loaders.get(name)
    if not loader:
      raise IL2FBRegimentAttributeError(
        f"'{self.__class__}' object has no attribute '{name}'"
      )

    language = get_language()
    if language and language.upper() not in SUPPORTED_LANGUAGES:
      language = DEFAULT_LANGUAGE_NAME

    full_name = f"{name}_{language}"

    value = getattr(self, full_name, None)

    if not value:
      value = self._load_value(loader, language)
      setattr(self, full_name, value)

    return value

  def _load_value(
    self,
    loader:   Callable[[str, Any], str],
    language: Any,
  ) -> str:

    value = loader(regiment_id=self.id, language=language)

    if not value and language != DEFAULT_LANGUAGE_NAME:
      value = loader(regiment_id=self.id, language=DEFAULT_LANGUAGE_NAME)

    return value

  def to_primitive(self, context: Any=None) -> Dict[str, Any]:
    return {
      'id':           self.id,
      'air_force':    self.air_force.to_primitive(context),
      'verbose_name': self.verbose_name,
      'help_text':    self.help_text,
    }

  def __repr__(self) -> str:
    return f"<{self.__class__.__name__} '{self.id}'>"


@export
class Regiments:

  def __init__(
    self,
    data_dir_path:      Path=DEFAULT_DATA_DIR_PATH,
    data_file_name:     str=DEFAULT_CATALOG_FILE_NAME,
    data_file_encoding: str=DEFAULT_DATA_FILE_ENCODING,
    info_loader:        RegimentInfoLoader=None,
  ):
    self._data_file_path = data_dir_path / data_file_name
    if not self._data_file_path.exists():
      raise IL2FBRegimentDataSourceNotFound(
        f"data source file '{str(self._data_file_path)}' does not exist"
      )

    self._data_file_encoding = data_file_encoding

    self._info_loader = info_loader or RegimentInfoLoader(
      data_dir_path=data_dir_path,
      data_file_encoding=data_file_encoding,
    )

    self._cache = dict()

  def get_by_id(self, id: str) -> Regiment:
    regiment = self._cache.get(id)

    if not regiment:
      regiment = self._load_by_id_or_raise(id)
      self._cache[id] = regiment

    return regiment

  def _load_by_id_or_raise(self, id: str) -> Regiment:
    default_regiment_id = self._get_default_regiment_id_for_regiment(id)
    if not default_regiment_id:
      raise IL2FBRegimentLookupError(
        f"regiment with id '{id}' not found"
      )

    air_force = AIR_FORCES.get_by_default_regiment_id(default_regiment_id)

    return Regiment(
      id=id,
      air_force=air_force,
      info_loader=self._info_loader,
    )

  def _get_default_regiment_id_for_regiment(self, id: str) -> Optional[str]:
    with self._data_file_path.open(
      mode="rt",
      encoding=self._data_file_encoding,
      buffering=1,
    ) as f:

      default_regiment_id = None

      for line in f:
        line = line.strip()
        if not line:
          continue

        if line in DEFAULT_REGIMENTS_IDS:
          default_regiment_id = line

        elif line == id:
          return default_regiment_id

  def filter_by_air_force(self, air_force: AirForceConstant) -> List[Regiment]:
    result = []

    with self._data_file_path.open(
      mode="rt",
      encoding=self._data_file_encoding,
      buffering=1,
    ) as f:

      default_regiment_id = air_force.default_regiment_id
      air_force_is_found = False

      for line in f:
        line = line.strip()

        if not line:
          continue

        if line == default_regiment_id:
          air_force_is_found = True

        elif air_force_is_found:
          if (
             line in DEFAULT_REGIMENTS_IDS or
            (line.startswith('[') and line.endswith(']'))
          ):
            # Next section was found. Fullstop.
            break

          regiment = self._cache.get(line)
          if not regiment:
            regiment = Regiment(
              id=line,
              air_force=air_force,
              info_loader=self._info_loader,
            )
            self._cache[line] = regiment

          result.append(regiment)

    return result
