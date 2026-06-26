from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray


def test_aggregate_temporal(
    skipper,
    cube_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename = tmp_path / "test_aggregate_temporal.nc"
    t_dim = collection_dims["t_dim"]
    b_dim = collection_dims["b_dim"]
    intervals = [
        ["2022-06-01", "2022-06-07"],
        ["2022-06-07", "2022-06-14"],
        ["2022-06-14", "2022-06-21"],
    ]
    cube = cube_red_nir.aggregate_temporal(intervals=intervals, reducer="sd")
    skipper.skip_if_unselected_process(cube)
    cube.download(filename)

    assert filename.exists()

    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 4  # 2 spatial + 1 bands + 1 temporal
    assert t_dim in data.dims
    assert len(data[t_dim]) == 3


def test_aggregate_temporal_period(
    skipper,
    cube_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename = tmp_path / "test_aggregate_temporal_period.nc"
    t_dim = collection_dims["t_dim"]
    b_dim = collection_dims["b_dim"]

    cube = cube_red_nir.aggregate_temporal_period(period="week", reducer="sum")
    skipper.skip_if_unselected_process(cube)
    cube.download(filename)

    assert filename.exists()

    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 4  # 2 spatial + 1 bands + 1 temporal
    assert t_dim in data.dims
    assert len(data[t_dim]) == 5
