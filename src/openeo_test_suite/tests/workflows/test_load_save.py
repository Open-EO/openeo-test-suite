from pathlib import Path
import xarray as xr
import rioxarray

def test_load_save_netcdf(connection,bounding_box_small,temporal_interval,s2_stac_url):
    filename = "test_load_save_netcdf.nc"
    Path(filename).unlink(missing_ok=True)
    cube = connection.load_stac(
        url = s2_stac_url,
        spatial_extent = bounding_box_small,
        temporal_extent = temporal_interval,
        bands = ["B04","B08"]
    )
    cube.download(filename)
    assert Path(filename).exists()
    assert len(xr.open_dataarray(filename).dims) == 4

def test_load_save_geotiff(connection,bounding_box_small,temporal_interval_one_day,s2_stac_url):
    filename = "test_load_save_geotiff.tiff"
    Path(filename).unlink(missing_ok=True)
    cube = connection.load_stac(
        url = s2_stac_url,
        spatial_extent = bounding_box_small,
        temporal_extent = temporal_interval_one_day,
        bands = ["B08"]
    )
    cube.download(filename)
    assert Path(filename).exists()
    assert len(rioxarray.open_rasterio(filename).dims) >= 3 # 2 spatial + 1 band + (maybe) 1 time

