from pathlib import Path
import xarray as xr

def test_load_reduce_save_netcdf(connection,bounding_box_small,temporal_interval,s2_stac_url,t_dim,tmp_path):
    from openeo.processes import clip
    filename = tmp_path / "test_load_reduce_save_netcdf.nc"
    cube = connection.load_stac(
        url = s2_stac_url,
        spatial_extent = bounding_box_small,
        temporal_extent = temporal_interval,
        bands = ["B04"]
    )
    cube = cube.reduce_dimension(dimension=t_dim,reducer="mean")
    cube.download(filename)
    assert Path(filename).exists()
    assert len(xr.open_dataarray(filename).dims) == 3 # 2 spatial + 1 band

