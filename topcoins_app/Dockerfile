#Dockerfile, build image , Container
FROM python:3.8
WORKDIR /topcoins_app
ADD . /topcoins_app
COPY ./requirement.txt .
RUN pip install -r requirement.txt
COPY . .
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["top_coins_service.py"]