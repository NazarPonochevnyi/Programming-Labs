import time
import hazelcast
import threading


"""
docker network create hazelcast-network
docker run -it --network hazelcast-network --rm -e HZ_CLUSTERNAME=hello-world -v "C:\Users\Nazar\PythonWorkspace\Programming-Labs\Data_Intensive_Apps\Lab1\hazelcast.xml":/opt/hazelcast/config/hazelcast-docker.xml -p 5701:5701 hazelcast/hazelcast:5.1.5
docker run -it --network hazelcast-network --rm -e HZ_CLUSTERNAME=hello-world -v "C:\Users\Nazar\PythonWorkspace\Programming-Labs\Data_Intensive_Apps\Lab1\hazelcast.xml":/opt/hazelcast/config/hazelcast-docker.xml -p 5702:5702 hazelcast/hazelcast:5.1.5
docker run -it --network hazelcast-network --rm -e HZ_CLUSTERNAME=hello-world -v "C:\Users\Nazar\PythonWorkspace\Programming-Labs\Data_Intensive_Apps\Lab1\hazelcast.xml":/opt/hazelcast/config/hazelcast-docker.xml -p 5703:5703 hazelcast/hazelcast:5.1.5
"""
client = hazelcast.HazelcastClient(
    cluster_name="hello-world",
)

key, inc_value = "counter", 1000
distrib_map = client.get_map("my_distrib_map").blocking()
distrib_map.put(key, 0)

cp_counter = client.cp_subsystem.get_atomic_long(key).blocking()
cp_counter.set(0)


def inference(func):
    threads = []
    for t in range(10):
        thread = threading.Thread(target=func)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def increment_counter():
    for _ in range(inc_value):
        counter = distrib_map.get(key)
        counter += 1
        distrib_map.put(key, counter)

def increment_counter_pess():
    for _ in range(inc_value):
        distrib_map.lock(key)
        try:
            counter = distrib_map.get(key)
            counter += 1
            distrib_map.put(key, counter)
        finally:
            distrib_map.unlock(key)

def increment_counter_opti():
    for _ in range(inc_value):
        while True:
            try:
                counter = distrib_map.get(key)
                updated_counter = counter + 1
                if distrib_map.replace_if_same(key, counter, updated_counter):
                    break
            except hazelcast.exception.ConcurrentModificationError:
                pass

def increment_counter_cp():
    for _ in range(inc_value):
        cp_counter.increment_and_get()


start_time = time.time()
inference(increment_counter)
print("--- No locking ---")
print(f"Final value of counter: {distrib_map.get(key)}")
print(f"Execution time: {round(time.time() - start_time, 2)}")
distrib_map.put(key, 0)

start_time = time.time()
inference(increment_counter_pess)
print("--- Pessimistic locking ---")
print(f"Final value of counter: {distrib_map.get(key)}")
print(f"Execution time: {round(time.time() - start_time, 2)}")
distrib_map.put(key, 0)

start_time = time.time()
inference(increment_counter_opti)
print("--- Optimistic locking ---")
print(f"Final value of counter: {distrib_map.get(key)}")
print(f"Execution time: {round(time.time() - start_time, 2)}")

start_time = time.time()
inference(increment_counter_cp)
print("--- CP Counter ---")
print(f"Final value of counter: {cp_counter.get()}")
print(f"Execution time: {round(time.time() - start_time, 2)}")

client.shutdown()
