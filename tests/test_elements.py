import pytest

import numpy as np
import properties
from lfview.resources import spatial


@pytest.mark.parametrize(
    ('element_class', 'sub_type'), [
        (spatial.ElementPointSet, 'pointset'),
        (spatial.ElementLineSet, 'lineset'),
        (spatial.ElementSurface, 'surface'),
        (spatial.ElementSurfaceGrid, 'surfacegrid'),
        (spatial.ElementVolumeGrid, 'volumegrid')
    ]
)
def test_types(element_class, sub_type):
    assert element_class.BASE_TYPE == 'elements'
    assert element_class.SUB_TYPE == sub_type


class FakeElement(spatial.elements._BaseElementPointSet):
    num_nodes = 3
    num_cells = None


class FakeData(spatial.DataBasic):
    location = properties.StringChoice(
        'Alternative locations', ['nodes', 'cells', 'edges']
    )


@pytest.mark.parametrize(
    'data', [
        [],
        ['https://example.com/api/data/basic/abc123'] * 100,
        [
            spatial.TextureProjection(
                origin=[0., 0, 0],
                axis_u='east',
                axis_v='north',
                image='https://example.com/api/files/image/abc123'
            )
        ],
        [
            spatial.DataBasic(
                location='nodes',
                array='https://example.com/api/files/array/abc123'
            )
        ],
        [spatial.DataBasic(location='cells', array=[1., 2., 3., 4., 5.])],
        [spatial.DataBasic(location='nodes', array=[1., 2., 3.])],
    ]
)
def test_good_element_data_validation(data):
    elem = FakeElement(data=data)
    assert elem.validate()


@pytest.mark.parametrize(
    'data', [
        ['https://example.com/api/data/basic/abc123'] * 101,
        ['https://example.com/api/elements/pointset/abc123'],
        [
            FakeData(
                location='edges',
                array='https://example.com/api/files/array/abc123'
            )
        ],
        [spatial.DataBasic(location='nodes', array=[1., 2., 3., 4.])],
    ]
)
def test_bad_element_data_validation(data):
    with pytest.raises(properties.ValidationError):
        elem = FakeElement(data=data)
        elem.validate()


@pytest.mark.parametrize(
    ('vertices', 'num_nodes', 'num_cells', 'validate'), [
        (properties.undefined, None, None, False),
        ('https://example.com//api/files/array/abc123', None, None, True),
        ([[1., 2, 3], [4, 5, 6]], 2, 2, True)
    ]
)
def test_good_elementpointset(vertices, num_nodes, num_cells, validate):
    elem = spatial.ElementPointSet(vertices=vertices)
    if validate:
        assert elem.validate()
    assert elem.num_nodes == num_nodes
    assert elem.num_cells == num_cells


@pytest.mark.parametrize(
    'bad_val', [
        'https://example.com/api/data/basic/abc123', [1., 2, 3, 4],
        [[1., 2], [3, 4]]
    ]
)
def test_bad_elementpointset(bad_val):
    with pytest.raises(properties.ValidationError):
        elem = spatial.ElementPointSet(vertices=bad_val)
        elem.validate()


@pytest.mark.parametrize(
    ('vertices', 'segments', 'num_nodes', 'num_cells', 'validate'), [
        (properties.undefined, properties.undefined, None, None, False),
        (
            'https://example.com//api/files/array/abc123',
            'https://example.com//api/files/array/def456', None, None, True
        ), ([[1., 2, 3], [4, 5, 6], [7, 8, 9]], [[0, 1], [1, 2]], 3, 2, True)
    ]
)
def test_good_elementlineset(
        vertices, segments, num_nodes, num_cells, validate
):
    elem = spatial.ElementLineSet(vertices=vertices, segments=segments)
    if validate:
        assert elem.validate()
    assert elem.num_nodes == num_nodes
    assert elem.num_cells == num_cells


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('vertices', 'https://example.com/api/data/basic/abc123'),
        ('vertices', [1., 2, 3, 4]),
        ('vertices', [[1., 2], [3, 4], [5, 6], [7, 8]]),
        ('segments', 'https://example.com/api/data/basic/abc123'),
        ('segments', [0, 1, 2, 3]),
        ('segments', [[0, 1, 2], [1, 2, 3]]),
        ('segments', [[0.5, 1.5], [1.5, 2.5]]),
        ('segments', [[-1, 0], [0, 1]]),
        ('segments', [[0, 1], [2, 3], [4, 5]]),
    ]
)
def test_bad_elementlineset(prop, bad_val):
    elem = spatial.ElementLineSet(
        vertices=[[1., 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
        segments=[[0, 1], [1, 2], [2, 3]],
    )
    with pytest.raises(properties.ValidationError):
        setattr(elem, prop, bad_val)
        elem.validate()


@pytest.mark.parametrize(
    ('vertices', 'triangles', 'num_nodes', 'num_cells', 'validate'), [
        (properties.undefined, properties.undefined, None, None, False),
        (
            'https://example.com//api/files/array/abc123',
            'https://example.com//api/files/array/def456', None, None, True
        ), ([[1., 2, 3], [4, 5, 6], [7, 8, 9]], [[0, 1, 2]], 3, 1, True)
    ]
)
def test_good_elementsurface(
        vertices, triangles, num_nodes, num_cells, validate
):
    elem = spatial.ElementSurface(vertices=vertices, triangles=triangles)
    if validate:
        assert elem.validate()
    assert elem.num_nodes == num_nodes
    assert elem.num_cells == num_cells


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('vertices', 'https://example.com/api/data/basic/abc123'),
        ('vertices', [1., 2, 3, 4]),
        ('vertices', [[1., 2], [3, 4], [5, 6], [7, 8]]),
        ('triangles', 'https://example.com/api/data/basic/abc123'),
        ('triangles', [0, 1, 2, 3]),
        ('triangles', [[0, 1], [1, 2]]),
        ('triangles', [[0.5, 1.5, 2.5], [1.5, 2.5, 3.5]]),
        ('triangles', [[-1, 0, 1], [0, 1, 2]]),
        ('triangles', [[0, 1, 2], [3, 4, 5]]),
    ]
)
def test_bad_elementsurface(prop, bad_val):
    elem = spatial.ElementSurface(
        vertices=[[1., 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
        triangles=[[0, 1, 2], [1, 2, 3], [2, 3, 0]],
    )
    with pytest.raises(properties.ValidationError):
        setattr(elem, prop, bad_val)
        elem.validate()


@pytest.mark.parametrize(
    ('tensor_u', 'tensor_v', 'offset_w', 'num_nodes', 'num_cells', 'validate'),
    [
        ([1], [1], properties.undefined, 4, 1, True),
        (
            [1, 1], [2], 'https://example.com//api/files/array/abc123', 6, 2,
            True
        ), (np.array([2]), np.array([1, 1]), [1., 2, 3, 4, 5, 6], 6, 2, True),
        (
            properties.undefined, properties.undefined, properties.undefined,
            None, None, False
        )
    ]
)
def test_good_elementsurfacegrid(
        tensor_u, tensor_v, offset_w, num_nodes, num_cells, validate
):
    elem = spatial.ElementSurfaceGrid(
        tensor_u=tensor_u,
        tensor_v=tensor_v,
        offset_w=offset_w,
        origin=[0, 0, 0],
        axis_u='east',
        axis_v='north',
    )
    if validate:
        assert elem.validate()
    assert elem.num_nodes == num_nodes
    assert elem.num_cells == num_cells


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('tensor_u', [-1., 1]), ('tensor_u', [1.] * 10001),
        ('tensor_v', [-1., 1]), ('tensor_v', [1.] * 10001),
        ('offset_w', [[1., 2, 3], [4, 5, 6], [7, 8, 9]]),
        ('offset_w', [1., 2, 3, 4])
    ]
)
def test_bad_elementsurfacegrid(prop, bad_val):
    elem = spatial.ElementSurfaceGrid(
        tensor_u=[1., 1],
        tensor_v=[1., 1],
        origin=[0, 0, 0],
        axis_u='east',
        axis_v='north',
    )
    with pytest.raises(properties.ValidationError):
        setattr(elem, prop, bad_val)
        elem.validate()


@pytest.mark.parametrize(
    ('tensor_u', 'tensor_v', 'tensor_w', 'num_nodes', 'num_cells', 'validate'),
    [
        ([1], [1], [1], 8, 1, True),
        (
            np.array([2]), np.array([1, 1]), np.array([0.5, 0.5, 0.5, 0.5]),
            30, 8, True
        ),
        (
            properties.undefined, properties.undefined, properties.undefined,
            None, None, False
        )
    ]
)
def test_good_elementvolumegrid(
        tensor_u, tensor_v, tensor_w, num_nodes, num_cells, validate
):
    elem = spatial.ElementVolumeGrid(
        tensor_u=tensor_u,
        tensor_v=tensor_v,
        tensor_w=tensor_w,
        origin=[0, 0, 0],
        axis_u='east',
        axis_v='north',
        axis_w='up',
    )
    if validate:
        assert elem.validate()
    assert elem.num_nodes == num_nodes
    assert elem.num_cells == num_cells


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('tensor_u', [-1., 1]), ('tensor_u', [1.] * 2001),
        ('tensor_v', [-1., 1]), ('tensor_v', [1.] * 2001),
        ('tensor_w', [-1., 1]), ('tensor_w', [1.] * 2001)
    ]
)
def test_bad_elementvolumegrid(prop, bad_val):
    elem = spatial.ElementVolumeGrid(
        tensor_u=[1., 1],
        tensor_v=[1., 1],
        tensor_w=[1., 1],
        origin=[0, 0, 0],
        axis_u='east',
        axis_v='north',
        axis_w='up',
    )
    with pytest.raises(properties.ValidationError):
        setattr(elem, prop, bad_val)
        elem.validate()


if __name__ == '__main__':
    pytest.main()
