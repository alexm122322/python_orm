from abc import ABC
from typing import Any, Dict, List, Tuple
from .column import Column
from .foreign_key import ForeignKey
from .column_types.primary_key import PrimaryKey
from ..drivers.sql_adapter import SqlAdapter
from .errors import ValueError


class ModelColumnValue:
    """The utils class which unites field_name, column, and value data.

    Args:
        field_name: The name of field.
        column: The column of field.
    """

    def __init__(self, field_name: str, column: Column):
        self.field_name = field_name
        self.column = column
        self._value: Any = None

    def set_value(self, value: Any):
        """Validate value and set up.

        Args:
            value: Settuping value.

        Raises:
            ValueError: If column is not nullable but value is None.
            If value is not valid. Check out `ColumnType`.validate_value.
        """

        if not self.column.nullable and value is None:
            raise ValueError('Value shuold be not None')

        if value is not None and not self.column.type.validate_value(value):
            raise ValueError(
                f'Value {value}{type(value)} for column({self.column}) is not valid.')

        self._value = value

    @property
    def value(self) -> Any:
        return self._value

    def insert_value(self, adapter: SqlAdapter) -> str:
        """SQL adapted value.

        Args:
            adapter: SQL adapter.

        Return:
            str: SQL adapted value.
        """
        return self.column.insert_value(self.value, adapter)

    @property
    def column_name(self) -> str:
        return self.column.name


class ModelColumnValues:
    """The utils class which unites ModelColumnValue's. 
    And methods that work with the data(columns and their values).

    Args:
        columns: The ModelColumnValue's.
    """

    def __init__(self):
        self.columns: List[ModelColumnValue] = []

    def init(self, atrs: List[Tuple[str, Any]]):
        """Init columns.

        Args:
            atrs (List[Tuple[str, Any]]): _description_
        """
        for atr in atrs:
            if isinstance(atr[1], Column):
                self.columns.append(ModelColumnValue(atr[0], atr[1]))

    def contains_by_field_name(self, field_name: str):
        return [v.field_name for v in self.columns].__contains__(field_name)

    def set_values(self, kwargs: Dict[str, Any]):
        for name, value in kwargs.items():
            self.set_value_by_field_name(name, value)

    def set_value_by_field_name(self, field_name: str, value: Any):
        column = self.find_column_by_field_name(field_name)
        column.set_value(value)

    def get_column_by_field_name(self, field_name: str) -> ModelColumnValue:
        column = self.find_column_by_field_name(field_name)
        return column

    def find_column_by_field_name(self, field_name: str) -> ModelColumnValue | None:
        index = [v.field_name for v in self.columns].index(field_name)
        if index == -1:
            return None
        return self.columns[index]

    @property
    def dict(self) -> Dict[str, Any]:
        dict: Dict[str, Any] = {}
        for column in self.columns:
            dict[column.field_name] = column.value

        return dict


class Model(ABC):
    """The template of the table in a static manner.
    The Row of the table in object manner.
    You should set up `__tablename__` - the name of the table.
    Foreign Key:
        If you need to set up a Foreign Key should add `__foreignkey__` to your template.
        Or any other attribute with a `ForeignKey` type. 
        `__foreignkey__` is the recommended name of atribute.

    Args:

        kwargs: The values of row.
        column_values: Info about columns and values.
    """

    def __init__(self, **kwargs):
        self.column_values = ModelColumnValues()
        self._id: Column | None = None
        self._set_up_column_values(kwargs)
        self._find_id()

    def __getattribute__(self, __name: str) -> Any:
        """Overrides method for getting control of attributes.
        For row of the table implementation purposes only.
        If the attribute contains in the `column_values` 
        then the method returns the value from `column_values`.
        For other attributes default behavior.
        """
        if (__name != 'column_values'
                and self.column_values.contains_by_field_name(__name)):
            return self.column_values.get_column_by_field_name(__name).value

        return super().__getattribute__(__name)

    def __setattr__(self, __name: str, __value: Any):
        """Overrides method for set controll atrribute.
        For row of the table implementation purposes only.
        If the attribute contains in the `column_values` 
        then the method set the value to `column_values`.
        For other attributes default behavior.
        """
        if (__name != 'column_values'
                and self.column_values.contains_by_field_name(__name)):
            return self.column_values.set_value_by_field_name(__name, __value)

        return super().__setattr__(__name, __value)

    @property
    def dict(self) -> Dict[str, Any]:
        return self.column_values.dict

    @property
    def table_id(self) -> Column | None:
        return self._id

    @classmethod
    def c(cls) -> List[Column]:
        """Finds columns of the table.

        Returns:
            List[Column]: Columns of the table.
        """
        members = cls.__dict__
        return [value for _, value in members.items() if isinstance(value, Column)]

    @classmethod
    def f(cls) -> ForeignKey | None:
        """Finds the Foreign Key of the table.

        Returns:
            ForeignKey | None: The Foreign Key of the tabel.
             None if Foreign Key does not exist in the template of the table.
        """
        members = cls.__dict__
        for _, value in members.items():
            if isinstance(value, ForeignKey):
                return value
        return None

    @classmethod
    def tn(cls) -> str:
        """Finds the name of the table.

        Returns:
            str: The table name.
        """
        members = cls.__dict__
        for name, value in members.items():
            if name == '__tablename__':
                return value
        return None

    def _set_up_column_values(self, kwargs: Dict[str, Any]):
        """Sets up the `column_values.`

        Args:
            kwargs: The arguments of the table row.
        """
        atrs = [(atr, getattr(self, atr)) for atr in self.__dir__()]
        self.column_values.init(atrs)
        self.column_values.set_values(kwargs)

    def _find_id(self):
        """Find the id through columns."""
        for c in self.column_values.columns:
            if isinstance(c.column.type, PrimaryKey):
                self._id = c.column
                return
