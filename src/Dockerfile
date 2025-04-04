FROM public.ecr.aws/lambda/python:3.9.2025.04.03.11

#COPY requirements.txt

COPY requirements.txt ${LAMBDA_TASK_ROOT}
# Install any needed packages specified in requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy Function code

COPY lambda_function.py  ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.lambda_handler" ]