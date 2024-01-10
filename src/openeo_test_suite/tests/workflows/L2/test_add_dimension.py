import pytest

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L2"


def test_ndvi_add_dim(
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

    filename = tmp_path / "test_ndvi_add_dim.nc"
    b_dim = collection_dims["b_dim"]

    def compute_ndvi(data):
        red = data.array_element(index=0)
        nir = data.array_element(index=1)
        return (nir - red) / (nir + red)

    ndvi = cube_one_day_red_nir.reduce_dimension(dimension=b_dim, reducer=compute_ndvi)
    ndvi = ndvi.add_dimension(type="bands", name=b_dim, label="NDVI")
    ndvi.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 4  # 2 spatial + 1 temporal + 1 bands
    assert b_dim in data.dims
    print(data[b_dim].values)
    assert data[b_dim].values == "NDVI"
