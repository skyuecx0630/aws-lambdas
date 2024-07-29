FROM public.ecr.aws/lambda/python:3.12

# ENV LAMBDA_TASK_ROOT=/var/task
WORKDIR /var/task

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY lambda_function.py .

CMD [ "lambda_function.handler" ]


# # Define custom function directory
# ARG FUNCTION_DIR="/var/task"

# FROM python:3.12 as build-image

# ARG FUNCTION_DIR
# WORKDIR ${FUNCTION_DIR}

# RUN pip install --target . awslambdaric

# COPY requirements.txt .
# RUN pip install --target . -r requirements.txt


# FROM python:3.12-slim

# ARG FUNCTION_DIR
# WORKDIR ${FUNCTION_DIR}

# RUN curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie \
#     && chmod +x /usr/local/bin/aws-lambda-rie
# # # If architecture is arm64
# # RUN curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie-arm64 \
# #     && chmod +x /usr/local/bin/aws-lambda-rie

# COPY --chmod=755 lambda-entrypoint.sh /lambda-entrypoint.sh

# COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
# COPY lambda_function.py .

# ENTRYPOINT [ "/lambda-entrypoint.sh" ]
# # ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# CMD [ "lambda_function.handler" ]