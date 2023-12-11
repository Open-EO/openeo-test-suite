from pathlib import Path

import xarray as xr


def test_ndvi_index(
    connection,
    bounding_box_small,
    temporal_interval,
    s2_stac_url,
    t_dim,
    b_dim,
    tmp_path,
):
    filename = tmp_path / "test_ndvi_index.nc"
    cube = connection.load_stac(
        url=s2_stac_url,
        spatial_extent=bounding_box_small,
        temporal_extent=temporal_interval,
        bands=["B04", "B08"],
    )

    def compute_ndvi(data):
        from openeo.processes import array_element

        red = data.array_element(index=0)
        nir = data.array_element(index=1)
        return (nir - red) / (nir + red)

    ndvi = cube.reduce_dimension(dimension=b_dim, reducer=compute_ndvi)

    print(ndvi.print_json())
    ndvi.download(filename)
    assert Path(filename).exists()
    assert len(xr.open_dataarray(filename).dims) == 3  # 2 spatial + 1 temporal


# Fails if array_index + label is not supported
def test_ndvi_label(
    connection,
    bounding_box_small,
    temporal_interval,
    s2_stac_url,
    t_dim,
    b_dim,
    tmp_path,
):
    filename = tmp_path / "test_ndvi_label.nc"
    cube = connection.load_stac(
        url=s2_stac_url,
        spatial_extent=bounding_box_small,
        temporal_extent=temporal_interval,
        bands=["B04", "B08"],
    )

    def compute_ndvi(data):
        from openeo.processes import array_element

        red = data.array_element(label="B04")
        nir = data.array_element(label="B08")
        return (nir - red) / (nir + red)

    ndvi = cube.reduce_dimension(dimension=b_dim, reducer=compute_ndvi)
    ndvi.download(filename)

    assert Path(filename).exists()
    assert len(xr.open_dataarray(filename).dims) == 3  # 2 spatial + 1 temporal
