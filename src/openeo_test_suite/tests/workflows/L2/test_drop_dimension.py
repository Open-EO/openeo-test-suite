from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L2"


def test_drop_dimension_time(
    skipper,
    cube_red_10x10,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

    filename = tmp_path / "test_drop_dimension_time.nc"
    t_dim = collection_dims["t_dim"]
    b_dim = collection_dims["b_dim"]

    cube = cube_red_10x10.drop_dimension(name=t_dim)
    cube.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 3  # 2 spatial + 1 bands
    assert t_dim not in data.dims
