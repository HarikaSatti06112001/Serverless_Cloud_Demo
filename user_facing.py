# user_facing.py
import streamlit as st
from my_mk1_homework import Alpha, Beta
import concurrent.futures

def invoke_runtime(runtime_class, user, prompt):
    """
    Invokes the specified runtime class with the given user and prompt.
    Returns the response from the runtime execution.
    """
    try:
        response = runtime_class()(user, {"prompt": prompt})
        return response
    except Exception as e:
        return str(e)

def invoke_parallel(runtime_class, user, prompts):
    """
    Invokes the specified runtime class with the given user and prompts in parallel.
    Returns the list of responses from the parallel runtime executions.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(invoke_runtime, runtime_class, user, prompt) for prompt in prompts]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return results

def main():
    """
    Main function that runs the Streamlit user interface.
    """
    st.title("Serverless Cloud Demo")
    st.header("Runtime Invocation")

    user = st.selectbox("Select User", ["user1", "user2", "admin"])

    alpha_count = st.number_input("Number of Alpha Invocations", min_value=1, max_value=5, value=1, step=1)
    beta_count = st.number_input("Number of Beta Invocations", min_value=1, max_value=5, value=1, step=1)
    alpha_prompts = [st.text_input(f"Alpha Prompt {i+1}") for i in range(alpha_count)]
    beta_prompts = [st.text_input(f"Beta Prompt {i+1}") for i in range(beta_count)]

    invoke_button = st.button("Invoke Runtimes")
    if invoke_button:
        alpha_responses = invoke_parallel(Alpha, user, alpha_prompts)
        beta_responses = invoke_parallel(Beta, user, beta_prompts)

        st.subheader("Alpha Responses")
        for i, response in enumerate(alpha_responses, start=1):
            st.write(f"Alpha {i}: {response}")

        st.subheader("Beta Responses")
        for i, response in enumerate(beta_responses, start=1):
            st.write(f"Beta {i}: {response}")

if __name__ == "__main__":
    main()