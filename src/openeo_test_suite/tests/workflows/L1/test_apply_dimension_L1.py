import pytest

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L1"


def test_apply_dimension_quantiles_0(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

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
    skipper,
    cube_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

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
