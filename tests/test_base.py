import json

import pytest
from six import string_types

import properties
from lfview.resources import spatial


@pytest.mark.parametrize(
    ('rgb_val', 'hex_val'), [
        ((0, 0, 0), '#000000'), ((66, 134, 244), '#4286F4'),
        ((255, 255, 255), '#FFFFFF')
    ]
)
def test_hex(rgb_val, hex_val):
    assert spatial.base.to_hex(rgb_val) == hex_val
    assert spatial.base.from_hex(hex_val) == rgb_val


@pytest.mark.parametrize('hex_val', ['ABC', 'ABCDEF1', 'ABCDEZ'])
def test_hex_errors(hex_val):
    with pytest.raises(ValueError):
        spatial.base.from_hex(hex_val)


class Something(properties.HasProperties):

    my_string = properties.String('')
    my_int = properties.Integer('')


def test_snapshot():
    class HasSnapshot(properties.HasProperties):

        snapshot = spatial.base.InstanceSnapshot(
            'Instance represented by JSON string',
            Something,
        )

    input_dict = {'my_string': 'hi', 'my_int': 5}
    hs = HasSnapshot()
    hs.snapshot = input_dict

    s = hs.serialize(snapshot=True)
    assert isinstance(s['snapshot'], string_types)
    assert '"__class__": "Something"' in s['snapshot']
    assert '"my_string": "hi"' in s['snapshot']
    assert '"my_int": 5' in s['snapshot']
    assert properties.equal(hs, HasSnapshot.deserialize(s))

    ns = hs.serialize(include_class=False)
    assert ns['snapshot'] == input_dict
    assert properties.equal(hs, HasSnapshot.deserialize(ns))


def test_instance_snapshot_kwargs():
    with pytest.raises(ValueError):
        spatial.base.InstanceSnapshot(
            '',
            Something,
            serializer=lambda *args, **kwargs: 5,
        )
    with pytest.raises(ValueError):
        spatial.base.InstanceSnapshot(
            '',
            Something,
            deserializer=lambda *args, **kwargs: 5,
        )


def test_shortstring():
    no_max_string = spatial.base.ShortString('no max')
    assert no_max_string.max_length is None
    assert no_max_string.validate(None, 'a' * 1000)
    max_string = spatial.base.ShortString('100 max length', max_length=100)
    assert max_string.max_length == 100
    assert max_string.validate(None, 'a' * 100)
    with pytest.raises(properties.ValidationError):
        max_string.validate(None, 'a' * 101)


def test_uid():
    base = spatial.base._BaseResource()
    assert base.validate()
    assert base.uid is None
    base.uid = 'spatial/uid'
    assert base.uid == 'spatial/uid'


def test_props():
    base = spatial.base._BaseResource()
    assert 'name' in base._props
    assert isinstance(base._props['name'], spatial.base.ShortString)
    assert base._props['name'].max_length == 300
    assert 'description' in base._props
    assert isinstance(base._props['description'], spatial.base.ShortString)
    assert base._props['description'].max_length == 5000


if __name__ == '__main__':
    pytest.main()
