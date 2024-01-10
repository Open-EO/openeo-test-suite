import pytest
import xarray as xr

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L1"


def test_reduce_time(
    netcdf_not_supported,
    process_levels,
    cube_red_nir,
    collection_dims,
    tmp_path,
):
    if netcdf_not_supported:
        pytest.skip("NetCDF not supported as output file format!")

    if len(process_levels) > 0 and LEVEL not in process_levels:
        pytest.skip(
            f"Skipping {LEVEL} workflow because the specified levels are: {process_levels}"
        )

    filename = tmp_path / "test_reduce_time.nc"
    b_dim = collection_dims["b_dim"]
    t_dim = collection_dims["t_dim"]

    cube = cube_red_nir.reduce_dimension(dimension=t_dim, reducer="mean")
    cube.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 3  # 2 spatial + 1 band
