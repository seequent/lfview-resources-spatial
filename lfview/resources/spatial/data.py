"""Data objects that hold numeric attributes and mapping to elements"""
from lfview.resources.files import Array
import numpy as np
import omf
import properties
from properties.extras import Pointer
from six import string_types

from .base import _BaseResource
from .mappings import MappingCategory, MappingDiscrete, MappingContinuous


class _BaseData(_BaseResource):
    """Base class for data objects"""


class DataBasic(_BaseData):
    """Basic numeric attribute data

    This data type is defined by an array that directly maps
    to an element geometry. For no-data values, use NaN.

    Currently, this only accepts 1D arrays and, when applied to a grid,
    the array must be stored in row-major order.
    """
    BASE_TYPE = 'data'
    SUB_TYPE = 'basic'

    array = Pointer(
        'Array of numeric values at locations on an element geometry, '
        'specified by the location property',
        Array,
    )
    location = properties.StringChoice(
        'Location of the data on geometry',
        choices={
            'nodes': ['N', 'node', 'vertices', 'corners'],
            'cells': ['CC', 'cell', 'segments', 'faces', 'blocks'],
        }
    )
    mappings = properties.List(
        'Mappings associated with the data',
        prop=properties.Union(
            '',
            props=[
                Pointer('', MappingContinuous),
                Pointer('', MappingDiscrete),
            ],
        ),
        max_length=100,
        default=list,
    )

    @properties.validator('array')
    def _validate_array_1d(self, change):
        """Ensure the array is 1D"""
        if (isinstance(change['value'], string_types)
                or change['value'] is properties.undefined):
            return
        if not change['value'].is_1d():
            raise properties.ValidationError(
                message='{} must use 1D array'.format(
                    self.__class__.__name__,
                ),
                reason='invalid',
                prop='array',
                instance=self,
            )

    def to_omf(self, cell_location):
        self.validate()
        if self.location == 'nodes':
            location = 'vertices'
        else:
            location = cell_location
        omf_data = omf.ScalarData(
            name=self.name or '',
            description=self.description or '',
            location=location,
            array=self.array.array,
        )
        return omf_data


class DataCategory(DataBasic):
    """Category attribute data

    This data type requires the array to be integer values that
    that correspond to the indices defined by the categories
    mapping object. Any values in the array that do not have a
    corresponding category index are assumed to be no-data.

    Similar to DataBasic, arrays must be 1D and row-major ordered when
    applied to grids.
    """

    SUB_TYPE = 'category'

    categories = Pointer(
        'Category mappings that define indices and corresponding data values',
        MappingCategory,
    )
    mappings = properties.List(
        'Other mappings associated with the categories',
        prop=Pointer('', MappingCategory),
        max_length=100,
        default=list,
    )

    @properties.validator('array')
    def _validate_array_int(self, change):
        """Ensure the array is only integers"""
        if (isinstance(change['value'], string_types)
                or change['value'] is properties.undefined):
            return
        if 'int' not in change['value'].dtype.lower():
            raise properties.ValidationError(
                message='{} must use integer array'.format(
                    self.__class__.__name__,
                ),
                reason='invalid',
                prop='array',
                instance=self,
            )

    def to_omf(self, cell_location):
        self.validate()
        if self.location == 'nodes':
            location = 'vertices'
        else:
            location = cell_location
        all_mapping_indices = set(
            sum(
                [
                    mapping.indices
                    for mapping in [self.categories] + self.mappings
                ], []
            )
        )
        all_array_indices = sorted(set(self.array.array))
        index_map = {}
        for i, array_index in enumerate(all_array_indices):
            if array_index in all_mapping_indices:
                index_map[array_index] = i
            else:
                index_map[array_index] = -1
        output_array = np.array([index_map[val] for val in self.array.array])
        omf_data = omf.MappedData(
            name=self.name or '',
            description=self.description or '',
            location=location,
            array=output_array,
            legends=[
                mapping.to_omf(index_map)
                for mapping in [self.categories] + self.mappings
            ],
        )
        return omf_data
