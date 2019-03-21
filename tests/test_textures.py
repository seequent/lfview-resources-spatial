import pytest

import properties
from lfview.resources import files, spatial


def test_types():
    assert spatial.TextureProjection.BASE_TYPE == 'textures'
    assert spatial.TextureProjection.SUB_TYPE == 'projection'


@pytest.mark.parametrize('origin', [[0., 0., 0.], [10, 15, 20]])
@pytest.mark.parametrize('axis_u', [[1, 0, 0], 'up'])
@pytest.mark.parametrize('axis_v', ['down', [0, 1, 0]])
@pytest.mark.parametrize(
    'image', [
        'https://example.com/api/files/image/abc123',
        files.Image(content_length=100)
    ]
)
def test_good_textureprojection(origin, axis_u, axis_v, image):
    tex = spatial.TextureProjection(
        origin=origin,
        axis_u=axis_u,
        axis_v=axis_v,
        image=image,
    )
    assert tex.validate()


@pytest.mark.parametrize(
    ('prop', 'bad_val'),
    [('image', 'https://example.com/api/files/array/abc123')]
)
def test_bad_textureprojection(prop, bad_val):
    tex = spatial.TextureProjection(
        origin=[0., 0, 0],
        axis_u='north',
        axis_v='east',
        image='https://example.com/api/files/image/abc123',
    )
    with pytest.raises(properties.ValidationError):
        setattr(tex, prop, bad_val)
        tex.validate()


if __name__ == '__main__':
    pytest.main()
