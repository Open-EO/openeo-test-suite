import numpy as np

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L1"


def test_apply_dimension_quantiles_0(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    """
    From https://processes.openeo.org/#apply_dimension
    The dimension labels are preserved when the target dimension
    is the source dimension and the number of values in the source
    dimension is equal to the number of values computed by the process.
    Otherwise, the dimension labels will be incrementing integers starting
    from zero, which can be changed using rename_labels afterwards. The
    number of labels will be equal to the number of values computed by the process.
    """
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

    filename = tmp_path / "test_apply_dimension_quantiles_0.nc"
    b_dim = collection_dims["b_dim"]
    t_dim = collection_dims["t_dim"]

    from openeo.processes import quantiles

    cube = cube_one_day_red_nir.apply_dimension(
        process=lambda d: quantiles(d, probabilities=[0.5, 0.75]),
        dimension=b_dim,
    )

    cube.download(filename)
    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    # From the process definition, the number of bands should remain 2,
    # since we request 2 quantiles over bands written into bands
    assert len(data[b_dim]) == 2

    # From the process definition, bands label should remain the same
    assert data[b_dim].values[0] == "B04"
    assert data[b_dim].values[1] == "B08"


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
        process=lambda d: quantiles(d, probabilities=[0.25, 0.5, 0.75]),
        dimension=t_dim,
        target_dimension=b_dim,
    )
    print(filename)
    cube.download(filename)
    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    # From the process definition, the number of bands should be now 3,
    # since we request 3 quantiles over time written into bands
    assert len(data[b_dim]) == 3

    # From the process definition, bands label should be integers
    # starting from zero
    assert (data[b_dim].values[0] == 0) or (data[b_dim].values[0] == "0")
    assert (data[b_dim].values[1] == 1) or (data[b_dim].values[1] == "1")
    assert (data[b_dim].values[2] == 2) or (data[b_dim].values[2] == "2")


def test_apply_dimension_ndvi(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

    filename = tmp_path / "test_apply_dimension_ndvi.nc"
    b_dim = collection_dims["b_dim"]

    def compute_ndvi(data):
        from openeo.processes import array_concat, array_element

        red = data.array_element(index=0)
        nir = data.array_element(index=1)
        ndvi = (nir - red) / (nir + red)
        return array_concat(data, ndvi)

    ndvi = cube_one_day_red_nir.apply_dimension(dimension=b_dim, process=compute_ndvi)
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
