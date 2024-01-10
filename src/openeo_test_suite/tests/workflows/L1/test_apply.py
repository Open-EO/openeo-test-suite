import pytest

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L1"


def test_apply(
    netcdf_not_supported,
    process_levels,
    cube_one_day_red,
    collection_dims,
    tmp_path,
):
    if netcdf_not_supported:
        pytest.skip("NetCDF not supported as output file format!")

    if len(process_levels) > 0 and LEVEL not in process_levels:
        pytest.skip(
            f"Skipping {LEVEL} workflow because the specified levels are: {process_levels}"
        )

    filename = tmp_path / "test_apply.nc"
    cube = cube_one_day_red.apply(lambda x: x.clip(0, 1))
    cube.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=collection_dims["b_dim"])

    # TODO: deeper inspection of the data?
    assert (data.max().item(0)) == 1
