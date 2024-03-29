from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray


def test_apply_dimension_order(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename = tmp_path / "test_apply_dimension_order.nc"
    b_dim = collection_dims["b_dim"]

    from openeo.processes import order

    cube = cube_one_day_red_nir.apply_dimension(
        process=lambda d: order(d),
        dimension=b_dim,
    )
    skipper.skip_if_unselected_process(cube)
    cube.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data[b_dim]) == 2
