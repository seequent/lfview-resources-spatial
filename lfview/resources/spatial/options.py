"""Objects that define visualization options"""
from collections import OrderedDict

import properties
from properties.extras import Pointer
from six import string_types

from .base import from_hex, to_hex
from .data import DataBasic, DataCategory
from .mappings import (
    MappingContinuous,
    MappingDiscrete,
    MappingCategory,
)
from .textures import TextureProjection


class _BaseOptions(properties.HasProperties):
    """Base class for all options"""

    _REGISTRY = OrderedDict()


class _BaseOptionsItem(_BaseOptions):
    """Base class for options on a specific visual attribute

    These options classes allow you to specify for each attribute
    both (1) a single static value and (2) variable values calculated
    from data/mapping.
    """

    def serialize(self, include_class=True, save_dynamic=False, **kwargs):
        """Serializer that explicitly excludes class"""
        output = super(_BaseOptionsItem, self).serialize(
            include_class=False, save_dynamic=save_dynamic, **kwargs
        )
        return output


class OptionsTexture(_BaseOptionsItem):
    """Options for a displayed texture"""

    value = properties.Float(
        'Opacity value of the texture image',
        min=0.0,
        max=1.0,
        default=1.0,
    )

    data = Pointer(
        'Texture data for visualization',
        TextureProjection,
    )


class OptionsOpacity(_BaseOptionsItem):
    """Options for displayed opacity

    Opaque is 1.0; transparent is 0.0. You may specify a single
    value for the entire Element or variable values using data and
    a mapping that evaluates to numbers in range 0-1.

    Note: Visualization clients may not support variable opacity.
    """

    value = properties.Float(
        'Single opacity value, used if data is unspecified',
        min=0.0,
        max=1.0,
        required=False,
    )
    data = properties.Union(
        'Data for attribute visualization',
        props=[
            Pointer('', DataBasic),
            Pointer('', DataCategory),
        ],
        required=False,
    )
    mapping = properties.Union(
        'Mapping to apply to data for visualization; must be specified '
        'if data is specified',
        props=[
            Pointer('', MappingContinuous),
            Pointer('', MappingDiscrete),
            Pointer('', MappingCategory),
        ],
        required=False,
    )

    @properties.validator
    def _validate_data(self):
        """Ensure value or data/mapping are set"""
        if self.data and not self.mapping:
            raise properties.ValidationError(
                message=(
                    'Mapping must be specified on visualization options if '
                    'data is present'
                ),
                reason='missing',
                prop='mapping',
                instance=self,
            )
        if not self.data and self.value is None:
            raise properties.ValidationError(
                message=(
                    'Value must be specified on visualization options if '
                    'data is not'
                ),
                reason='missing',
                prop='value',
                instance=self,
            )


class OptionsSize(OptionsOpacity):
    """Options for displayed size

    You may specify a single size value for the entire Element or
    variable values using data and a mapping that evaluates to positive
    numbers.

    Note: Visualization clients may not support variable size.
    """

    value = properties.Float(
        'Single size value, only used if data is unspecified',
        min=0.0,
        required=False,
    )


class OptionsColor(OptionsOpacity):
    """Options for displayed color

    You may specify a single solid color value for the entire Element or
    a variable colormap using data and mapping that evaluates to RGB color
    """

    value = properties.Color(
        'Single color value, only used if data is unspecified',
        required=False,
        serializer=to_hex,
        deserializer=from_hex,
    )


class OptionsSurfaceColor(OptionsColor):
    """Options for displayed surface color

    Identical to :class:`lfview.resources.spatial.options.OptionsColor`
    except it also includes solid back color.
    """

    back = properties.Color(
        'Back color of the surface, only used if data is unspecified',
        required=False,
        serializer=to_hex,
        deserializer=from_hex,
    )


class OptionsWireframe(_BaseOptionsItem):
    """Options for displaying wireframes on elements

    Currently this is limited to enabled/disabled.
    """
    active = properties.Boolean(
        'Wireframe on/off',
        default=False,
    )


class _BaseElementOptions(_BaseOptions):
    """Base class for various element options"""
    visible = properties.Boolean(
        'Visibility of resource on/off',
        default=True,
    )
    opacity = properties.Instance(
        'Default opacity options on the element',
        OptionsOpacity,
        default=OptionsOpacity,
    )
    color = properties.Instance(
        'Default color options on the element',
        OptionsColor,
        default=OptionsColor,
    )


class OptionsPoints(_BaseElementOptions):
    """PointSet visualization options"""


class OptionsLines(_BaseElementOptions):
    """LineSet visualization options

    Using this options class implies that lines do not have any thickness.
    """


class OptionsTubes(OptionsLines):
    """LineSet visualization options for lines with finite thickness

    This adds radius to standard
    :class:`lfview.resources.spatial.options.OptionsLines`
    and may be used with drillholes, for example.
    """
    radius = properties.Instance(
        'Default opacity options on the element',
        OptionsSize,
        default=OptionsSize,
    )


class OptionsSurface(_BaseElementOptions):
    """Surface visualizatino options"""
    color = properties.Instance(
        'Default color options on the element',
        OptionsSurfaceColor,
        default=OptionsSurfaceColor,
    )
    wireframe = properties.Instance(
        'Default wireframe options on the element',
        OptionsWireframe,
        default=OptionsWireframe,
    )
    textures = properties.List(
        'Default textures on the element',
        OptionsTexture,
        default=list,
    )


class OptionsBlockModel(_BaseElementOptions):
    """Volume visualization options for displaying as solid block model"""
    wireframe = properties.Instance(
        'Default wireframe options on the element',
        OptionsWireframe,
        default=OptionsWireframe,
    )


class OptionsVolumeSlices(OptionsBlockModel):
    """Volume visualization options for displaying certain cross sections

    Cross-section slices are specified by normalized location along the
    three volume axes.
    """
    slices_u = properties.List(
        'List of active slice locations along u axis',
        properties.Float('', min=0., max=1.),
        max_length=256,
        default=lambda: [0.5],
    )
    slices_v = properties.List(
        'List of active slice locations along v axis',
        properties.Float('', min=0., max=1.),
        max_length=256,
        default=lambda: [0.5],
    )
    slices_w = properties.List(
        'List of active slice locations along w axis',
        properties.Float('', min=0., max=1.),
        max_length=256,
        default=lambda: [0.5],
    )
