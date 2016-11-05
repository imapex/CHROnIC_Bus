# CHROnIC_Bus
Microservice to Accept and Distribute Jobs. Not designed to be an especially feature rich message bus,
but created for a specific purpose - to asynchronously send/receive messages via HTTP REST API. This
bus is designed to sit in a public infrastructure and be reachable from environments that sit
behind a HTTP Proxy server, with limited outbound connectivity.

