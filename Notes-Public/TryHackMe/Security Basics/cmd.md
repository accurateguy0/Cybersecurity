Another valuable tool for troubleshooting is `tracert`, which stands for _trace route_. The command `tracert target_name` traces the network route traversed to reach the target. Without getting into more details, it expects the routers on the path to notify us if they drop a packet because its time-to-live (TTL) has reached zero.

We can list the running processes using `tasklist`.

You can check all available filters by displaying the help page using `tasklist /?`

With the process ID (PID) known, we can terminate any task using `taskkill /PID target_pid`.