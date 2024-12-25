#!/usr/bin/env python
import sys
import warnings
from crewai import Crew, Process

from mareting_dept.crew import MarketingDept

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



def run():
    """
    Run the crew.
    """
    print("Choose an option:")
    print("1. Get New Strategy")
    print("2. Email Response")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        print("Generating a new 30-day marketing strategy...")
        company_name="tesla"
        website="https://www.tesla.com/"
        about="tesla is leading electric manufacture"
        latest_product="launcing model5 car to the market"
        inputs = {
        'company_name': company_name,
        'Company_website': website,
        'about': about,
        'latest_product': latest_product,
        'project_description': f"""
            {company_name}, a leader in {about}, is preparing a strategic marketing campaign to promote its new offering: {latest_product}. 
            This campaign will highlight key advantages of the product/service, focusing on innovation, industry relevance, and integration into client workflows. 
            The campaign aims to target industry leaders and professionals who appreciate cutting-edge technology and transformative solutions.

           
            Project Overview: Design and execute a comprehensive a week marketing campaign that promotes {latest_product} and elevates the brand presence of {company_name}.
        """
    }
        result = MarketingDept().crew().kickoff(inputs=inputs)
        print("Result:", result)
    elif choice == "2":
        print("Email Response Selected")
        sent_email = input("Enter the email you sent to the client: ")
        client_reply = input("Enter the client's response: ")
        print("Generating a professional reply...")
        
        # Instantiate the MarketingDept class
        marketing_dept = MarketingDept()

        # Create a temporary crew for the email_response_task
        email_response_crew = Crew(
            agents=[marketing_dept.email_marketer()],
            tasks=[marketing_dept.email_response_task()],
            process=Process.sequential,
            verbose=True,
        )

        # Execute the crew with specific inputs
        response = email_response_crew.kickoff(
            inputs={"sent_email": sent_email, "client_reply": client_reply}
        )

        print("Suggested Reply:", response)


    else:
        print("Invalid choice. Please restart.")
   
    


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         MaretingDept().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         MaretingDept().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         MaretingDept().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")
