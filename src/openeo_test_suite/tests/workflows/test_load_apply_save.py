from pathlib import Path

import xarray as xr


def test_load_apply_save_netcdf(
    connection, bounding_box_small, temporal_interval_one_day, s2_stac_url, tmp_path
):
    from openeo.processes import clip

    filename = tmp_path / "test_load_apply_save_netcdf.nc"
    cube = connection.load_stac(
        url=s2_stac_url,
        spatial_extent=bounding_box_small,
        temporal_extent=temporal_interval_one_day,
        bands=["B04"],
    )
    cube = cube.apply(lambda x: x.clip(0, 1))
    cube.download(filename)
    assert Path(filename).exists()
    assert (xr.open_dataarray(filename).max().item(0)) == 1


def test_load_apply_dimension_save_netcdf(
    connection,
    bounding_box_small,
    temporal_interval_one_day,
    s2_stac_url,
    b_dim,
    tmp_path,
):
    filename = tmp_path / "test_load_apply_dimension_save_netcdf.nc"
    cube = connection.load_stac(
        url=s2_stac_url,
        spatial_extent=bounding_box_small,
        temporal_extent=temporal_interval_one_day,
        bands=["B04", "B08"],
    )
    cube = cube.apply_dimension(dimension=b_dim, process="max")
    cube.download(filename)
    print(xr.open_dataarray(filename)[b_dim])
    assert Path(filename).exists()
    assert len(xr.open_dataarray(filename)[b_dim]) == 1
