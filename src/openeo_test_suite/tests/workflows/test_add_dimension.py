from pathlib import Path

import xarray as xr


def test_ndvi_add_dim(
    connection,
    bounding_box_small,
    temporal_interval,
    s2_stac_url,
    t_dim,
    b_dim,
    tmp_path,
):
    filename = tmp_path / "test_ndvi_add_dim.nc"
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
    ndvi = ndvi.add_dimension(type="bands", name=b_dim, label="NDVI")
    ndvi.download(filename)

    assert Path(filename).exists()
    assert (
        len(xr.open_dataarray(filename).dims) == 4
    )  # 2 spatial + 1 temporal + 1 bands
    assert b_dim in xr.open_dataarray(filename).dims
    assert xr.open_dataarray(filename)[b_dim].values == "NDVI"
