FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN mkdir -p /root/.cache/torch/hub/checkpoints && \
    wget --no-check-certificate -P /root/.cache/torch/hub/checkpoints  https://download.pytorch.org/models/resnet18-5c106cde.pth
WORKDIR /app
COPY . .
RUN python3 -m pip install -r requirements.txt



EXPOSE 8080

CMD [ "python", "app.py" ]
