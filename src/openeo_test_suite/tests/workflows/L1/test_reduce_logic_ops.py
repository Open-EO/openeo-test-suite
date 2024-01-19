import numpy as np

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray

LEVEL = "L1"


def test_boolean_mask(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()
    skipper.skip_if_unmatching_process_level(level=LEVEL)

    filename = tmp_path / "test_boolean_mask.nc"
    b_dim = collection_dims["b_dim"]

    def compute_ndvi(data):
        from openeo.processes import array_element

        red = data.array_element(index=0)
        nir = data.array_element(index=1)
        return (nir - red) / (nir + red)

    ndvi = cube_one_day_red_nir.reduce_dimension(dimension=b_dim, reducer=compute_ndvi)
    ndvi_mask = ndvi > 0.75
    ndvi_mask.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    unique, counts = np.unique(data, return_counts=True)
    assert 0 in unique
    assert 1 in unique
    assert len(unique) <= 3 # zeros, ones and maybe NaNs
