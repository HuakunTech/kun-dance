from lib import compress_frame, decompress_frame, serialize_frame, deserialize_frame


def test_serialize():
    frame = [[0, 0, 0, 1, 1, 0, 0], [1, 1, 0, 1, 1, 0, 0]]
    serialized_frame = serialize_frame(frame)
    expected = "ooolloo\nllolloo"
    assert serialized_frame == expected


def test_deserialize():
    frame_str = "ooolloo\nllolloo"
    expected = [[0, 0, 0, 1, 1, 0, 0], [1, 1, 0, 1, 1, 0, 0]]
    deserialized_frame = deserialize_frame(frame_str)
    assert (deserialized_frame == expected).all()


def test_compress():
    frame_str = "ooolloo\nllolloo"
    compressed_frame = compress_frame(frame_str)
    expected = "3o2l2o\n2lo2l2o"
    assert compressed_frame == expected


def test_decompress():
    compressed_frame = "3o2l2o\n2lo2l2o"
    decompressed_frame = decompress_frame(compressed_frame)
    print(decompressed_frame)
    expected = "ooolloo\nllolloo"
    assert decompressed_frame == expected
