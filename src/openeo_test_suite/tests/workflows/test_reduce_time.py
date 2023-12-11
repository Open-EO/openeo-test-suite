from pathlib import Path

import xarray as xr


def test_reduce_time(
    connection, bounding_box_small, temporal_interval, s2_stac_url, t_dim, tmp_path
):
    filename = tmp_path / "test_reduce_time.nc"
    cube = connection.load_stac(
        url=s2_stac_url,
        spatial_extent=bounding_box_small,
        temporal_extent=temporal_interval,
        bands=["B04"],
    )
    cube = cube.reduce_dimension(dimension=t_dim, reducer="mean")
    cube.download(filename)
    assert Path(filename).exists()
    assert len(xr.open_dataarray(filename).dims) == 3  # 2 spatial + 1 band


def test_reduce_time_merge(
    connection, bounding_box_small, temporal_interval, s2_stac_url, t_dim, tmp_path
):
    filename = tmp_path / "test_reduce_time_merge.nc"
    cube = connection.load_stac(
        url=s2_stac_url,
        spatial_extent=bounding_box_small,
        temporal_extent=temporal_interval,
        bands=["B04"],
    )
    cube_0 = cube.reduce_dimension(dimension=t_dim, reducer="mean")
    cube_1 = cube.reduce_dimension(dimension=t_dim, reducer="median")

    cube_merged = cube_0.merge_cubes(cube_1, overlap_resolver="subtract")
    cube_merged.download(filename)
    assert Path(filename).exists()
    assert len(xr.open_dataarray(filename).dims) == 3  # 2 spatial + 1 band
