# dispatcher.py
import concurrent.futures
import queue
import time
import logging
from auth import authenticate_user, check_permissions, can_invoke_runtime
import docker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a Docker client
client = docker.from_env()

class Dispatcher:
    def __init__(self, max_workers_alpha=3, max_workers_beta=3, idle_timeout=60):
        """
        Initializes the Dispatcher with the specified maximum number of workers for each runtime
        and the idle timeout for containers.
        """
        self.max_workers_alpha = max_workers_alpha
        self.max_workers_beta = max_workers_beta
        self.alpha_queue = queue.Queue(maxsize=max_workers_alpha)
        self.beta_queue = queue.Queue(maxsize=max_workers_beta)
        self.alpha_containers = self.get_container_list("runtimealpha")
        self.beta_containers = self.get_container_list("runtimebeta")
        self.idle_timeout = idle_timeout
        self.container_last_used = {}

    def dispatch(self, user, runtime, args):
        """
        Dispatches the runtime execution request to the appropriate container.
        Authenticates the user and checks their permissions before dispatching.
        Returns the result of the runtime execution.
        """
        if not authenticate_user(user):
            return "Authentication failed"

        if not can_invoke_runtime(user, runtime.__name__):
            return "Permission denied"

        if runtime.__name__ == "RuntimeAlpha":
            permission = "alpha"
            work_queue = self.alpha_queue
            containers = self.alpha_containers
            max_workers = self.max_workers_alpha
        elif runtime.__name__ == "RuntimeBeta":
            permission = "beta"
            work_queue = self.beta_queue
            containers = self.beta_containers
            max_workers = self.max_workers_beta
        else:
            return "Invalid runtime"

        if not check_permissions(user, permission):
            return "Permission denied"

        container_name = None
        while containers:
            container_name = containers.pop(0)
            if self.is_container_available(container_name):
                break
            else:
                container_name = None

        if container_name is None:
            if len(containers) == 0:
                return f"Maximum number of active executions reached for {runtime.__name__}"
            else:
                return "No available containers"

        try:
            work_queue.put(None, block=False)
            logging.info(f"Dispatching {runtime.__name__} to container: {container_name}")
            result = self.run_container(user, runtime, args, container_name)
            work_queue.get()
            containers.append(container_name)
            return result
        except queue.Full:
            containers.append(container_name)
            return f"Maximum number of active executions reached for {runtime.__name__}"
        except Exception as e:
            logging.error(f"Error executing {runtime.__name__} on container: {container_name}")
            logging.error(str(e))
            work_queue.get()
            containers.append(container_name)
            return "An error occurred while executing the runtime"

    def run_container(self, user, runtime, args, container_name):
        """
        Runs the specified runtime in the specified container.
        Tracks the usage and checks for idle containers after the execution.
        Returns the result of the runtime execution.
        """
        try:
            container = client.containers.get(container_name)
            logging.info(f"Executing {runtime.__name__} on container: {container_name}")

            result = self.execute_in_container(container, runtime, args)
            logging.info(f"Execution completed for {runtime.__name__} on container: {container_name}")

            start_time = time.time()
            end_time = time.time()
            duration = end_time - start_time

            self.track_usage(user, runtime, start_time, end_time, duration)
            self.container_last_used[container_name] = end_time

            self.check_idle_containers()

            return result
        except Exception as e:
            logging.error(f"Error executing {runtime.__name__} on container: {container_name}")
            logging.error(str(e))
            return "An error occurred while executing the runtime"

    def execute_in_container(self, container, runtime, args):
        """
        Executes the specified runtime with the given arguments inside the specified container.
        Returns the result of the runtime execution.
        """
        logging.info(f"Executing {runtime.__name__} with args: {args}")
        cmd = f"from runtimes import {runtime.__name__}; r = {runtime.__name__}(); result = r.generate({args}); print(result)"
        _, output = container.exec_run(["python", "-c", cmd])
        result = output.decode("utf-8").strip()
        logging.info(f"Execution result for {runtime.__name__}: {result}")
        return result
    
    def get_container_list(self, runtime_prefix):
        """
        Retrieves the list of available containers for the specified runtime prefix.
        Returns the list of container names.
        """
        containers = []
        for i in range(1, 4):
            container_name = f"{runtime_prefix}{i}"
            if self.is_container_available(container_name):
                containers.append(container_name)
        return containers

    def is_container_available(self, container_name):
        """
        Checks if the specified container is available and running.
        Returns True if the container is available, False otherwise.
        """
        try:
            container = client.containers.get(container_name)
            return container.status == "running"
        except docker.errors.NotFound:
            return False

    def track_usage(self, user, runtime, start_time, end_time, duration):
        """
        Tracks the usage of the specified runtime by the user.
        Stores the usage data in a file named "usage.log".
        """
        usage_data = {
            "user": user,
            "runtime": runtime.__name__,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration
        }
        with open("usage.log", "a") as file:
            file.write(f"{usage_data}\n")

    def check_idle_containers(self):
        """
        Checks for idle containers and stops and removes them if they have been idle for longer than the specified idle timeout.
        """
        current_time = time.time()
        for container_name, last_used_time in self.container_last_used.items():
            if current_time - last_used_time > self.idle_timeout:
                try:
                    container = client.containers.get(container_name)
                    container.stop()
                    container.remove()
                    logging.info(f"Stopped and removed idle container: {container_name}")
                    if container_name in self.alpha_containers:
                        self.alpha_containers.remove(container_name)
                    elif container_name in self.beta_containers:
                        self.beta_containers.remove(container_name)
                    del self.container_last_used[container_name]
                except docker.errors.NotFound:
                    logging.warning(f"Container not found: {container_name}")
                except Exception as e:
                    logging.error(f"Error stopping and removing container: {container_name}")
                    logging.error(str(e))