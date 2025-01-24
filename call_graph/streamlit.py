# import os
# import streamlit as st
# import boto3
# from botocore.exceptions import NoCredentialsError
# from dotenv import load_dotenv

# load_dotenv()

# # Initialize Streamlit app
# st.title("Graph Visualizer")

# print(f"AWS Access Key ID: {os.getenv('AWS_ACCESS_KEY_ID')}")
# print(f"AWS Secret Access Key: {os.getenv('AWS_SECRET_ACCESS_KEY')}")

# # AWS S3 configuration
# s3 = boto3.client(
#     "s3",
#     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
#     region_name="ca-central-1"
# )

# bucket_name = "graphbucket222"

# # Function to list files from S3
# def list_s3_objects():
#     try:
#         response = s3.list_objects_v2(Bucket=bucket_name)
#         if "Contents" in response:
#             return [obj["Key"] for obj in response["Contents"]]
#         else:
#             return []
#     except NoCredentialsError:
#         st.error("AWS credentials not available.")
#         return []
#     except Exception as e:
#         st.error(f"Error fetching objects: {e}")
#         return []

# # Get list of files from S3
# file_list = list_s3_objects()

# if not file_list:
#     st.warning("No files found in the S3 bucket.")
# else:
#     # Multiselect dropdown for selecting files
#     selected_files = st.multiselect(
#         "Select files to visualize:",
#         options=file_list,
#         help="Start typing to search for files."
#     )

#     # Display HTML content for selected files
#     if selected_files:
#         for file_key in selected_files:
#             try:
#                 # Fetch the file content
#                 obj = s3.get_object(Bucket=bucket_name, Key=file_key)
#                 html_content = obj["Body"].read().decode("utf-8")

#                 st.markdown(f"### Preview: {file_key}")
#                 st.components.v1.html(html_content, height=600, scrolling=True)
#             except Exception as e:
#                 st.error(f"Failed to load {file_key}: {e}")
