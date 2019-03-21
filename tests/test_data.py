import pytest

import properties
from lfview.resources import files, spatial


def test_types():
    assert spatial.DataBasic.BASE_TYPE == 'data'
    assert spatial.DataBasic.SUB_TYPE == 'basic'
    assert spatial.DataCategory.BASE_TYPE == 'data'
    assert spatial.DataCategory.SUB_TYPE == 'category'


@pytest.mark.parametrize(
    'array', [
        'https://example.com/api/files/array/abc123',
        [10., 20, 15.],
        files.Array(shape=[3], dtype='Float32Array', content_length=12),
    ]
)
@pytest.mark.parametrize('location', ['nodes', 'cells', 'N', 'CC'])
@pytest.mark.parametrize(
    'mappings', [
        [
            'https://example.com/api/mappings/continuous/abc123',
            'https://example.com/api/mappings/discrete/def456'
        ],
        [
            {
                'gradient': 'https://example.com/api/files/array/ghi789',
                'data_controls': [1., 2., 3., 4.]
            },
            {
                'values': ['a', 'b'],
                'end_points': [1.],
                'end_inclusive': [True],
                'visibility': [True, True]
            }
        ],
        [
            spatial.MappingContinuous(
                gradient='https://example.com/api/files/array/abc123',
                data_controls=[1., 2., 3., 4.]
            ),
            spatial.MappingDiscrete(
                values=['a', 'b'],
                end_points=[1.],
                end_inclusive=[True],
                visibility=[True, True]
            )
        ]
    ]
)
def test_good_databasic(array, location, mappings):
    data = spatial.DataBasic(
        array=array,
        location=location,
        mappings=mappings,
    )
    assert data.validate()


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('array', [[1., 2.], [3., 4.]]),
        ('location', 'edges'),
        (
            'mappings',
            ['https://example.com/api/mappings/continuous/def456'] * 101
        ),
    ]
)
def test_bad_databasic(prop, bad_val):
    data = spatial.DataBasic(
        array='https://example.com/api/files/array/abc123',
        location='N',
    )
    with pytest.raises(properties.ValidationError):
        setattr(data, prop, bad_val)
        data.validate()


@pytest.mark.parametrize(
    'array', [
        'https://example.com/api/files/array/abc123',
        [10, 20, 15],
        files.Array(shape=[3], dtype='Int16Array', content_length=6),
    ]
)
@pytest.mark.parametrize('location', ['nodes', 'cells', 'N', 'CC'])
@pytest.mark.parametrize(
    'mappings', [
        ['https://example.com/api/mappings/category/abc123'],
        [
            {
                'values': ['a', 'b'],
                'indices': [0, 1],
                'visibility': [True, True]
            }
        ],
        [
            spatial.MappingCategory(
                values=['a', 'b'], indices=[0, 1], visibility=[True, True]
            )
        ]
    ]
)
@pytest.mark.parametrize(
    'categories', [
        'https://example.com/api/mappings/category/abc123',
        {
            'values': ['a', 'b'],
            'indices': [0, 1],
            'visibility': [True, True]
        },
        spatial.MappingCategory(
            values=['a', 'b'], indices=[0, 1], visibility=[True, True]
        )
    ]
)
def test_good_datacategory(array, location, mappings, categories):
    data = spatial.DataCategory(
        array=array,
        location=location,
        categories=categories,
        mappings=mappings,
    )
    assert data.validate()


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('array', [1.5, 2.5, 3.5]),
        ('array', [[1, 2], [3, 4]]),
        ('location', 'edges'),
        (
            'mappings',
            ['https://example.com/api/mappings/category/def456'] * 101
        ),
        ('categories', 'https://example.com/api/mappings/continuous/def456'),
    ]
)
def test_bad_datacategory(prop, bad_val):
    data = spatial.DataCategory(
        array='https://example.com/api/files/array/abc123',
        location='N',
        categories='https://example.com/api/mappings/category/def456'
    )
    with pytest.raises(properties.ValidationError):
        setattr(data, prop, bad_val)
        data.validate()


if __name__ == '__main__':
    pytest.main()
