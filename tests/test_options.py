import pytest

import properties
from lfview.resources import spatial


def test_no_class_in_serialize():
    boi = spatial.options._BaseOptionsItem()
    assert boi.serialize(include_class=True) == {}


@pytest.mark.parametrize('opacity', [0., 0.5, 1.])
@pytest.mark.parametrize('visible', [True, False])
@pytest.mark.parametrize(
    'data', [
        'https://example.com/api/textures/projection/abc123',
        {
            'origin': [0., 0, 0],
            'axis_u': [1., 0, 0],
            'axis_v': [0., 1, 1],
            'image': 'https://example.com/api/files/image/abc123'
        }
    ]
)
def test_good_optionstexture(opacity, visible, data):
    ot = spatial.options.OptionsTexture(
        value=opacity,
        visible=visible,
        data=data,
    )
    assert ot.validate()


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('value', -1.0), ('value', 5), ('visible', 1), ('visible', 'False'),
        ('data', properties.undefined),
        ('data', 'https://example.com/api/data/basic/abc123')
    ]
)
def test_bad_optionstexture(prop, bad_val):
    ot = spatial.options.OptionsTexture(
        data='https://example.com/api/textures/projection/abc123',
    )
    with pytest.raises(properties.ValidationError):
        setattr(ot, prop, bad_val)
        ot.validate()


@pytest.mark.parametrize(
    ('options_class', 'value'), [
        (spatial.options.OptionsOpacity, 0.5),
        (spatial.options.OptionsSize, 5),
        (spatial.options.OptionsColor, 'red'),
        (spatial.options.OptionsSurfaceColor, 'red')
    ]
)
@pytest.mark.parametrize(
    'data', [
        'https://example.com/api/data/basic/abc123',
        {
            'array': 'https://example.com/api/files/array/abc123',
            'location': 'nodes',
            'categories': 'https://example.com/api/mappings/category/def456'
        }
    ]
)
@pytest.mark.parametrize(
    'mapping', [
        'https://example.com/api/mappings/continuous/abc123',
        {
            'values': ['a'],
            'indices': [0],
            'visibility': [True]
        }
    ]
)
def test_good_optionsitems(options_class, value, data, mapping):
    opt = options_class(
        value=value,
        data=data,
        mapping=mapping,
    )
    assert opt.validate()


@pytest.mark.parametrize(
    'options_class', [
        spatial.options.OptionsOpacity, spatial.options.OptionsSize,
        spatial.options.OptionsColor, spatial.options.OptionsSurfaceColor
    ]
)
@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('value', -1.0), ('data', properties.undefined),
        ('data', 'https://example.com/api/textures/projection/abc123'),
        ('mapping', properties.undefined),
        ('mapping', 'https://example.com/api/data/basic/abc123')
    ]
)
def test_bad_optionsitems(options_class, prop, bad_val):
    opt = options_class(
        value=properties.undefined,
        data='https://example.com/api/data/basic/abc123',
        mapping='https://example.com/api/mappings/continuous/def456',
    )
    with pytest.raises(properties.ValidationError):
        setattr(opt, prop, bad_val)
        opt.validate()


def test_surface_color_serialization():
    opt = spatial.options.OptionsSurfaceColor(
        value='black',
        back='white',
    )
    assert opt.value == (0, 0, 0)
    assert opt.back == (255, 255, 255)
    assert opt.serialize()['value'] == '#000000'
    assert opt.serialize()['back'] == '#FFFFFF'


def test_options_wireframe():
    opt = spatial.options.OptionsWireframe()
    assert not opt.active


expected_type = {
    'opacity': spatial.options.OptionsOpacity,
    'color': spatial.options.OptionsColor,
    'radius': spatial.options.OptionsSize,
    'size': spatial.options.OptionsSize,
    'wireframe': spatial.options.OptionsWireframe,
    'textures': list,
}


@pytest.mark.parametrize(
    ('options_class', 'expected_props'), [
        (spatial.OptionsPoints, ['opacity', 'color', 'size']),
        (spatial.OptionsLines, ['opacity', 'color']),
        (spatial.OptionsTubes, ['opacity', 'color', 'radius']),
        (
            spatial.OptionsSurface,
            ['opacity', 'color', 'wireframe', 'textures']
        ), (spatial.OptionsBlockModel, ['opacity', 'color', 'wireframe']),
        (spatial.OptionsVolumeSlices, ['opacity', 'color', 'wireframe'])
    ]
)
def test_options_props(options_class, expected_props):
    assert options_class().visible
    for prop in expected_props:
        assert prop in options_class._props
        assert isinstance(getattr(options_class(), prop), expected_type[prop])


def test_surface_options():
    assert isinstance(
        spatial.OptionsSurface().color, spatial.options.OptionsSurfaceColor
    )


@pytest.mark.parametrize('prop', ['slices_u', 'slices_v', 'slices_w'])
def test_good_volumeslices_options(prop):
    opt = spatial.OptionsVolumeSlices(
        opacity={'value': 1}, color={'value': 'red'}
    )
    assert getattr(opt, prop) == [0.5]
    setattr(opt, prop, [])
    assert opt.validate()
    setattr(opt, prop, [val / 256. for val in range(256)])
    assert opt.validate()


@pytest.mark.parametrize('prop', ['slices_u', 'slices_v', 'slices_w'])
@pytest.mark.parametrize(
    'value', [[-1.], [0.5, 2.], [val / 257. for val in range(257)]]
)
def test_bad_volumeslices_options(prop, value):
    opt = spatial.OptionsVolumeSlices(
        opacity={'value': 1}, color={'value': 'red'}
    )
    with pytest.raises(properties.ValidationError):
        setattr(opt, prop, value)
        opt.validate()


@pytest.mark.parametrize(
    ('value', 'shape'), [
        (0, 'square'),
        (100, 'sphere'),
    ]
)
def test_good_point_options(value, shape):
    opt = spatial.options.OptionsPoints(
        size=spatial.options.OptionsSize(value=value),
        shape=shape,
        opacity={'value': 1},
        color={'value': 'red'}
    )
    assert opt.validate()


@pytest.mark.parametrize(
    ('value', 'shape'),
    [
        (-1, 'sphere'),  # bad size value
        (1, 'NotAnOption'),  # bad shape value
    ]
)
def test_bad_point_options(value, shape):
    with pytest.raises(properties.ValidationError):
        opt = spatial.options.OptionsPoints(
            size=spatial.options.OptionsSize(value=value),
            shape=shape,
            opacity={'value': 1},
            color={'value': 'red'}
        )
        opt.validate()


def test_default_point_options():
    opt = spatial.options.OptionsPoints()

    assert opt.shape == 'square'
    assert opt.size.value == 10
