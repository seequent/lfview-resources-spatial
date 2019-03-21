import pytest

import properties
from lfview.resources import files, spatial


def test_types():
    assert spatial.MappingContinuous.BASE_TYPE == 'mappings'
    assert spatial.MappingDiscrete.BASE_TYPE == 'mappings'
    assert spatial.MappingCategory.BASE_TYPE == 'mappings'
    assert spatial.MappingContinuous.SUB_TYPE == 'continuous'
    assert spatial.MappingDiscrete.SUB_TYPE == 'discrete'
    assert spatial.MappingCategory.SUB_TYPE == 'category'


@pytest.mark.parametrize(
    'gradient', [
        'https://example.com/api/files/array/abc123',
        [[0, 0, 0], [255, 255, 255]],
        files.Array(shape=[5, 3], dtype='Int16Array', content_length=30)
    ]
)
@pytest.mark.parametrize('data_controls', [[-1., 2., 3.], [1., 1., 1.]])
@pytest.mark.parametrize('gradient_controls', [[0., 0.5, 1], [0., 0., 0.]])
@pytest.mark.parametrize(
    'visibility', [[True, True, True, True], [0, 0, 1, 0]]
)
@pytest.mark.parametrize('interpolate', [0, 1])
def test_good_continuous(
        gradient, data_controls, gradient_controls, visibility, interpolate
):
    mc = spatial.MappingContinuous(
        gradient=gradient,
        data_controls=data_controls,
        gradient_controls=gradient_controls,
        visibility=visibility,
        interpolate=interpolate,
    )
    assert mc.validate()


def test_default_continuous():
    mc = spatial.MappingContinuous()
    assert mc.gradient_controls == [0., 0, 1, 1]
    assert mc.visibility == [False, True, True, True, False]
    assert not mc.interpolate


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('data_controls', [4.]),
        ('data_controls', [
            4.,
            4.,
            4.,
            5.,
            5,
        ]),
        ('data_controls', [4., 4., 4., 3.]),
        ('gradient_controls', [0.]),
        ('gradient_controls', [0., 0.1, 0.2, 0.3, 1.]),
        ('gradient_controls', [0., 1.]),
        ('visibility', [True, True]),
        ('visibility', [1, 1, 1, 1, 1, 1]),
        ('visibility', [True, True, True]),
    ]
)
def test_bad_continuous(prop, bad_val):
    mc = spatial.MappingContinuous(
        gradient='https://example.com/api/files/array/abc123',
        data_controls=[0., 1., 2., 3.],
    )
    with pytest.raises(properties.ValidationError):
        setattr(mc, prop, bad_val)
        mc.validate()


@pytest.mark.parametrize(
    'values', [['red', 'white', 'black'], [1., 2., 3.], ['a', 'b', 'c']]
)
@pytest.mark.parametrize('end_points', [[1., 2.], [1., 1.]])
@pytest.mark.parametrize('end_inclusive', [[True, True], [0, 0]])
@pytest.mark.parametrize('visibility', [[False, True, False], [1, 0, 1]])
def test_good_discrete(values, end_points, end_inclusive, visibility):
    md = spatial.MappingDiscrete(
        values=values,
        end_points=end_points,
        end_inclusive=end_inclusive,
        visibility=visibility,
    )
    assert md.validate()


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('values', [4.] * 257), ('end_points', [1.] * 256),
        ('end_inclusive', [True] * 256), ('visibility', [True] * 257),
        ('end_points', [0., 1., 2.]), ('end_inclusive', [True, True, True]),
        ('visibility', [True, True]), ('end_points', [2., 1.])
    ]
)
def test_bad_discrete(prop, bad_val):
    md = spatial.MappingDiscrete(
        values=['a', 'b', 'c'],
        end_points=[0., 1.],
        end_inclusive=[True, True],
        visibility=[True, True, True],
    )
    with pytest.raises(properties.ValidationError):
        setattr(md, prop, bad_val)
        md.validate()


@pytest.mark.parametrize(
    'values', [['red', 'white', 'black'], [1., 2., 3.], ['a', 'b', 'c']]
)
@pytest.mark.parametrize('indices', [[0, 1, 2], [10, 20, 30]])
@pytest.mark.parametrize('visibility', [[True, True, True], [0, 1, 0]])
def test_good_category(values, indices, visibility):
    mc = spatial.MappingCategory(
        values=values,
        indices=indices,
        visibility=visibility,
    )
    mc.validate()


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('values', [4.] * 257),
        ('indices', list(range(257))),
        ('visibility', [True] * 257),
        ('indices', [1, 2, 1]),
        ('indices', [0, 1]),
        ('visibility', [True, True]),
    ]
)
def test_bad_category(prop, bad_val):
    mc = spatial.MappingCategory(
        values=['a', 'b', 'c'],
        indices=[0, 1, 2],
        visibility=[True, True, True],
    )
    with pytest.raises(properties.ValidationError):
        setattr(mc, prop, bad_val)
        mc.validate()


@pytest.mark.parametrize(
    'instance', [
        spatial.MappingDiscrete(
            end_points=[5.],
            end_inclusive=[True],
            visibility=[True, True],
        ),
        spatial.MappingCategory(indices=[0, 1], visibility=[True, True])
    ]
)
def test_hex(instance):
    instance.values = ['white', 'black']
    assert instance.values == [(255, 255, 255), (0, 0, 0)]
    assert instance.serialize()['values'] == ['#FFFFFF', '#000000']


if __name__ == '__main__':
    pytest.main()
