from pathlib import Path

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Text

from verboselib import get_language

from il2fb.commons import SupportedLanguages
from il2fb.commons.organization import AirForce
from il2fb.commons.organization import AirForces


__here__ = Path(__file__).absolute().parent
__all__  = []


DEFAULT_LANGUAGE_NAME = SupportedLanguages.get_default().name

DEFAULT_DATA_DIR_PATH = __here__ / "data"
DEFAULT_DATA_MISSING_VALUE = None
DEFAULT_DATA_FILE_ENCODING = "cp1251"
DEFAULT_VALUE_ENCODING = "unicode-escape"

DEFAULT_CATALOG_FILE_NAME = "regiments.ini"

DEFAULT_NAMES_FILE_NAME_FORMAT        = "regShort_{language}.properties"
DEFAULT_DESCRIPTIONS_FILE_NAME_FORMAT = "regInfo_{language}.properties"

FLIGHT_PREFIXES = set(AirForces.get_flight_prefixes())


def export(target: Any) -> Any:
  __all__.append(target.__name__)
  return target


@export
class RegimentInfoLoader:

  def __init__(
    self,
    data_dir_path: Path=DEFAULT_DATA_DIR_PATH,
    data_file_encoding: Text=DEFAULT_DATA_FILE_ENCODING,
    data_value_encoding: Text=DEFAULT_VALUE_ENCODING,
    data_missing_value: Text=DEFAULT_DATA_MISSING_VALUE,
    names_file_name_format: Text=DEFAULT_NAMES_FILE_NAME_FORMAT,
    descriptions_file_name_format: Text=DEFAULT_DESCRIPTIONS_FILE_NAME_FORMAT,
  ):
    self._data_dir_path = data_dir_path
    self._data_file_encoding = data_file_encoding
    self._data_value_encoding = data_value_encoding
    self._data_missing_value = data_missing_value
    self._names_file_name_format = names_file_name_format
    self._descriptions_file_name_format = descriptions_file_name_format

  def get_name(self, code_name: Text, language: Any) -> Text:
    file_name = self._names_file_name_format.format(language=language)
    return self._get_value(code_name, file_name)

  def get_description(self, code_name: Text, language: Any) -> Text:
    file_name = self._descriptions_file_name_format.format(language=language)
    return self._get_value(code_name, file_name)

  def _get_value(self, code_name: Text, file_name: Text) -> Text:
    file_path = self._data_dir_path / file_name
    try:
      return self._load_value_or_raise(code_name, file_path)
    except ValueError:
      return self._data_missing_value

  def _load_value_or_raise(self, code_name: Text, file_path: Path) -> Text:
    if not file_path.exists():
      raise ValueError

    with file_path.open(mode="rb") as f:
      code_name = code_name.encode(self._data_file_encoding)
      for line in f:
        if line.startswith(code_name):
          key, value = line.split(maxsplit=1)
          return value.decode(self._data_value_encoding).strip()
      else:
        raise ValueError


@export
class Regiment:

  def __init__(
    self,
    air_force:   AirForce,
    code_name:   Text,
    info_loader: Optional[RegimentInfoLoader]=None,
  ):
    self.air_force = air_force
    self.code_name = code_name

    self._info_loader = info_loader or RegimentInfoLoader()
    self._text_attribute_loaders = {
      'verbose_name': self._info_loader.get_name,
      'help_text':    self._info_loader.get_description,
    }

  def __getattr__(self, name: Text) -> Text:
    loader = self._text_attribute_loaders.get(name)
    if not loader:
      raise AttributeError(
        f"'{self.__class__}' object has no attribute '{name}'"
      )

    language  = get_language()
    if language not in SupportedLanguages:
      language = DEFAULT_LANGUAGE_NAME

    full_name = f"{name}_{language}"

    value = getattr(self, full_name, None)

    if not value:
      value = self._load_value(loader, language)
      setattr(self, full_name, value)

    return value

  def _load_value(
    self,
    loader:   Callable[[Text, Any], Text],
    language: Any,
  ) -> Text:

    value = loader(code_name=self.code_name, language=language)

    if not value and language != DEFAULT_LANGUAGE_NAME:
      value = loader(code_name=self.code_name, language=DEFAULT_LANGUAGE_NAME)

    return value

  def to_primitive(self, context: Any=None) -> Dict[Text, Any]:
    return {
      'air_force':    self.air_force.to_primitive(context),
      'code_name':    self.code_name,
      'verbose_name': self.verbose_name,
      'help_text':    self.help_text,
    }

  def __repr__(self) -> Text:
    return f"<{self.__class__.__name__} '{self.code_name}'>"


@export
class Regiments:

  def __init__(
    self,
    data_dir_path:      Path=DEFAULT_DATA_DIR_PATH,
    data_file_name:     Text=DEFAULT_CATALOG_FILE_NAME,
    data_file_encoding: Text=DEFAULT_DATA_FILE_ENCODING,
    info_loader:        RegimentInfoLoader=None,
  ):
    self._data_file_path = data_dir_path / data_file_name
    if not self._data_file_path.exists():
      raise ValueError(
        f"Data file '{str(self._data_file_path)}' does not exist"
      )

    self._data_file_encoding = data_file_encoding

    self._info_loader = info_loader or RegimentInfoLoader(
      data_dir_path=data_dir_path,
      data_file_encoding=data_file_encoding,
    )

    self._cache = dict()

  def get_by_code_name(self, code_name: Text) -> Regiment:
    regiment = self._cache.get(code_name)

    if not regiment:
      regiment = self._load_by_code_name_or_raise(code_name)
      self._cache[code_name] = regiment

    return regiment

  def _load_by_code_name_or_raise(self, code_name: Text) -> Regiment:
    flight_prefix = self._get_flight_prefix_for_existing_regiment(code_name)
    if not flight_prefix:
      raise ValueError(f"Regiment with code name '{code_name}' not found")

    air_force = AirForces.get_by_flight_prefix(flight_prefix)

    return Regiment(
      air_force=air_force,
      code_name=code_name,
      info_loader=self._info_loader,
    )

  def _get_flight_prefix_for_existing_regiment(self, code_name: Text) -> Optional[Text]:
    with self._data_file_path.open(
      mode="rt",
      encoding=self._data_file_encoding,
      buffering=1,
    ) as f:

      flight_prefix = None

      for line in f:
        line = line.strip()
        if not line:
          continue

        if line in FLIGHT_PREFIXES:
          flight_prefix = line

        elif line == code_name:
          return flight_prefix

  def filter_by_air_force(self, air_force: AirForce) -> List[Regiment]:
    result = []

    with self._data_file_path.open(
      mode="rt",
      encoding=self._data_file_encoding,
      buffering=1,
    ) as f:

      default_flight_prefix = air_force.default_flight_prefix
      air_force_is_found = False

      for line in f:
        line = line.strip()

        if not line:
          continue

        if line == default_flight_prefix:
          air_force_is_found = True

        elif air_force_is_found:
          if (
             line in FLIGHT_PREFIXES or
            (line.startswith('[') and line.endswith(']'))
          ):
            # Next section was found. Fullstop.
            break

          regiment = self._cache.get(line)
          if not regiment:
            regiment = Regiment(
              air_force=air_force,
              code_name=line,
              info_loader=self._info_loader,
            )
            self._cache[line] = regiment

          result.append(regiment)

    return result
