# start by pulling the python image
FROM python:3.8-alpine

# copy the requerimientos file into the image
COPY ./requerimientos.txt /portal_empleados/requerimientos.txt

# switch working directory
WORKDIR /portal_empleados

# install the dependencies and packages in the requerimientos file
RUN pip install -r requerimientos.txt

# copy every content from the local file to the image
COPY . /portal_empleados/

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["run.py" ]