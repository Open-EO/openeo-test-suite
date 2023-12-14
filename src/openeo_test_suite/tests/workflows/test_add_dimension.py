from pathlib import Path

import xarray as xr


def test_ndvi_add_dim(cube_one_day_red_nir, b_dim, tmp_path):
    filename = tmp_path / "test_ndvi_add_dim.nc"

    def compute_ndvi(data):
        from openeo.processes import array_element

        red = data.array_element(index=0)
        nir = data.array_element(index=1)
        return (nir - red) / (nir + red)

    ndvi = cube_one_day_red_nir.reduce_dimension(dimension=b_dim, reducer=compute_ndvi)
    ndvi = ndvi.add_dimension(type="bands", name=b_dim, label="NDVI")
    ndvi.download(filename)

    assert Path(filename).exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)

    assert len(data.dims) == 4  # 2 spatial + 1 temporal + 1 bands
    assert b_dim in data.dims
    print(data[b_dim].values)
    assert data[b_dim].values == "NDVI"
