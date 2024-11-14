from pydantic import BaseModel
from openai import OpenAI
import os
import time
from colorama import init, Fore, Style
from pprint import pprint  # Import the pprint module

# Initialize colorama
init()

# Initialize OpenAI API (Make sure to set your OpenAI API key)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")  # Load API key from environment variable
)

# Define a Pydantic model for structured output
class StepEvaluationResponse(BaseModel):
    success: str  # "yes" or "no"
    feedback: str  # Optional feedback message

def chat_gpt_agent(input_text, current_state):
    """
    This function interacts with the OpenAI ChatGPT model to simulate a step action.
    """
    response = client.chat.completions.create(
        model="gpt-4o",  # Adjust the model as needed (e.g., gpt-4o for structured outputs)
        messages=[
            {"role": "system", "content": "You are an assistant executing sequential tasks."},
            {"role": "user", "content": f"Current state:\n{current_state}\n\nNext step:\n{input_text}"}
        ],
        max_tokens=100
    )
    selection = response.choices[0].message.content.strip()
    return selection

def step_evaluation_agent(step, result):
    """
    This function interacts with a secondary OpenAI ChatGPT agent to evaluate if a step was successful,
    using structured output.
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",  # Use structured output-capable model
        messages=[
            {"role": "system", "content": "You are an agent that evaluates the success or failure of a given task based on its outcome. Please respond with a structured JSON object that includes 'success' (yes/no) and 'feedback' (optional) as keys."},
            {"role": "user", "content": f"Step: '{step}'\nResult: '{result}'\nDetermine if this step was successful or not, and provide feedback if necessary."}
        ],
        response_format=StepEvaluationResponse
    )
    
    return response.choices[0].message.parsed

def step_callback(step, result):
    """
    Callback function that uses another agent to determine if a step was successfully executed.
    """
    evaluation = step_evaluation_agent(step, result)
    print(f"\n{Fore.CYAN}Evaluation result: {Style.RESET_ALL}{evaluation}")

    if evaluation.success.lower() == "yes":
        print(f"{Fore.GREEN}✓ Step '{step}' executed successfully.{Style.RESET_ALL}")
        return True, None
    else:
        feedback = evaluation.feedback or "No feedback provided."
        print(f"{Fore.RED}✗ Step '{step}' failed based on evaluation. Retrying...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Feedback: {feedback}{Style.RESET_ALL}\n")
        return False, feedback

def execute_step_trace(trace, initial_state):
    """
    This function iterates over each step in the trace and executes it using the ChatGPT agent,
    while accumulating state.
    """
    current_state = initial_state
    successful_steps = {}
    for step in trace:
        print(f"\n{Fore.BLUE}{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Starting execution of step: {Fore.WHITE}'{step}'{Style.RESET_ALL}")
        success = False
        feedback = None
        while not success:
            input_text = step if not feedback else f"{step} (Retry with feedback: {feedback})"
            print(f"\n{Fore.MAGENTA}Sending input to agent:{Style.RESET_ALL}\n{input_text}")
            result = chat_gpt_agent(input_text, current_state)
            print(f"\n{Fore.MAGENTA}Result from agent:{Style.RESET_ALL}\n{result}")

            success, feedback = step_callback(step, result)

            if success:
                current_state += f"\n\nStep: {step}\nResult: {result}"
                successful_steps[step] = result
            else:
                time.sleep(2)

        print(f"\n{Fore.GREEN}✓ Finished execution of step: '{step}'{Style.RESET_ALL}")
    print(f"\n{Fore.BLUE}{'='*60}{Style.RESET_ALL}\n")
    
    
    return successful_steps
# Example initial state (the word problem)
initial_state = "Emily has twice as many apples as Bob. Together, they have 36 apples. How many apples does each person have?"

# Example trace
trace = [
    "Read the problem statement",
    "Identify known quantities",
    "Identify unknown quantities",
    "Translate the word problem into mathematical expressions",
    "Set up equations based on the relationships described",
    "Solve the equations to find the unknowns",
    "Check the solution by substituting values back into the original problem",
    "Interpret the solution in the context of the problem",
    "Write the final answer with appropriate units or context"
]

# Execute the trace
successful_steps = execute_step_trace(trace, initial_state)

# Pretty print the successful steps with key-value pairs on new lines
print("\nSuccessful Steps:\n")
for key, value in successful_steps.items():
    print(f"\n\nStep: {key}\nResult: {value}\n{'-' * 60}")