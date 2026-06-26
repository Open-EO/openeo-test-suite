from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray


def test_apply(
    skipper,
    cube_one_day_red,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename = tmp_path / "test_apply.nc"
    cube = cube_one_day_red.apply(lambda x: x.clip(0, 1))
    skipper.skip_if_unselected_process(cube)
    cube.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=collection_dims["b_dim"])

    # TODO: deeper inspection of the data?
    assert (data.max().item(0)) == 1
