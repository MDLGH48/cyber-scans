# cyber-scans

Design and implement a system for dispatching cyber scans.
The system should be built of (at least) 3 separate logical units:

**Ingest** – The ingestion system must be able to receive multiple requests to initiate scans
in parallel (N) under load. Per request, the system must acknowledge the fact that the
request has been received and provide the caller with a unique scan-id that will be
assigned to each dispatched scan.

**Process** – The dispatching system does not work under load, rather processes requests
at its own pace one by one.
(For efficiency, you may also implement an option for processing consecutive requests
in bulk)

**Status** – an endpoint where a caller can check the status of a scan using the unique
scan-id it received from the ingestion system.
The available statuses are:
- **Accepted** – the request for a new scan has been received and is pending
processing
- **Running** – the scan is currently running
- **Error** – an error occurred during the scan (e.g. bad domain name)
- **Complete** – the scan was completed successfully
- **Not-Found** – the scan-id could not be found

Statuses should be kept for at least 20 mins.
Status checks should not create additional loads on any other system.

You may use external tools. If you make an assumption about using an external system (DB, Cache etc.), 
create a mock in code wrapping the calls to the system.
Please use python and specify the dependencies.