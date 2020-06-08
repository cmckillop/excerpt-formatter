FROM node:14.4.0
COPY package.json yarn.lock webpack.common.js webpack.dev.js webpack.prod.js app/src /
COPY ./app/src /app/src
RUN yarn
RUN yarn build

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
COPY requirements.txt /
COPY ./app /app
COPY --from=0 /app/dist ./app/dist
RUN pip install -r /requirements.txt
EXPOSE 80
