import pytest

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L3"


def test_apply_dimension_order(
    netcdf_not_supported,
    process_levels,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    if netcdf_not_supported:
        pytest.skip("NetCDF not supported as output file format!")

    if len(process_levels) > 0 and LEVEL not in process_levels:
        pytest.skip(
            f"Skipping {LEVEL} workflow because the specified levels are: {process_levels}"
        )

    filename = tmp_path / "test_apply_dimension_order.nc"
    b_dim = collection_dims["b_dim"]

    from openeo.processes import order

    cube = cube_one_day_red_nir.apply_dimension(
        process=lambda d: order(d),
        dimension=b_dim,
    )

    cube.download(filename)
    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data[b_dim]) == 2
