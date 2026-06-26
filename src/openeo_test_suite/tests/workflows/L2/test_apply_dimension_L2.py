import numpy as np

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray


def test_apply_dimension_ndvi_2(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename = tmp_path / "test_apply_dimension_ndvi_2.nc"
    b_dim = collection_dims["b_dim"]

    def compute_ndvi(data):
        from openeo.processes import array_concat

        red = data.array_element(label="B04")
        nir = data.array_element(label="B08")
        ndvi = (nir - red) / (nir + red)
        return array_concat(data, ndvi)

    ndvi = cube_one_day_red_nir.apply_dimension(dimension=b_dim, process=compute_ndvi)
    skipper.skip_if_unselected_process(ndvi)
    ndvi.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)
    assert len(data.dims) == 4  # 2 spatial + 1 temporal + 1 bands
    # Check that NDVI results is within -1 and +1
    assert np.nanmin(data[{b_dim: 2}]) >= -1
    assert np.nanmax(data[{b_dim: 2}]) <= 1

    # From the process definition, the number of bands should be now 3,
    # since we request concat B04,B08 and the result of NDVI computation
    assert len(data[b_dim]) == 3

    # From the process definition, bands label should be integers
    # starting from zero, since the process return arrays with 3 values
    # which is longer than the original length
    assert (data[b_dim].values[0] == 0) or (data[b_dim].values[0] == "0")
    assert (data[b_dim].values[1] == 1) or (data[b_dim].values[1] == "1")
    assert (data[b_dim].values[2] == 2) or (data[b_dim].values[2] == "2")
