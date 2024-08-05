import logging
import time
import uuid

import uvicorn
from fastapi import FastAPI, Request
from fastapi_health import health

import router as endpoints
from container import Container
from router import user_prompt_apis

# Create a logger for logging in the application
logger = logging.getLogger(__name__)


def healthy_condition():
    return {"service": "online"}


def sick_condition():
    return False  # True


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml("resource/config.yml")
    # print(f"container.config: {container.config}")

    # APIs will be dependent on service/repository so we will need to wire API's package/modules
    container.wire(packages=[endpoints])

    app = FastAPI()

    app.container = container

    # Include api routes
    app.include_router(user_prompt_apis.router)
    app.add_api_route("/health", health([healthy_condition, sick_condition]))

    # TODO expose the metrics to tools like prometheus/grafana uncomment lines below
    # Instrumentator().instrument(app, metric_namespace='cpi', metric_subsystem='onlinecomponent').expose(app)
    # app.add_route("/metrics", metrics)

    return app


app = create_app()


@app.on_event("shutdown")
async def shutdown_event():
    pass
    # if Container.db.provided:
    #     await Container.db.provided.close()


# print every request and response with process time
@app.middleware("http")
async def log_requests(request: Request, call_next):
    rid = uuid.uuid4()
    logger.info(f"rid={rid} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={rid} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001, access_log=True)
