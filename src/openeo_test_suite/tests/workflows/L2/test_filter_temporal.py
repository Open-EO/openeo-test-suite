from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L2"


def test_filter_temporal(
    skipper,
    cube_red_nir,
    collection_dims,
    tmp_path,
    temporal_interval_one_day,
):
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

    filename = tmp_path / "test_filter_temporal.nc"
    t_dim = collection_dims["t_dim"]
    b_dim = collection_dims["b_dim"]

    cube = cube_red_nir.filter_temporal(temporal_interval_one_day)
    cube.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 4  # 2 spatial + 1 bands + 1 temporal
    assert t_dim in data.dims
    assert len(data[t_dim]) == 1
