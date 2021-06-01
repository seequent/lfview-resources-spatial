"""Texture data objects that place images on elements"""
from lfview.resources.files import Image
import properties
from properties.extras import Pointer

from .data import _BaseData


class _BaseTexture(_BaseData):
    """Base class for texture data"""

    BASE_TYPE = 'textures'


class TextureProjection(_BaseTexture):
    """Simple texture data that projects an image onto an element

    Using origin and axes, this defines an image location in space. When
    this texture is applied to an element, the image from the texture
    is projected normal to its plane onto the element.

    This is ideal for projecting surface imagery onto a topographic
    surface.
    """

    SUB_TYPE = 'projection'

    origin = properties.Vector3('Origin point of the texture')
    axis_u = properties.Vector3(
        'Vector corresponding to the image horizontal axis'
    )
    axis_v = properties.Vector3(
        'Vector corresponding to the image vertical axis'
    )
    image = Pointer(
        'Texture image file',
        Image,
    )

    def to_omf(self):
        self.validate()
        omf_texture = omf.ImageTexture(
            name=self.name or '',
            description=self.description or '',
            axis_u=self.axis_u,
            axis_v=self.axis_v,
            image=self.image.image,
        )
        return omf_texture
