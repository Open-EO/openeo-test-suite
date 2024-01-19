from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L1"


def test_ndvi_index(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

    filename = tmp_path / "test_ndvi_index.nc"
    b_dim = collection_dims["b_dim"]

    def compute_ndvi(data):
        from openeo.processes import array_element

        red = data.array_element(index=0)
        nir = data.array_element(index=1)
        return (nir - red) / (nir + red)

    ndvi = cube_one_day_red_nir.reduce_dimension(dimension=b_dim, reducer=compute_ndvi)
    ndvi.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 3  # 2 spatial + 1 temporal


# Fails if array_index + label is not supported
def test_ndvi_label(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename = tmp_path / "test_ndvi_label.nc"
    b_dim = collection_dims["b_dim"]

    def compute_ndvi(data):
        red = data.array_element(label="B04")
        nir = data.array_element(label="B08")
        return (nir - red) / (nir + red)

    ndvi = cube_one_day_red_nir.reduce_dimension(dimension=b_dim, reducer=compute_ndvi)
    ndvi.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 3  # 2 spatial + 1 temporal
