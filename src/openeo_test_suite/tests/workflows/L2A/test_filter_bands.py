from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray


def test_filter_bands(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename = tmp_path / "test_filter_bbox.nc"
    b_dim = collection_dims["b_dim"]

    cube = cube_one_day_red_nir.filter_bands(["B08"])
    skipper.skip_if_unselected_process(cube)
    cube.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 4
    assert b_dim in data.dims
    assert data[b_dim].values[0] == "B08"
