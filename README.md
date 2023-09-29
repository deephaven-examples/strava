## Strava

This repository contains a basic Deephaven Community Core instance with two scripts: `accessFit.py` and `runTickingHeartRate.py`. They both create tables by reading data. The former uses the `fitparse` Python module to read a `*.fit` file, and the latter reads a series of CSVs with Deephaven's CSV reader.

## Use

This project has the same prerequisites as [deephaven-core](https://github.com/deephaven/deephaven-core). See that readme for Deephaven Community Core installation.

From your terminal:

```sh
docker compose pull
docker compose up
```

The files are visible from the File Explorer in the top right of the UI.

Note: This application uses anonymous authentication. No key is required to access the Deephaven IDE.

With your web browser, connect to `http://localhost:10000/ide`.

## Notes

This project has been updated to work with Deephaven 0.28.0 and 0.28.1. No guarantee of backwards or forwards compatibility can be given.
