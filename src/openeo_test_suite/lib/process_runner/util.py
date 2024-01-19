from datetime import datetime, timezone

import dateutil.parser
import numpy as np
import xarray as xr


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
            # date replace for older Python versions that don't support ISO parsing (only available since 3.11)
            values = [
                datetime.fromisoformat(date.replace("Z", "")) for date in dim["values"]
            ]
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
        if np.issubdtype(data.coords[c].dtype, np.datetime64):
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


def isostr_to_datetime(dt):
    return dateutil.parser.parse(dt)


def datetime_to_isostr(dt):
    # Convert numpy.datetime64 to timestamp (in seconds)
    timestamp = dt.astype("datetime64[s]").astype(int)
    # Create a datetime object from the timestamp
    dt_object = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
    # Convert to ISO format string
    return dt_object.isoformat().replace("+00:00", "Z")


def find_callback_parameters(runner, parent_process_id, parent_parameter):
    parent_process = runner.describe_process(parent_process_id)
    parameter = next(
        (p for p in parent_process.parameters if p["name"] == parent_parameter), None
    )
    if parameter is not None:
        schemas = (
            [parameter["schema"]]
            if isinstance(parameter["schema"], dict)
            else parameter["schema"]
        )
        schema = next(
            (s for s in schemas if "subtype" in s and s["subtype"] == "process-graph"),
            None,
        )
        if schema is not None:
            return schema["parameters"]
    return []
