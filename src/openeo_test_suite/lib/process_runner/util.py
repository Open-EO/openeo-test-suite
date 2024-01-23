import re
from datetime import datetime, timezone
from typing import Union

import numpy as np
import xarray as xr
from dateutil.parser import isoparse
from pandas import Timestamp

ISO8601_REGEX = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"


def numpy_to_native(data, expected):
    # Converting numpy dtypes to native python types
    if isinstance(data, np.ndarray) or isinstance(data, np.generic):
        if isinstance(expected, list):
            return data.tolist()
        else:
            if data.size == 0:
                return None
            if data.size == 1:
                return data.item()
            elif data.size > 1:
                return data.tolist()

    return data


def datacube_to_xarray(cube):
    coords = []
    crs = None
    for name in cube["order"]:
        dim = cube["dimensions"][name]
        if dim["type"] == "temporal":
            values = [
                isostr_to_datetime(date, fail_on_error=False) for date in dim["values"]
            ]
            # Verify that the values are all datetimes, otherwise likely the tests are invalid
            if all(isinstance(date, datetime) for date in values):
                # Ot looks like xarray does not support creating proper time dimensions from datetimes,
                # so we convert to np.datetime64 explicitly.
                # np.datetime64 doesn't like timezone-aware datetimes, so we remove the timezone.
                values = [np.datetime64(dt.replace(tzinfo=None), "ns") for dt in values]
            else:
                raise Exception("Mixed datetime types in temporal dimension")
        elif dim["type"] == "spatial":
            values = dim["values"]
            if "reference_system" in dim:
                crs = dim["reference_system"]
        else:
            values = dim["values"]

        coords.append((name, values))

    da = xr.DataArray(cube["data"], coords=coords)
    if crs is not None:
        da.attrs["crs"] = crs  # todo: non-standardized
    if "nodata" in cube:
        da.attrs["nodata"] = cube["nodata"]  # todo: non-standardized

    return da


def xarray_to_datacube(data):
    if not isinstance(data, xr.DataArray):
        return data

    order = list(data.dims)

    dims = {}
    for c in data.coords:
        type = "bands"
        values = []
        axis = None
        dtype = data.coords[c].dtype
        if np.issubdtype(dtype, np.datetime64) or isinstance(dtype, Timestamp):
            type = "temporal"
            values = [datetime_to_isostr(date) for date in data.coords[c].values]
        else:
            values = data.coords[c].values.tolist()
            if c == "x":  # todo: non-standardized
                type = "spatial"
                axis = "x"
            elif c == "y":  # todo: non-standardized
                type = "spatial"
                axis = "y"
            elif c == "t":  # todo: non-standardized
                type = "temporal"

        dim = {"type": type, "values": values}
        if axis is not None:
            dim["axis"] = axis
        if "crs" in data.attrs:
            dim["reference_system"] = data.attrs["crs"]  # todo: non-standardized

        dims[c] = dim

    cube = {
        "type": "datacube",
        "order": order,
        "dimensions": dims,
        "data": data.values.tolist(),
    }

    if "nodata" in data.attrs:
        cube["nodata"] = data.attrs["nodata"]  # todo: non-standardized

    return cube


def isostr_to_datetime(dt: str, fail_on_error=True) -> Union[datetime, str]:
    if not fail_on_error:
        try:
            return isostr_to_datetime(dt)
        except:
            return dt
    else:
        if re.match(ISO8601_REGEX, dt):
            return isoparse(dt)
        else:
            raise ValueError(
                "Datetime is not in ISO format (YYYY-MM-DDThh:mm:ss plus timezone))"
            )


def datetime_to_isostr(dt):
    if isinstance(dt, Timestamp):
        dt_object = dt.to_pydatetime()
    elif isinstance(dt, np.datetime64):
        # Convert numpy.datetime64 to timestamp (in seconds)
        timestamp = dt.astype("datetime64[s]").astype(int)
        # Create a datetime object from the timestamp
        dt_object = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
    elif isinstance(dt, datetime):
        dt_object = dt
    elif re.match(ISO8601_REGEX, dt):
        return dt
    else:
        raise NotImplementedError("Unsupported datetime type")

    # Convert to ISO format string
    return dt_object.isoformat().replace("+00:00", "Z")
