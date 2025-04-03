import time

event_time = 1743135087465 / 1000  # Convert from ms to seconds
local_time = time.time()

print("Event Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(event_time)))
print("Local Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(local_time)))
print("Time Difference:", local_time - event_time)
