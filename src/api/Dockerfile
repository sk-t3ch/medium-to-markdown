# Define global args
ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.9"
ARG DISTRO_VERSION="3.12"
ARG PY_PI_URL="pypi.dev.t3chflicks.org"

# Stage 1 - bundle base image + runtime
# Grab a fresh copy of the image and install GCC
FROM python:${RUNTIME_VERSION}-slim AS build-image

# Include global args in this stage of the build
ARG FUNCTION_DIR
ARG RUNTIME_VERSION
ARG PY_PI_URL
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}
# Copy handler function
COPY . ${FUNCTION_DIR}
# Optional – Install the function's dependencies
RUN ls ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install --extra-index-url https://${PY_PI_URL} t3chflicks-service==0.34 --target ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install -r ${FUNCTION_DIR}/requirements.txt --target ${FUNCTION_DIR}
# Install Lambda Runtime Interface Client for Python
RUN python${RUNTIME_VERSION} -m pip install awslambdaric --target ${FUNCTION_DIR}

# Stage 3 - final runtime image
# Grab a fresh copy of the Python image
# FROM python:${RUNTIME_VERSION}-alpine${DISTRO_VERSION}
# Include global arg in this stage of the build
# ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}
# Copy in the built dependencies
# COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie
COPY entry.sh /
ENTRYPOINT [ "/entry.sh" ]
CMD [ "main.handler" ]