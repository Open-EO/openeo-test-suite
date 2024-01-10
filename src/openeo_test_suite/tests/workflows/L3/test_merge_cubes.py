from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L3"


def test_reduce_time_merge(
    skipper,
    cube_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

    filename = tmp_path / "test_reduce_time_merge.nc"
    b_dim = collection_dims["b_dim"]
    t_dim = collection_dims["t_dim"]

    cube_0 = cube_red_nir.reduce_dimension(dimension=t_dim, reducer="mean")
    cube_1 = cube_red_nir.reduce_dimension(dimension=t_dim, reducer="median")

    cube_merged = cube_0.merge_cubes(cube_1, overlap_resolver="subtract")
    cube_merged.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)
    assert len(data.dims) == 3  # 2 spatial + 1 band
