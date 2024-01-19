import numpy as np

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L2"


def test_filter_bbox(
    skipper,
    cube_one_day_red,
    collection_dims,
    tmp_path,
    bounding_box_32632_10x10,
):
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

    filename = tmp_path / "test_filter_bbox.nc"
    b_dim = collection_dims["b_dim"]
    x_dim = collection_dims["x_dim"]
    y_dim = collection_dims["y_dim"]
    t_dim = collection_dims["t_dim"]

    cube = cube_one_day_red.filter_bbox(bounding_box_32632_10x10)
    cube.download(filename)

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
    assert (data[x_dim].min().values - x_res/2) <= bounding_box_32632_10x10["west"]
    assert (data[x_dim].max().values + x_res/2) >= bounding_box_32632_10x10["east"]
    assert (data[y_dim].min().values - y_res/2) <= bounding_box_32632_10x10["north"]
    assert (data[y_dim].max().values + y_res/2) >= bounding_box_32632_10x10["south"]
    # Check that we got exactly 100x100 pixels
    assert np.prod(data.shape) == 100