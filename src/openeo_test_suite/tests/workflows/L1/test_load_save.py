import numpy as np

from openeo_test_suite.lib.workflows.io import (
    load_geotiff_dataarray,
    load_netcdf_dataarray,
)

LEVEL = "L1"


def test_load_save_netcdf(
    skipper,
    cube_red_nir,
    collection_dims,
    tmp_path,
    bounding_box_32632,
):
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

    filename = tmp_path / "test_load_save_netcdf.nc"
    b_dim = collection_dims["b_dim"]
    x_dim = collection_dims["x_dim"]
    y_dim = collection_dims["y_dim"]
    t_dim = collection_dims["t_dim"]

    cube_red_nir.download(filename)

    assert filename.exists()
    print(filename)
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 4
    assert b_dim in data.dims
    assert x_dim in data.dims
    assert y_dim in data.dims
    assert t_dim in data.dims
    assert len(data[b_dim]) == 2

    # Check that the requested AOI in included in the returned netCDF
    # Coordinates from xarray are pixel centers. The bbox provides the bbox bounds.
    x_res = np.abs(data[x_dim][0].values - data[x_dim][1].values)
    y_res = np.abs(data[y_dim][0].values - data[y_dim][1].values)
    assert (data[x_dim].min().values - x_res / 2) <= bounding_box_32632["west"]
    assert (data[x_dim].max().values + x_res / 2) >= bounding_box_32632["east"]
    assert (data[y_dim].min().values - y_res / 2) <= bounding_box_32632["north"]
    assert (data[y_dim].max().values + y_res / 2) >= bounding_box_32632["south"]


def test_load_save_10x10_netcdf(
    skipper,
    cube_red_10x10,
    collection_dims,
    tmp_path,
    bounding_box_32632_10x10,
):
    skipper.skip_if_no_netcdf_support()

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
    # Coordinates from xarray are pixel centers. The bbox provides the bbox bounds.
    x_res = np.abs(data[x_dim][0].values - data[x_dim][1].values)
    y_res = np.abs(data[y_dim][0].values - data[y_dim][1].values)
    assert (data[x_dim].min().values - x_res / 2) <= bounding_box_32632_10x10["west"]
    assert (data[x_dim].max().values + x_res / 2) >= bounding_box_32632_10x10["east"]
    assert (data[y_dim].min().values - y_res / 2) <= bounding_box_32632_10x10["north"]
    assert (data[y_dim].max().values + y_res / 2) >= bounding_box_32632_10x10["south"]
    # Check that we got exactly 100x100 pixels
    assert np.prod(data.shape) == 100


# The next test will fail if the back-end allows to store only 3D (x,y,bands) cubes to geoTIFF
# In this test, only a single acquisition in time should be loaded


def test_load_save_geotiff(
    skipper,
    cube_one_day_red,
    collection_dims,
    tmp_path,
    bounding_box_32632,
):
    skipper.skip_if_no_geotiff_support()

    filename = tmp_path / "test_load_save_geotiff.tiff"
    b_dim = collection_dims["b_dim"]
    x_dim = collection_dims["x_dim"]
    y_dim = collection_dims["y_dim"]
    t_dim = collection_dims["t_dim"]

    cube_one_day_red.download(filename)

    assert filename.exists()
    data = load_geotiff_dataarray(filename)

    # Check that the requested AOI in included in the returned netCDF
    # Coordinates from xarray are pixel centers. The bbox provides the bbox bounds.
    x_res = np.abs(data[x_dim][0].values - data[x_dim][1].values)
    y_res = np.abs(data[y_dim][0].values - data[y_dim][1].values)
    assert (data[x_dim].min().values - x_res / 2) <= bounding_box_32632["west"]
    assert (data[x_dim].max().values + x_res / 2) >= bounding_box_32632["east"]
    assert (data[y_dim].min().values - y_res / 2) <= bounding_box_32632["north"]
    assert (data[y_dim].max().values + y_res / 2) >= bounding_box_32632["south"]
