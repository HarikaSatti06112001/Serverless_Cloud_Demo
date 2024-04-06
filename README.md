# Serverless Cloud System

## Introduction

This project aims to implement a mockup of a serverless cloud system that exposes a set of Python classes to an end user, abstracting away the underlying cloud layer. The system allows users to invoke two different runtimes, RuntimeAlpha and RuntimeBeta, with specified prompts and receive generated responses.

## Architecture

The serverless cloud system consists of three main components:

- **User-facing code:** Provides a simple interface for users to invoke the runtimes by importing the Alpha and Beta classes from the my_mk1_homework module.
- **Host-facing code:** Includes the RuntimeAlpha and RuntimeBeta classes, which are wrapped and called from within containers. These classes simulate processing time and generate responses based on the input prompts.
- **Dispatcher:** Handles incoming function calls, forwards them to the appropriate container, and returns the responses to the user. It implements load balancing and queue management to ensure efficient execution of the runtimes.

## Implementation Details

### User-facing code

The user-facing code allows users to invoke the Alpha and Beta runtimes by importing them from the my_mk1_homework module. Users can provide a prompt as input and receive the generated response. The code supports multiple invocations of the runtimes in parallel.

### Host-facing code

The host-facing code defines the RuntimeAlpha and RuntimeBeta classes, which are executed within containers. Each runtime class has a load method that is called when the container starts and simulates a startup time. The generate method of each runtime class takes the user's prompt as input, simulates processing time, and generates a response.

### Dispatcher

The dispatcher component is responsible for handling incoming function calls, forwarding them to the appropriate container, and returning the responses to the user. It implements load balancing and queue management to ensure efficient execution of the runtimes.

The dispatcher uses separate queues for RuntimeAlpha and RuntimeBeta to manage the workload. It maintains a list of available containers for each runtime and dispatches the function calls to the next available container in a round-robin fashion.

The dispatcher enforces the constraint of allowing a maximum of three active executions of each runtime at any given time. If the maximum limit is reached, the dispatcher returns an appropriate message to the user.

## Authentication and Authorization

The system includes an authentication mechanism to verify users and an authorization system to control access to the runtimes based on user roles and permissions. Users are authenticated based on their provided username, and their permissions are checked against a predefined set of user roles.

Users can only invoke the runtimes they are authorized to access. If a user tries to invoke a runtime they are not authorized for, the dispatcher returns a permission denied message.

## Container Management

The system uses Docker containers to execute the runtimes. The dispatcher manages the container lifecycle, including starting and stopping containers based on the workload.

To optimize resource utilization, the dispatcher implements a strategy to shut down containers that have been idle for a certain period of time. It keeps track of the last usage time of each container and periodically checks for idle containers. If a container has been idle for longer than the specified timeout, it is stopped and removed.

## Usage Tracking

The system tracks the usage of the runtimes for each user. It records the start time, end time, and duration of each runtime execution and stores the usage data in a log file. This data can be used for billing and analytics purposes.

## Error Handling

The system includes error handling mechanisms to gracefully handle exceptions and provide meaningful error messages to the users. If an error occurs during the execution of a runtime, the dispatcher catches the exception and returns an appropriate error message to the user.

## Features

The serverless cloud system incorporates the following features:

- **Authentication and Authorization:** The system includes an authentication mechanism to verify users and an authorization system to control access to the runtimes based on user roles and permissions.
  - Users are authenticated based on their provided username.
  - User roles and permissions are defined in the auth.py module.
  - The system supports three users: "user1", "user2", and "admin".
    - "user1" has access to invoke only RuntimeAlpha.
    - "user2" has access to invoke only RuntimeBeta.
    - "admin" has complete access and can invoke both RuntimeAlpha and RuntimeBeta.
  - Users can only invoke the runtimes they are authorized to access. If a user tries to invoke a runtime they are not authorized for, the dispatcher returns a permission denied message.
- **Parallel Execution:** The system supports parallel execution of the runtimes. RuntimeAlpha and RuntimeBeta can run in parallel, with a maximum of three active executions of each at any given time.
- **Container Management:** The system uses Docker containers to execute the runtimes. The dispatcher manages the container lifecycle, including starting and stopping containers based on the workload and idle timeout.
- **Usage Tracking:** The system tracks the usage of the runtimes for each user. It records the start time, end time, and duration of each runtime execution and stores the usage data in a log file.
- **Error Handling:** The system includes error handling mechanisms to gracefully handle exceptions and provide meaningful error messages to the users.
- **User Interface:** The system provides a user-friendly interface using Streamlit, allowing users to select their username, specify the number of invocations for each runtime, enter prompts, and invoke the runtimes. The generated responses are displayed in the user interface.

## Environment Setup

To set up the environment for running the serverless cloud system, follow these steps:

1. Ensure that you have Docker and Docker Compose installed on your machine.
2. Open a terminal and navigate to the project directory.
3. Run the following command to build and start the Docker containers:
   ```bash
   docker-compose up --build
4. Wait for the containers to start up. You should see output indicating that the containers are running and ready to accept requests.
5. Open a New Terminal Window: This will be used to run the user interface.

## Usage

To use the serverless cloud system, follow these steps after completing the environment setup:

1. **Ensure Docker Containers Running:** Make sure the Docker containers are running in a separate terminal window.
2. **Navigate to Project Directory:** In the new terminal window, navigate to the project directory where the serverless cloud system is located.
3. **Install Python Dependencies:** Run the following command to install the required Python dependencies.

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the User Interface:** Execute the command below to run the user interface application.

    ```bash
    streamlit run user_facing.py
    ```

5. **Access the User Interface:** Open your web browser and go to `http://localhost:8501` to access the user interface.
6. **Use the System:** Within the user interface, select your username from the dropdown menu (`user1`, `user2`, or `admin`), specify the number of invocations for RuntimeAlpha and RuntimeBeta, enter the desired prompts, and click the "Invoke Runtimes" button.
7. **View Responses:** The generated responses for each runtime will be displayed in the user interface.

**Note:** Keep the terminal with the running Docker containers active while using the serverless cloud system. Closing the terminal or stopping the containers will make the system inaccessible.

## Future Enhancements

Several areas can be improved in future iterations of the serverless cloud system:

- **Dynamic Scaling:** Implement dynamic scaling of containers based on the workload to efficiently handle variable workloads.
- **Improved Load Balancing:** Enhance the load balancing algorithm for better distribution across containers.
- **Message Queue Integration:** Integrate a message queue system like RabbitMQ or Celery for improved scalability and robustness.
- **Billing and Cost Optimization:** Implement a billing system to track usage and optimize costs associated with container usage.
- **Monitoring and Logging:** Enhance monitoring and logging for better visibility into system performance and troubleshooting.
- **Security Enhancements:** Strengthen security measures, including secure communication, data encryption, and role-based access control.

## Conclusion

The serverless cloud system provides a functional mockup for invoking RuntimeAlpha and RuntimeBeta with specified prompts. While it meets core requirements, there is significant scope for enhancements in scalability, load balancing, billing, monitoring, and security. With further development, this project can evolve into a robust, efficient, and production-ready serverless platform.