import numpy as np
import pytest

from openeo_test_suite.lib.workflows.io import (
    load_geotiff_dataarray,
    load_netcdf_dataarray,
)

LEVEL = "L1"


def test_load_save_netcdf(
    netcdf_not_supported,
    process_levels,
    cube_red_nir,
    collection_dims,
    tmp_path,
):
    if netcdf_not_supported:
        pytest.skip("NetCDF not supported as output file format!")

    if len(process_levels) > 0 and LEVEL not in process_levels:
        pytest.skip(
            f"Skipping {LEVEL} workflow because the specified levels are: {process_levels}"
        )

    filename = tmp_path / "test_load_save_netcdf.nc"
    b_dim = collection_dims["b_dim"]
    x_dim = collection_dims["x_dim"]
    y_dim = collection_dims["y_dim"]
    t_dim = collection_dims["t_dim"]

    cube_red_nir.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 4
    assert b_dim in data.dims
    assert x_dim in data.dims
    assert y_dim in data.dims
    assert t_dim in data.dims
    assert len(data[b_dim]) == 2


def test_load_save_10x10_netcdf(
    netcdf_not_supported,
    cube_red_10x10,
    collection_dims,
    tmp_path,
    bounding_box_32632_10x10,
):
    if netcdf_not_supported:
        pytest.skip("NetCDF not supported as output file format!")

    filename = tmp_path / "test_load_save_10x10_netcdf.nc"
    b_dim = collection_dims["b_dim"]
    x_dim = collection_dims["x_dim"]
    y_dim = collection_dims["y_dim"]
    t_dim = collection_dims["t_dim"]

    cube_red_10x10.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 4
    assert b_dim in data.dims
    assert x_dim in data.dims
    assert y_dim in data.dims
    assert t_dim in data.dims
    # Check that the requested AOI in included in the returned netCDF
    assert data[x_dim].min().values <= bounding_box_32632_10x10["west"]
    assert data[x_dim].max().values >= bounding_box_32632_10x10["east"]
    assert data[y_dim].min().values <= bounding_box_32632_10x10["north"]
    assert data[y_dim].max().values >= bounding_box_32632_10x10["south"]
    # Check that we got exactly 100x100 pixels
    assert np.prod(data.shape) == 100


# The next test will fail if the back-end allows to store only 3D (x,y,bands) cubes to geoTIFF
# In this test, only a single acquisition in time should be loaded


def test_load_save_geotiff(geotiff_not_supported, cube_one_day_red, tmp_path):
    if geotiff_not_supported:
        pytest.skip("GeoTIFF not supported as output file format!")

    filename = tmp_path / "test_load_save_geotiff.tiff"
    cube_one_day_red.download(filename)

    assert filename.exists()
    data = load_geotiff_dataarray(filename)
    assert len(data.dims) >= 3  # 2 spatial + 1 band + (maybe) 1 time
    # TODO: check if the content matches the requested AOI! With VITO works with orginal CRS but not with lat/lon (as in this case)
