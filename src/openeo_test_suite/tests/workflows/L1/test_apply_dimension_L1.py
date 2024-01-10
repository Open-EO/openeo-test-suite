import pytest

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L1"


def test_apply_dimension_quantiles_0(
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

    filename = tmp_path / "test_apply_dimension_quantiles_0.nc"
    b_dim = collection_dims["b_dim"]
    t_dim = collection_dims["t_dim"]

    from openeo.processes import quantiles

    cube = cube_one_day_red_nir.apply_dimension(
        process=lambda d: quantiles(d, [0.25, 0.5, 0.75]),
        dimension=b_dim,
    )

    cube.download(filename)
    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data[b_dim]) == 3


def test_apply_dimension_quantiles_1(
    netcdf_not_supported,
    cube_red_nir,
    collection_dims,
    tmp_path,
):
    if netcdf_not_supported:
        pytest.skip("NetCDF not supported as output file format!")

    filename = tmp_path / "test_apply_dimension_quantiles_1.nc"
    b_dim = collection_dims["b_dim"]
    t_dim = collection_dims["t_dim"]

    from openeo.processes import quantiles

    cube = cube_red_nir.apply_dimension(
        process=lambda d: quantiles(d, [0.25, 0.5, 0.75]),
        dimension=t_dim,
        target_dimension=b_dim,
    )

    cube.download(filename)
    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data[b_dim]) == 3
